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
    const url = new URL(req.url, `https://${req.headers.host}`);
    const code = url.searchParams.get("code");
    const state = url.searchParams.get("state");
    const oauthError = url.searchParams.get("error_description") || url.searchParams.get("error");
    if (oauthError) return page(res, `<h1>Connection cancelled</h1><p>${escapeHtml(oauthError)}</p>`, 200);
    if (!code || !ACCOUNTS.includes(state)) return page(res, `<h1>Something's missing</h1><p>No authorization code, or an unexpected account (${escapeHtml(state || "none")}).</p>`, 400);

    const { INSTAGRAM_APP_ID: appId, INSTAGRAM_APP_SECRET: appSecret, INSTAGRAM_REDIRECT_URI: redirectUri } = process.env;
    if (!appId || !appSecret || !redirectUri) return page(res, "<h1>Not configured yet</h1><p>Instagram environment variables are missing.</p>", 500);

    try {
        const form = new URLSearchParams({ client_id: appId, client_secret: appSecret, grant_type: "authorization_code", redirect_uri: redirectUri, code });
        const shortRes = await fetch("https://api.instagram.com/oauth/access_token", { method: "POST", body: form });
        const shortJson = await shortRes.json();
        if (!shortJson.access_token) return page(res, `<h1>Token exchange failed</h1><pre>${escapeHtml(JSON.stringify(shortJson, null, 2))}</pre>`, 500);

        const longUrl = `https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=${encodeURIComponent(appSecret)}&access_token=${encodeURIComponent(shortJson.access_token)}`;
        const longJson = await (await fetch(longUrl)).json();
        if (!longJson.access_token) return page(res, `<h1>Long-lived token exchange failed</h1><pre>${escapeHtml(JSON.stringify(longJson, null, 2))}</pre>`, 500);

        await getRedis().set(`instagram-token:${state}`, { access_token: longJson.access_token, obtained_at: Date.now(), expires_in: longJson.expires_in || 5184000 });
        return page(res, `<h1>Connected</h1><p>The <strong>${escapeHtml(state)}</strong> Instagram account is linked.</p>`, 200);
    } catch (err) {
        return page(res, `<h1>Unexpected error</h1><pre>${escapeHtml(String(err))}</pre>`, 500);
    }
}

function page(res, body, status) {
    res.status(status).setHeader("Content-Type", "text/html").send(`<!doctype html><html><body style="font-family:sans-serif;max-width:560px;margin:60px auto;padding:0 20px">${body}</body></html>`);
}
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char])); }
