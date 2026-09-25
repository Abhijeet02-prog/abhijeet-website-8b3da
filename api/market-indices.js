// Live Nifty 50 / Sensex / Bank Nifty data for the hero market ticker.
//
// Fetched here (server-side) rather than straight from the browser for two
// reasons: Yahoo Finance's chart endpoint doesn't send CORS headers for
// arbitrary origins, so a direct browser fetch would just fail; and putting
// our own Cache-Control layer in front of it means many visitors loading
// the site around the same time share one upstream request instead of each
// triggering a fresh one.
//
// This is Yahoo's public "chart" endpoint — undocumented/unofficial (the
// same one the popular yfinance Python library relies on), but free, with
// no API key or signup. Being unofficial, it can occasionally rate-limit
// or change shape without notice, which is why every symbol fetch below is
// wrapped in its own try/catch: one symbol failing returns null values for
// just that entry instead of taking down the whole ticker.
//
// NON-NEGOTIABLE requirement: post-market hours and market holidays must
// keep showing the exact figure from when the market was last live — never
// blank, zero, or a "—". Confirmed live (25 Sep 2026, during market hours)
// that Yahoo's own meta already freezes regularMarketPrice/previousClose at
// the last traded values once trading stops for the day (regularMarketTime
// simply stops advancing) — so a plain market close or holiday is already
// covered for free by Yahoo itself. The real gap is an upstream hiccup: a
// transient network error, rate-limit, or shape change from this unofficial
// endpoint, which would otherwise blank an index out even though nothing
// about the market actually changed. To close that gap, every successful
// fetch is cached in Redis as "last known good", and a failed fetch falls
// back to that cached value instead of returning nulls.

import { Redis } from "@upstash/redis";

const SYMBOLS = [
    { symbol: "^NSEI", name: "NIFTY 50" },
    { symbol: "^BSESN", name: "SENSEX" },
    { symbol: "^NSEBANK", name: "BANK NIFTY" },
];

const CACHE_PREFIX = "market-index:";

// Same env-var fallback as api/instagram-media.js: Redis.fromEnv() only
// looks for UPSTASH_REDIS_REST_URL/_TOKEN, but Vercel's own "Upstash for
// Redis" marketplace integration (Storage tab) creates KV_REST_API_URL/
// KV_REST_API_TOKEN instead. Building the client explicitly from whichever
// pair is present avoids depending on which naming convention this
// project's storage integration happens to use.
function getRedis() {
    const url = process.env.UPSTASH_REDIS_REST_URL || process.env.KV_REST_API_URL;
    const token = process.env.UPSTASH_REDIS_REST_TOKEN || process.env.KV_REST_API_TOKEN;
    if (!url || !token) throw new Error("no Redis REST URL/token found in environment (checked UPSTASH_REDIS_REST_* and KV_REST_API_*)");
    return new Redis({ url, token });
}

export default async function handler(req, res) {
    const indices = await Promise.all(SYMBOLS.map(fetchQuote));
    const ok = indices.some((idx) => idx.price != null);

    // s-maxage lets Vercel's edge cache serve the same response to many
    // visitors for 30s instead of hitting Yahoo per page load; the ticker
    // itself polls this endpoint every 60s from the client.
    res
        .setHeader("Cache-Control", "public, max-age=0, s-maxage=30, stale-while-revalidate=60")
        .status(200)
        .json({ updatedAt: new Date().toISOString(), ok, indices });
}

async function fetchQuote({ symbol, name }) {
    try {
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}`;
        const upstream = await fetch(url, {
            headers: { "User-Agent": "Mozilla/5.0 (compatible; abhijeettoshniwal.com market-ticker/1.0)" },
        });
        if (!upstream.ok) throw new Error(`upstream_${upstream.status}`);

        const data = await upstream.json();
        const meta = data?.chart?.result?.[0]?.meta;
        if (!meta || meta.regularMarketPrice == null) throw new Error("no_meta");

        const price = meta.regularMarketPrice;
        const prevClose = meta.previousClose ?? meta.chartPreviousClose ?? null;
        const change = prevClose != null ? price - prevClose : null;
        const changePercent = prevClose ? (change / prevClose) * 100 : null;

        const result = { symbol, name, price, change, changePercent };

        // Best-effort cache write. Never let a Redis problem fail the
        // actual request — worst case we just don't have a fallback ready
        // for next time.
        cacheLastGood(symbol, result).catch(() => {});

        return result;
    } catch (err) {
        // Upstream failed (rate-limited, network blip, shape change, etc).
        // Serve the last known-good value instead of going blank — this is
        // what makes the "always show the last live figure" guarantee hold
        // even when Yahoo itself is briefly unreachable, not just when the
        // market is closed.
        const cached = await readLastGood(symbol);
        if (cached) return { ...cached, name };
        return { symbol, name, price: null, change: null, changePercent: null, error: String(err) };
    }
}

async function cacheLastGood(symbol, result) {
    await getRedis().set(CACHE_PREFIX + symbol, result);
}

async function readLastGood(symbol) {
    try {
        return await getRedis().get(CACHE_PREFIX + symbol);
    } catch (err) {
        return null;
    }
}
