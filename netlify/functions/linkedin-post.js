// POST /api/linkedin-post
// Publishes a text-only LinkedIn post using the stored access token.
import { getStore } from "@netlify/blobs";

export default async (req) => {
    if (!req || !req.method || req.method !== "POST") {
        return json({ error: "method_not_allowed" }, 405);
    }

    let body;
    try {
        body = await req.json();
    } catch {
        return json({ error: "invalid_json" }, 400);
    }

    const text = String(body?.text || "").trim();
    if (!text) {
        return json({ error: "text_required" }, 400);
    }

    const store = getStore("linkedin-token");
    const tokenData = await store.get("primary", { type: "json" });

    if (!tokenData || !tokenData.access_token) {
        return json({ error: "linkedin_not_connected" }, 401);
    }

    try {
        const profileRes = await fetch("https://api.linkedin.com/v2/userinfo", {
            headers: { Authorization: `Bearer ${tokenData.access_token}` },
        });

        const profileData = await profileRes.json();
        if (!profileRes.ok || !profileData?.sub) {
            return json({ error: "linkedin_profile_fetch_failed", detail: profileData }, 500);
        }

        const payload = {
            author: `urn:li:person:${profileData.sub}`,
            lifecycleState: "PUBLISHED",
            specificContent: {
                "com.linkedin.ugc.ShareContent": {
                    shareCommentary: { text },
                    shareMediaCategory: "NONE",
                },
            },
            visibility: {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
            },
        };

        const postRes = await fetch("https://api.linkedin.com/v2/ugcPosts", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${tokenData.access_token}`,
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            },
            body: JSON.stringify(payload),
        });

        const postJson = await postRes.text();

        if (!postRes.ok) {
            return json({ error: "linkedin_post_failed", detail: postJson }, 500);
        }

        return json({ success: true, detail: postJson }, 200);
    } catch (err) {
        return json({ error: "linkedin_post_exception", detail: String(err) }, 500);
    }
};

function json(body, status) {
    return new Response(JSON.stringify(body), {
        status,
        headers: { "Content-Type": "application/json" },
    });
}

export const config = { path: "/api/linkedin-post" };
