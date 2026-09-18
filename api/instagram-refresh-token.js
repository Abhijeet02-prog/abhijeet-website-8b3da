import { Redis } from "@upstash/redis";

const ACCOUNTS = ["music", "writing"];

export default async function handler(req, res) {
    if (req.headers.authorization !== `Bearer ${process.env.CRON_SECRET}`) return res.status(401).send("Unauthorized");
    const redis = Redis.fromEnv();
    const results = {};
    for (const account of ACCOUNTS) {
        const data = await redis.get(`instagram-token:${account}`);
        if (!data?.access_token) { results[account] = "not_connected"; continue; }
        try {
            const url = `https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${encodeURIComponent(data.access_token)}`;
            const json = await (await fetch(url)).json();
            if (json.access_token) {
                await redis.set(`instagram-token:${account}`, { access_token: json.access_token, obtained_at: Date.now(), expires_in: json.expires_in || 5184000 });
                results[account] = "refreshed";
            } else results[account] = `refresh_failed: ${JSON.stringify(json)}`;
        } catch (err) { results[account] = `error: ${String(err)}`; }
    }
    return res.status(200).json(results);
}