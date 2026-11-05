// LinkedIn follower and impression figures for the homepage proof strip.
//
// Sources, in order:
//  1. LinkedIn's official API, once a token with the analytics scopes has
//     been connected via /api/linkedin-auth?for=stats (stored in Redis as
//     "linkedin-token:stats"). Followers come from memberFollowersCount and
//     impressions from memberCreatorPostAnalytics. These scopes belong to
//     LinkedIn's Community Management API product, which LinkedIn must
//     approve for the app first. Queried once per day, after 11:00 AM IST,
//     and frozen until the next 11:00.
//  2. assets/linkedin-stats.json in this repo: the figures as shown on the
//     LinkedIn profile (follower count, and the impressions figure from the
//     headline). Updated by the daily 11:00 AM IST job that reads the profile.
//  3. Built-in defaults, so the strip is never empty.

import { Redis } from "@upstash/redis";

const IST_OFFSET_MS = 5.5 * 60 * 60 * 1000;
const DEFAULTS = { followers: 3700, followersLabel: "3,700+", impressions: 250000, impressionsLabel: "250k+" };

function getRedis() {
    const url = process.env.UPSTASH_REDIS_REST_URL || process.env.KV_REST_API_URL;
    const token = process.env.UPSTASH_REDIS_REST_TOKEN || process.env.KV_REST_API_TOKEN;
    if (!url || !token) return null;
    try { return new Redis({ url, token }); } catch { return null; }
}

function editionDate(now = Date.now()) {
    const ist = new Date(now + IST_OFFSET_MS);
    let cut = Date.UTC(ist.getUTCFullYear(), ist.getUTCMonth(), ist.getUTCDate(), 11, 0, 0);
    if (ist.getTime() < cut) cut -= 24 * 3600 * 1000;
    const d = new Date(cut);
    return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, "0")}-${String(d.getUTCDate()).padStart(2, "0")}`;
}

// 3,711 -> "3,700+", 253,400 -> "250k+", 1,240,000 -> "1.2M+"
export function label(n) {
    if (!Number.isFinite(n) || n <= 0) return null;
    if (n < 1000) return `${n}`;
    if (n < 10000) return `${(Math.floor(n / 100) * 100).toLocaleString("en-US")}+`;
    if (n < 1000000) return `${Math.floor(n / 10000) * 10}k+`;
    return `${(Math.floor(n / 100000) / 10).toString()}M+`;
}

async function fromApi(redis) {
    if (!redis) return null;
    let tok;
    try { tok = await redis.get("linkedin-token:stats"); } catch { return null; }
    if (!tok?.access_token) return null;
    const headers = {
        Authorization: `Bearer ${tok.access_token}`,
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": process.env.LINKEDIN_API_VERSION || "202610",
    };
    const out = {};
    try {
        const r = await fetch("https://api.linkedin.com/rest/memberFollowersCount?q=me", { headers });
        if (r.ok) {
            const j = await r.json();
            const n = j?.elements?.[0]?.memberFollowersCount;
            if (Number.isFinite(n)) out.followers = n;
        }
    } catch { /* fall through */ }
    try {
        const r = await fetch("https://api.linkedin.com/rest/memberCreatorPostAnalytics?q=me&queryType=IMPRESSION&aggregation=TOTAL", { headers });
        if (r.ok) {
            const j = await r.json();
            const n = j?.elements?.[0]?.count;
            if (Number.isFinite(n)) out.impressions = n;
        }
    } catch { /* fall through */ }
    return Object.keys(out).length ? out : null;
}

async function fromFile(req) {
    try {
        const host = req.headers["x-forwarded-host"] || req.headers.host;
        const r = await fetch(`https://${host}/assets/linkedin-stats.json`, { cache: "no-store" });
        if (!r.ok) return null;
        return await r.json();
    } catch { return null; }
}

export default async function handler(req, res) {
    const redis = getRedis();
    const date = editionDate();
    let stats = null, source = "default";

    // Official API: once per 11:00 IST edition.
    if (redis) {
        try { stats = await redis.get(`linkedin-stats:${date}`); } catch { stats = null; }
        if (stats) source = "api";
    }
    if (!stats) {
        const api = await fromApi(redis);
        if (api) {
            stats = api; source = "api";
            if (redis) { try { await redis.set(`linkedin-stats:${date}`, api, { ex: 3 * 24 * 3600 }); } catch { /* best effort */ } }
        }
    }

    const file = await fromFile(req);
    const followers = stats?.followers ?? file?.followers ?? DEFAULTS.followers;
    const impressions = stats?.impressions ?? file?.impressions ?? DEFAULTS.impressions;
    if (!stats && file) source = "profile";

    res.setHeader("Cache-Control", "public, max-age=300, s-maxage=600, stale-while-revalidate=3600");
    res.status(200).json({
        followers,
        followersLabel: (source === "profile" && file?.followersLabel) || label(followers) || DEFAULTS.followersLabel,
        impressions,
        impressionsLabel: (source === "profile" && file?.impressionsLabel) || label(impressions) || DEFAULTS.impressionsLabel,
        updated: file?.updated || null,
        source,
    });
}
