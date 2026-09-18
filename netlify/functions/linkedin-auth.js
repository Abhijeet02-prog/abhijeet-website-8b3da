// GET /api/linkedin-auth
// Redirects the user to LinkedIn OAuth so they can authorize posting access.
export default async (req) => {
    const url = new URL(req.url);
    const state = url.searchParams.get("state") || "primary";

    const redirectUri = Netlify.env.get("LINKEDIN_REDIRECT_URI");
    const clientId = Netlify.env.get("LINKEDIN_CLIENT_ID");

    if (!redirectUri || !clientId) {
        return new Response(
            "<html><body><h1>LinkedIn not configured yet</h1><p>Set LINKEDIN_CLIENT_ID and LINKEDIN_REDIRECT_URI in the site env vars.</p></body></html>",
            { status: 500, headers: { "Content-Type": "text/html" } }
        );
    }

    const params = new URLSearchParams({
        response_type: "code",
        client_id: clientId,
        redirect_uri: redirectUri,
        state,
        scope: "openid profile w_member_social",
    });

    return Response.redirect(`https://www.linkedin.com/oauth/v2/authorization?${params.toString()}`, 302);
};

export const config = { path: "/api/linkedin-auth" };
