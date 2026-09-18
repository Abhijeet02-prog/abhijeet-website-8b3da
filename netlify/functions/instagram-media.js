// GET /api/instagram-media?account=music|writing
// Returns posts for the requested Instagram account.
//
// Instagram's API has no concept of "pinned" posts — that flag only exists
// inside the Instagram app itself, so there's no way to read it automatically.
// To still show chosen posts at the top, featured-posts.json lets Abhijeet list
// specific post URLs per account. If that list is non-empty, those exact posts
// are looked up and returned (in the order listed). If it's empty, this falls
// back to the true latest posts, refreshed on every page load — same as before.
import { getStore } from "@netlify/blobs";
import featuredPosts from "./featured-posts.json";

const ACCOUNTS = ["music", "writing"];
const DEFAULT_LIMIT = 3;
const FIELDS = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp";

export default async (req) => {
  const url = new URL(req.url);
  const account = url.searchParams.get("account");

  if (!ACCOUNTS.includes(account)) {
    return json({ error: "invalid_account" }, 400);
  }

  const store = getStore("instagram-tokens");
  const tokenData = await store.get(account, { type: "json" });

  if (!tokenData || !tokenData.access_token) {
    // Not connected yet — the site's own fallback UI handles this gracefully.
    return json({ connected: false, items: [] }, 200);
  }

  const featuredShortcodes = ((featuredPosts && featuredPosts[account]) || [])
    .map(extractShortcode)
    .filter(Boolean);

  try {
    if (featuredShortcodes.length) {
      const items = await findFeatured(tokenData.access_token, featuredShortcodes);
      if (items.length) {
        return json({ connected: true, items }, 200, "public, max-age=600");
      }
      // None of the featured posts were found (e.g. deleted, or not in recent
      // history) — fall through to latest posts rather than showing nothing.
    }

    const igUrl = `https://graph.instagram.com/me/media?fields=${FIELDS}&access_token=${encodeURIComponent(tokenData.access_token)}&limit=${DEFAULT_LIMIT}`;
    const igRes = await fetch(igUrl);
    const igJson = await igRes.json();

    if (igJson.error) {
      return json({ connected: true, error: "ig_api_error", detail: igJson.error }, 200);
    }

    return json({ connected: true, items: igJson.data || [] }, 200, "public, max-age=600");
  } catch (err) {
    return json({ connected: true, error: "fetch_failed", detail: String(err) }, 200);
  }
};

// Pulls the shortcode (the id-looking part of the URL) out of a full Instagram
// post/reel URL, e.g. "https://www.instagram.com/p/ABC123/" -> "ABC123".
function extractShortcode(urlStr) {
  const m = String(urlStr || "").match(/instagram\.com\/(?:p|reel|tv)\/([^/?#]+)/i);
  return m ? m[1] : null;
}

// Searches the account's media, paging back through history if needed, for the
// requested shortcodes — and returns them in the order featured-posts.json listed
// them in. Stops once every requested post has been found, or after a few pages.
async function findFeatured(accessToken, shortcodes) {
  const found = new Map();
  let nextUrl = `https://graph.instagram.com/me/media?fields=${FIELDS}&access_token=${encodeURIComponent(accessToken)}&limit=50`;
  let pages = 0;

  while (nextUrl && found.size < shortcodes.length && pages < 4) {
    const res = await fetch(nextUrl);
    const data = await res.json();
    if (data.error) break;

    for (const item of data.data || []) {
      const code = extractShortcode(item.permalink);
      if (code && shortcodes.includes(code) && !found.has(code)) {
        found.set(code, item);
      }
    }

    nextUrl = data.paging && data.paging.next ? data.paging.next : null;
    pages++;
  }

  return shortcodes.map((code) => found.get(code)).filter(Boolean);
}

function json(body, status, cacheControl) {
  const headers = { "Content-Type": "application/json" };
  if (cacheControl) headers["Cache-Control"] = cacheControl;
  return new Response(JSON.stringify(body), { status, headers });
}

export const config = { path: "/api/instagram-media" };
