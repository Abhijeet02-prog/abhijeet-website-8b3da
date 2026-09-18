export default function handler(req, res) {
    const { LINKEDIN_CLIENT_ID: clientId, LINKEDIN_REDIRECT_URI: redirectUri } = process.env;
    if (!clientId || !redirectUri) return res.status(500).send("Set LINKEDIN_CLIENT_ID and LINKEDIN_REDIRECT_URI.");
    const url = new URL("https://www.linkedin.com/oauth/v2/authorization");
    url.search = new URLSearchParams({ response_type: "code", client_id: clientId, redirect_uri: redirectUri, state: "primary", scope: "openid profile w_member_social" });
    return res.redirect(url.toString());
}