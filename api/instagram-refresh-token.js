import { Redis } from "@upstash/redis";

const ACCOUNTS = ["music", "writing"];

export default async function handler(req, res) {
    if (req.headers.authorization !== `Bearer ${process.env.CRON_SECRET}`) return res.status(401).send("Unauthorized");
    // Same reasoning as api/instagram-media.js: Redis.fromEnv() throws
    // synchronously if Upstash isn't configured/reachable. Left uncaught,
    // that crashes the whole daily cron run (500) instead of reporting a
    // clear per-run status — catch it once, up front, and report it.
    let redis;
    try {
        redis = Redis.fromEnv();
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
