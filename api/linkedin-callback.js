import { Redis } from "@upstash/redis";

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
    const error = url.searchParams.get("error_description") || url.searchParams.get("error");
    if (error) return page(res, `<h1>Connection cancelled</h1><p>${escapeHtml(error)}</p>`, 200);
    if (!code) return page(res, "<h1>Missing code</h1><p>LinkedIn did not return an authorization code.</p>", 400);
    const { LINKEDIN_CLIENT_ID: clientId, LINKEDIN_CLIENT_SECRET: clientSecret, LINKEDIN_REDIRECT_URI: redirectUri } = process.env;
    if (!clientId || !clientSecret || !redirectUri) return page(res, "<h1>Not configured yet</h1><p>LinkedIn environment variables are missing.</p>", 500);
    try {
        const body = new URLSearchParams({ grant_type: "authorization_code", code, redirect_uri: redirectUri, client_id: clientId, client_secret: clientSecret });
        const tokenRes = await fetch("https://www.linkedin.com/oauth/v2/accessToken", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body });
        const tokenData = await tokenRes.json();
        if (!tokenRes.ok || !tokenData.access_token) return page(res, `<h1>Token exchange failed</h1><pre>${escapeHtml(JSON.stringify(tokenData, null, 2))}</pre>`, 500);
        const profileData = await (await fetch("https://api.linkedin.com/v2/userinfo", { headers: { Authorization: `Bearer ${tokenData.access_token}` } })).json();
        await getRedis().set("linkedin-token:primary", { access_token: tokenData.access_token, refresh_token: tokenData.refresh_token || null, expires_in: tokenData.expires_in || 3600, obtained_at: Date.now(), profile: profileData || null });
        return page(res, "<h1>LinkedIn connected</h1><p>The account is ready to post.</p>", 200);
    } catch (err) { return page(res, `<h1>Unexpected error</h1><pre>${escapeHtml(String(err))}</pre>`, 500); }
}
function page(res, body, status) { res.status(status).setHeader("Content-Type", "text/html").send(`<!doctype html><html><body style="font-family:sans-serif;max-width:560px;margin:60px auto;padding:0 20px">${body}</body></html>`); }
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char])); }
