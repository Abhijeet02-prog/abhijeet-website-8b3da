// Daily "Today's briefing" for the Profile page's Writing section.
//
// One edition per day, cut at 11:00 AM IST. An edition holds the top
// headlines (published in the 24 hours before the cut-off) for each topic
// Abhijeet writes about. Headlines come from Google News' public RSS search
// (India edition, no API key), and each item links out to the original
// publisher; we show only the headline, the source name and the time.
//
// Freezing per day: the first request after 11:00 IST (normally the Vercel
// cron in vercel.json, at 05:30 UTC) builds the edition and stores it in
// Redis under that day's key, so everyone sees the same briefing until the
// next 11:00. If Redis is unavailable the edition is still built, and the
// CDN caches it until the next cut-off. If Google News fails, the last good
// edition is served instead of an empty section.

import { Redis } from "@upstash/redis";

const TOPICS = [
    { id: "markets", label: "Markets", query: "Sensex OR Nifty OR \"stock market\"" },
    { id: "policy", label: "Policy", query: "RBI OR SEBI OR \"finance ministry\"" },
    { id: "oil", label: "Oil", query: "\"crude oil\" OR Brent OR OPEC" },
    { id: "economy", label: "Economy", query: "\"Indian economy\" OR inflation OR GDP OR GST" },
];

const PER_TOPIC = 3;
const IST_OFFSET_MS = 5.5 * 60 * 60 * 1000;
const CUTOFF_HOUR_IST = 11;
const KEY_PREFIX = "news-edition:";
const LAST_KEY = "news-edition:last";

function getRedis() {
    const url = process.env.UPSTASH_REDIS_REST_URL || process.env.KV_REST_API_URL;
    const token = process.env.UPSTASH_REDIS_REST_TOKEN || process.env.KV_REST_API_TOKEN;
    if (!url || !token) return null;
    try { return new Redis({ url, token }); } catch { return null; }
}

// Most recent 11:00 IST at or before `now`, plus the next one.
export function editionWindow(now = Date.now()) {
    const ist = new Date(now + IST_OFFSET_MS);
    let cutIst = Date.UTC(ist.getUTCFullYear(), ist.getUTCMonth(), ist.getUTCDate(), CUTOFF_HOUR_IST, 0, 0);
    if (ist.getTime() < cutIst) cutIst -= 24 * 3600 * 1000;
    const cutoff = cutIst - IST_OFFSET_MS;
    const d = new Date(cutIst);
    const date = `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, "0")}-${String(d.getUTCDate()).padStart(2, "0")}`;
    return { date, cutoff, next: cutoff + 24 * 3600 * 1000 };
}

function decode(str = "") {
    return str
        .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
        .replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, "\"")
        .replace(/&#39;|&apos;/g, "'").replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
        .replace(/&amp;/g, "&")
        .trim();
}

function tag(block, name) {
    const m = block.match(new RegExp(`<${name}[^>]*>([\\s\\S]*?)</${name}>`));
    return m ? decode(m[1]) : "";
}

export function parseRss(xml) {
    const items = [];
    for (const m of xml.matchAll(/<item>([\s\S]*?)<\/item>/g)) {
        const b = m[1];
        const source = tag(b, "source");
        let title = tag(b, "title");
        if (source && title.endsWith(` - ${source}`)) title = title.slice(0, -(source.length + 3));
        const link = tag(b, "link");
        const published = Date.parse(tag(b, "pubDate"));
        if (!title || !/^https?:\/\//.test(link) || Number.isNaN(published)) continue;
        items.push({ title, link, source, published });
    }
    return items;
}

function normal(t) {
    return t.toLowerCase().replace(/[^a-z0-9 ]/g, "").split(" ").slice(0, 8).join(" ");
}

async function fetchTopic(topic, cutoff, seen) {
    const q = encodeURIComponent(`${topic.query} when:1d`);
    const url = `https://news.google.com/rss/search?q=${q}&hl=en-IN&gl=IN&ceid=IN:en`;
    const r = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 (personal site news briefing)" } });
    if (!r.ok) throw new Error(`google news ${r.status}`);
    const items = parseRss(await r.text())
        .filter((it) => it.published <= cutoff && it.published >= cutoff - 24 * 3600 * 1000)
        .sort((a, b) => b.published - a.published);
    const picked = [];
    for (const it of items) {
        const key = normal(it.title);
        if (seen.has(key)) continue;
        seen.add(key);
        picked.push(it);
        if (picked.length === PER_TOPIC) break;
    }
    return { id: topic.id, label: topic.label, items: picked };
}

async function buildEdition(win) {
    const seen = new Set();
    const topics = [];
    for (const t of TOPICS) {
        try { topics.push(await fetchTopic(t, win.cutoff, seen)); }
        catch { topics.push({ id: t.id, label: t.label, items: [] }); }
    }
    return { date: win.date, cutoff: win.cutoff, next: win.next, topics };
}

const hasItems = (ed) => ed && ed.topics && ed.topics.some((t) => t.items.length);

export default async function handler(req, res) {
    const win = editionWindow();
    const redis = getRedis();
    const key = KEY_PREFIX + win.date;
    let edition = null;
    let stale = false;

    if (redis) {
        try { edition = await redis.get(key); } catch { edition = null; }
    }

    if (!hasItems(edition)) {
        edition = await buildEdition(win);
        if (hasItems(edition)) {
            if (redis) {
                try {
                    await redis.set(key, edition, { ex: 3 * 24 * 3600 });
                    await redis.set(LAST_KEY, edition, { ex: 7 * 24 * 3600 });
                } catch { /* cache is best-effort */ }
            }
        } else if (redis) {
            try {
                const last = await redis.get(LAST_KEY);
                if (hasItems(last)) { edition = last; stale = true; }
            } catch { /* fall through with the empty edition */ }
        }
    }

    const secsToNext = Math.max(60, Math.floor((win.next - Date.now()) / 1000));
    const ok = hasItems(edition);
    res
        .setHeader("Cache-Control", ok && !stale
            ? `public, max-age=300, s-maxage=${secsToNext}`
            : "public, max-age=0, s-maxage=300")
        .status(200)
        .json({ ...edition, stale, updatedLabel: "11:00 AM IST" });
}
