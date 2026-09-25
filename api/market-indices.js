// Live Nifty 50 / Sensex / Bank Nifty data for the hero market ticker.
//
// Fetched here (server-side) rather than straight from the browser for two
// reasons: Yahoo Finance's chart endpoint doesn't send CORS headers for
// arbitrary origins, so a direct browser fetch would just fail; and putting
// our own Cache-Control layer in front of it means many visitors loading
// the site around the same time share one upstream request instead of each
// triggering a fresh one.
//
// This is Yahoo's public "chart" endpoint — undocumented/unofficial (the
// same one the popular yfinance Python library relies on), but free, with
// no API key or signup. Being unofficial, it can occasionally rate-limit
// or change shape without notice, which is why every symbol fetch below is
// wrapped in its own try/catch: one symbol failing returns null values for
// just that entry instead of taking down the whole ticker.

const SYMBOLS = [
    { symbol: "^NSEI", name: "NIFTY 50" },
    { symbol: "^BSESN", name: "SENSEX" },
    { symbol: "^NSEBANK", name: "BANK NIFTY" },
];

export default async function handler(req, res) {
    // TEMP DEBUG — inspect Yahoo's raw meta shape (regularMarketTime,
    // marketState, previousClose vs chartPreviousClose, etc.) to confirm
    // after-hours/holiday behavior before finalizing the fallback logic.
    // Remove this branch once confirmed.
    if (req.query?.debug) {
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(req.query.debug)}`;
        const upstream = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 (compatible; abhijeettoshniwal.com market-ticker/1.0)" } });
        const data = await upstream.json();
        return res.status(200).json(data?.chart?.result?.[0]?.meta || { error: "no_meta", raw: data });
    }

    const indices = await Promise.all(SYMBOLS.map(fetchQuote));
    const ok = indices.some((idx) => idx.price != null);

    // s-maxage lets Vercel's edge cache serve the same response to many
    // visitors for 30s instead of hitting Yahoo per page load; the ticker
    // itself polls this endpoint every 60s from the client.
    res
        .setHeader("Cache-Control", "public, max-age=0, s-maxage=30, stale-while-revalidate=60")
        .status(200)
        .json({ updatedAt: new Date().toISOString(), ok, indices });
}

async function fetchQuote({ symbol, name }) {
    try {
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}`;
        const upstream = await fetch(url, {
            headers: { "User-Agent": "Mozilla/5.0 (compatible; abhijeettoshniwal.com market-ticker/1.0)" },
        });
        if (!upstream.ok) throw new Error(`upstream_${upstream.status}`);

        const data = await upstream.json();
        const meta = data?.chart?.result?.[0]?.meta;
        if (!meta || meta.regularMarketPrice == null) throw new Error("no_meta");

        const price = meta.regularMarketPrice;
        const prevClose = meta.previousClose ?? meta.chartPreviousClose ?? null;
        const change = prevClose != null ? price - prevClose : null;
        const changePercent = prevClose ? (change / prevClose) * 100 : null;

        return { symbol, name, price, change, changePercent };
    } catch (err) {
        return { symbol, name, price: null, change: null, changePercent: null, error: String(err) };
    }
}
