import { Redis } from "@upstash/redis";

export default async function handler(req, res) {
    if (req.method !== "POST") return res.status(405).json({ error: "method_not_allowed" });
    const text = String(req.body?.text || "").trim();
    if (!text) return res.status(400).json({ error: "text_required" });
    const tokenData = await Redis.fromEnv().get("linkedin-token:primary");
    if (!tokenData?.access_token) return res.status(401).json({ error: "linkedin_not_connected" });
    try {
        const profileRes = await fetch("https://api.linkedin.com/v2/userinfo", { headers: { Authorization: `Bearer ${tokenData.access_token}` } });
        const profileData = await profileRes.json();
        if (!profileRes.ok || !profileData?.sub) return res.status(500).json({ error: "linkedin_profile_fetch_failed", detail: profileData });
        const postRes = await fetch("https://api.linkedin.com/v2/ugcPosts", { method: "POST", headers: { Authorization: `Bearer ${tokenData.access_token}`, "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0" }, body: JSON.stringify({ author: `urn:li:person:${profileData.sub}`, lifecycleState: "PUBLISHED", specificContent: { "com.linkedin.ugc.ShareContent": { shareCommentary: { text }, shareMediaCategory: "NONE" } }, visibility: { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" } }) });
        const detail = await postRes.text();
        return res.status(postRes.ok ? 200 : 500).json(postRes.ok ? { success: true, detail } : { error: "linkedin_post_failed", detail });
    } catch (err) { return res.status(500).json({ error: "linkedin_post_exception", detail: String(err) }); }
}