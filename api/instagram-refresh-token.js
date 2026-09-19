import { Redis } from "@upstash/redis";

const ACCOUNTS = ["music", "writing"];

// See api/instagram-media.js for why this doesn't use Redis.fromEnv():
// Vercel's "Upstash for Redis" marketplace integration names the env vars
// KV_REST_API_URL / KV_REST_API_TOKEN, not the UPSTASH_REDIS_REST_* names
// fromEnv() looks for.
function getRedis() {
    const url = process.env.UPSTASH_REDIS_REST_URL || process.env.KV_REST_API_URL;
    const token = process.env.UPSTASH_REDIS_REST_TOKEN || process.env.KV_REST_API_TOKEN;
    if (!url || !token) throw new Error("no Redis REST URL/token found in environment (checked UPSTASH_REDIS_REST_* and KV_REST_API_*)");
    return new Redis({ url, token });
}

export default async function handler(req, res) {
    if (req.headers.authorization !== `Bearer ${process.env.CRON_SECRET}`) return res.status(401).send("Unauthorized");
    // Same reasoning as api/instagram-media.js: a bad/missing Redis config
    // throws synchronously. Left uncaught, that crashes the whole daily
    // cron run (500) instead of reporting a clear per-run status — catch
    // it once, up front, and report it.
    let redis;
    try {
        redis = getRedis();
    } catch (err) {
        return res.status(200).json({ error: "redis_unavailable", detail: String(err) });
    }
    const results = {};
    for (const account of ACCOUNTS) {
        try {
            const data = await redis.get(`instagram-token:${account}`);
            if (!data?.access_token) { results[account] = "not_connected"; continue; }
            const url = `https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${encodeURIComponent(data.access_token)}`;
            const json = await (await fetch(url)).json();
            if (json.access_token) {
                await redis.set(`instagram-token:${account}`, { access_token: json.access_token, obtained_at: Date.now(), expires_in: json.expires_in || 5184000 });
                results[account] = "refreshed";
            } else results[account] = `refresh_failed: ${JSON.stringify(json)}`;
        } catch (err) { results[account] = `error: ${String(err)}`; }
        // one account's failure (bad token, transient Upstash/Graph API
        // error) no longer aborts the loop before the other account gets
        // its own refresh attempt
    }
    return res.status(200).json(results);
}
