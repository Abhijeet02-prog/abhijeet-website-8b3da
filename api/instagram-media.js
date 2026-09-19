import { Redis } from "@upstash/redis";
import featuredPosts from "./featured-posts.json" with { type: "json" };

const ACCOUNTS = ["music", "writing"];
const DEFAULT_LIMIT = 3;
const FIELDS = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp";

export default async function handler(req, res) {
    const account = new URL(req.url, `https://${req.headers.host}`).searchParams.get("account");
    if (!ACCOUNTS.includes(account)) return res.status(400).json({ error: "invalid_account" });

    // Redis.fromEnv() throws synchronously if UPSTASH_REDIS_REST_URL /
    // UPSTASH_REDIS_REST_TOKEN aren't set on this project, and any network
    // hiccup talking to Upstash throws too. Either used to crash the whole
    // function (500 FUNCTION_INVOCATION_FAILED), which left the frontend's
    // "Loading latest posts..." spinner unresolved instead of falling back
    // to the plain Follow-button UI it already knows how to show. Catching
    // it here means a misconfigured or unreachable Redis degrades to that
    // same graceful fallback instead of a hard failure.
    let tokenData;
    try {
        tokenData = await Redis.fromEnv().get(`instagram-token:${account}`);
    } catch (err) {
        return res.status(200).json({ connected: false, items: [], error: "redis_unavailable", detail: String(err) });
    }
    if (!tokenData?.access_token) return res.status(200).json({ connected: false, items: [] });

    const featuredShortcodes = ((featuredPosts && featuredPosts[account]) || [])
        .map(extractShortcode)
        .filter(Boolean);

    try {
        if (featuredShortcodes.length) {
            const items = await findFeatured(tokenData.access_token, featuredShortcodes);
            if (items.length) return res.setHeader("Cache-Control", "public, max-age=600").status(200).json({ connected: true, items });
        }

        const igUrl = `https://graph.instagram.com/me/media?fields=${FIELDS}&access_token=${encodeURIComponent(tokenData.access_token)}&limit=${DEFAULT_LIMIT}`;
        const igRes = await fetch(igUrl);
        const igJson = await igRes.json();
        if (igJson.error) return res.status(200).json({ connected: true, error: "ig_api_error", detail: igJson.error });
        return res.setHeader("Cache-Control", "public, max-age=600").status(200).json({ connected: true, items: igJson.data || [] });
    } catch (err) {
        return res.status(200).json({ connected: true, error: "fetch_failed", detail: String(err) });
    }
}

function extractShortcode(urlStr) {
    const match = String(urlStr || "").match(/instagram\.com\/(?:p|reel|tv)\/([^/?#]+)/i);
    return match ? match[1] : null;
}

async function findFeatured(accessToken, shortcodes) {
    const found = new Map();
    let nextUrl = `https://graph.instagram.com/me/media?fields=${FIELDS}&access_token=${encodeURIComponent(accessToken)}&limit=50`;
    let pages = 0;
    while (nextUrl && found.size < shortcodes.length && pages < 4) {
        const data = await (await fetch(nextUrl)).json();
        if (data.error) break;
        for (const item of data.data || []) {
            const code = extractShortcode(item.permalink);
            if (code && shortcodes.includes(code) && !found.has(code)) found.set(code, item);
        }
        nextUrl = data.paging?.next || null;
        pages++;
    }
    return shortcodes.map((code) => found.get(code)).filter(Boolean);
}
