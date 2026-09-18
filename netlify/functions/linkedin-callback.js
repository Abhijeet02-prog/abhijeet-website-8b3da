// GET /api/linkedin-callback?code=...&state=primary
// Exchanges the OAuth code for an access token and stores the token in Netlify Blobs.
import { getStore } from "@netlify/blobs";

export default async (req) => {
    const url = new URL(req.url);
    const code = url.searchParams.get("code");
    const state = url.searchParams.get("state") || "primary";
    const errorDescription = url.searchParams.get("error_description") || url.searchParams.get("error");

    if (errorDescription) {
        return html(`<h1>Connection cancelled</h1><p>${escapeHtml(errorDescription)}</p>`, 200);
    }

    if (!code) {
        return html(`<h1>Missing code</h1><p>LinkedIn did not return an authorization code.</p>`, 400);
    }

    const clientId = Netlify.env.get("LINKEDIN_CLIENT_ID");
    const clientSecret = Netlify.env.get("LINKEDIN_CLIENT_SECRET");
    const redirectUri = Netlify.env.get("LINKEDIN_REDIRECT_URI");

    if (!clientId || !clientSecret || !redirectUri) {
        return html(`<h1>Not configured yet</h1><p>Set LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET and LINKEDIN_REDIRECT_URI.</p>`, 500);
    }

    try {
        const body = new URLSearchParams({
            grant_type: "authorization_code",
            code,
            redirect_uri: redirectUri,
            client_id: clientId,
            client_secret: clientSecret,
        });

        const tokenRes = await fetch("https://www.linkedin.com/oauth/v2/accessToken", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body,
        });

        const tokenData = await tokenRes.json();

        if (!tokenRes.ok || !tokenData.access_token) {
            return html(`<h1>Token exchange failed</h1><pre>${escapeHtml(JSON.stringify(tokenData, null, 2))}</pre>`, 500);
        }

        const profileRes = await fetch("https://api.linkedin.com/v2/userinfo", {
            headers: { Authorization: `Bearer ${tokenData.access_token}` },
        });

        const profileData = await profileRes.json();

        const store = getStore("linkedin-token");
        await store.setJSON("primary", {
            access_token: tokenData.access_token,
            refresh_token: tokenData.refresh_token || null,
            expires_in: tokenData.expires_in || 3600,
            obtained_at: Date.now(),
            profile: profileData || null,
            state,
        });

        return html(`<h1>LinkedIn connected ✓</h1><p>The LinkedIn account is connected and ready to post. You can close this tab.</p>`, 200);
    } catch (err) {
        return html(`<h1>Unexpected error</h1><pre>${escapeHtml(String(err))}</pre>`, 500);
    }
};

function html(body, status) {
    return new Response(
        `<!doctype html><html><body style="font-family:sans-serif; max-width:560px; margin:60px auto; padding:0 20px;">${body}</body></html>`,
        { status, headers: { "Content-Type": "text/html" } }
    );
}

function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

export const config = { path: "/api/linkedin-callback" };
