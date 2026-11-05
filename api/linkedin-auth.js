export default function handler(req, res) {
    const { LINKEDIN_CLIENT_ID: clientId, LINKEDIN_REDIRECT_URI: redirectUri } = process.env;
    if (!clientId || !redirectUri) return res.status(500).send("Set LINKEDIN_CLIENT_ID and LINKEDIN_REDIRECT_URI.");
    const url = new URL("https://www.linkedin.com/oauth/v2/authorization");
    // ?for=stats asks for the analytics scopes (LinkedIn's Community
    // Management API product must be approved for the app first); the
    // default connection is the posting one.
    const forStats = new URL(req.url, "https://x").searchParams.get("for") === "stats";
    url.search = new URLSearchParams({
        response_type: "code", client_id: clientId, redirect_uri: redirectUri,
        state: forStats ? "stats" : "primary",
        scope: forStats ? "openid profile r_member_profileAnalytics r_member_postAnalytics" : "openid profile w_member_social",
    });
    return res.redirect(url.toString());
}