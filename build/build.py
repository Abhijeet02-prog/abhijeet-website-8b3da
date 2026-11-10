import json, os, html, datetime
from content import *

OUT = os.environ.get("OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
E = html.escape
TODAY = "2026-11-05"

def fmt_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"
def short_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"

PERSON = {
    "@type": "Person", "@id": SITE + "/#person", "name": NAME, "url": SITE + "/",
    "jobTitle": "Marketing Director",
    "worksFor": {"@type": "Organization", "name": "Aurangabad Pipes Pvt. Ltd.", "url": APPL_SITE},
    "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Goa Institute of Management"},
                 {"@type": "CollegeOrUniversity", "name": "Vellore Institute of Technology"}],
    "address": {"@type": "PostalAddress", "addressLocality": "Aurangabad", "addressRegion": "Maharashtra", "addressCountry": "IN"},
    "knowsAbout": ["B2B marketing", "Industrial marketing", "Growth marketing", "Business development", "Wealth management", "Indian markets and economy"],
    "sameAs": [LINKEDIN, IG_MUSIC, IG_WRITING],
}

THEME_JS = ("(function(){var d=document.documentElement;d.classList.add('js');var t=null;try{t=localStorage.getItem('theme')}catch(e){}"
            "if(t!=='light'&&t!=='dark'){t=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}"
            "d.setAttribute('data-theme',t)})();")

def head(title, desc, path, og, ld, og_type="website", extra=""):
    url = SITE + path
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<script>{THEME_JS}</script>
<link rel="preload" href="/assets/inter-400.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="/assets/lora-var.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v=4">
<script src="/assets/site.js?v=2" defer></script>
<meta name="theme-color" content="#f6f3ed" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#111316" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(title)}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
{extra}<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

NAV = [("/work", "Work"), ("/about", "About"), ("/insights", "Insights"), ("/contact", "Contact")]
SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6" stroke-linecap="round"/></svg>'
MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z" stroke-linejoin="round"/></svg>'
MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke-linecap="round"/></svg>'

def header(active):
    items = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f"""<header class="site-header">
  <div class="frame">
    <a class="wordmark" href="/" aria-label="{NAME}, home">Abhijeet Toshniwal<span>.</span></a>
    <nav class="nav" aria-label="Main">
      <ul class="nav-list" id="navList">{items}</ul>
      <button class="icon-btn theme-toggle" id="themeToggle" type="button" aria-label="Switch theme" aria-pressed="false">{SUN}{MOON}</button>
      <button class="icon-btn menu-btn" id="menuBtn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="navList">{MENU}</button>
    </nav>
  </div>
</header>
"""

def footer():
    return f"""<footer class="site-footer">
  <div class="frame">
    <div class="footer-grid">
      <div>
        <h2>{NAME}</h2>
        <p>Marketing Director at Aurangabad Pipes. Engineer by training, banker by experience, writer by habit. Based in Aurangabad, Maharashtra.</p>
      </div>
      <div>
        <h3>Site</h3>
        <ul><li><a href="/work">Work</a></li><li><a href="/about">About</a></li><li><a href="/insights">Insights</a></li><li><a href="/contact">Contact</a></li></ul>
      </div>
      <div>
        <h3>Elsewhere</h3>
        <ul>
          <li><a href="{LINKEDIN}" rel="me noopener" data-track="outbound_linkedin">LinkedIn</a></li>
          <li><a href="{IG_MUSIC}" rel="me noopener">Instagram: music</a></li>
          <li><a href="{IG_WRITING}" rel="me noopener">Instagram: thoughts</a></li>
          <li><a href="mailto:{EMAIL}" data-track="contact_email">Email</a></li>
        </ul>
      </div>
    </div>
    <p class="copyright">&copy; <span id="year">2026</span> {NAME}. Views in my writing are personal and are not investment advice.</p>
  </div>
</footer>
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "d9389966144748a5866dee89bfaa3f5b"}}' defer></script>
</body>
</html>
"""

def write(path, s):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)

def lens_block():
    steps = [("Signal", "A tanker is hit near Hormuz"), ("Currency", "The rupee feels it"), ("Prices", "Then inflation"),
             ("Costs", "Then what a factory pays for its inputs")]
    lenses = [
        ("together", "All three", "0,1,2,3", "One event, followed end to end",
         "From the strait to the shop floor to the customer's budget. Tracing that whole chain is what I write about every day, and what I bring to work."),
        ("engineer", "As an engineer", "3", "The last link: what it costs to make and ship",
         "Steel, energy and freight decide what a seamless tube costs to produce and deliver. The engineering question is where the process can absorb a shock and where it cannot."),
        ("banker", "As a banker", "1,2", "The middle links: currency and prices",
         "A weaker rupee and rising inflation change deposits, credit, forex needs and the value of a family's portfolio. At ICICI Bank this was the conversation behind every relationship."),
        ("marketer", "As a marketer", "2,3", "The buyer at the end of the chain",
         "When input costs and prices rise, the question is who still buys, at what price, and which message keeps their trust. That is my job at Aurangabad Pipes."),
    ]
    st = "".join(f'<li><div class="node"><span class="dot" aria-hidden="true"></span><span class="step">{a}</span></div><b>{b}</b></li>' for a, b in steps)
    tabs = "".join(f'<button type="button" id="lens-{k}" data-hits="{h}" aria-controls="note-{k}">{t}</button>' for k, t, h, _, _ in lenses)
    notes = "".join(f'<div class="lens-note" id="note-{k}" aria-labelledby="lens-{k}"><h3>{hd}</h3><p>{p}</p></div>' for k, _, _, hd, p in lenses)
    return f"""<div class="lens">
  <div class="lens-tabs" aria-label="Read the chain as">{tabs}</div>
  <ol class="chain" aria-label="How one event travels">{st}</ol>
  {notes}
  <p class="lens-source">The chain is how I explain my own work on LinkedIn: “When a tanker gets hit near Hormuz, it shows up in the rupee, then in inflation, then in what a factory pays for its inputs.” <a class="text-link" href="/insights/oil-flowing-again-why-118">Read one example</a></p>
</div>"""

def evidence_items():
    items = [
        ("₹750 Cr", "Relationship book across 10 ultra-high-net-worth families at ICICI Bank, 2026.", "Client assets managed, not owned", "/work#icici-bank"),
        ("5", "New-to-bank families brought in, typically with investable surplus above ₹100 Cr.", "ICICI Bank, Alipore Zone", "/work#icici-bank"),
        ("100", "MBA institutions mapped into a prioritised campus pipeline for EdgeX Academy.", "A pipeline, not signed partnerships", "/work#edgex-academy"),
        ("12% → 7%", "Supply-chain cost targeted by a rebuilt cost model for Reliance ResQ.", "A project target, not a realised result", "/work#reliance-resq"),
        ("8 hrs → 10 min", "Paint curing time targeted by a conveyor concept I designed at Disha Auto Components.", "A design target", "/work#disha-auto"),
        ("42+", "Import-export clients analysed for churn at ICICI Bank, with three fixes proposed.", "Internship, 2025", "/work#icici-internship"),
    ]
    return "".join(f'<div><b>{a}</b><p>{b} <a href="{l}" class="visually-hidden">Details: {E(b)}</a></p><span class="qual">{q}</span></div>' for a, b, q, l in items)

def post_row(a, external=False):
    if external:
        return (f'<li><a class="post" href="{li_post(a["urn"])}" rel="noopener" data-track="insight_linkedin"><time datetime="{a["date"]}">{short_date(a["date"])}</time>'
                f'<div><span class="tag">{a["topic"]}</span><span class="ext">On LinkedIn ↗</span><h3>{E(a["title"])}</h3><p>{E(a["summary"])}</p></div></a></li>')
    return (f'<li class="post-row"><div class="post-meta"><time datetime="{a["date"]}">{short_date(a["date"])}</time>'
            f'<a class="li-link" href="{li_post(a["urn"])}" rel="noopener" data-track="insight_linkedin">LinkedIn \u2197<span class="visually-hidden">: the original post, {E(a["title"])}</span></a></div>'
            f'<a class="post" href="/insights/{a["slug"]}" data-track="insight_open"><span class="tag">{a["topic"]}</span><h3>{E(a["title"])}</h3><p>{E(a["summary"])}</p></a></li>')

def media_block(all_three=False):
    vids = [("keyboard", "Keyboard, playing at home"), ("flute", "Flute, on stage"), ("the-artistic-room", "The artistic room: guitar and keys")]
    out = []
    for slug, label in vids:
        out.append(f"""<figure class="media">
  <div class="frame-v">
    <img src="/assets/reels/posters/{slug}.webp" width="360" height="640" loading="lazy" decoding="async" alt="{E(label)}: a still from Abhijeet's music video">
    <button class="play" type="button" data-src="/assets/reels/{slug}.mp4" data-poster="/assets/reels/posters/{slug}.webp" data-label="{E(label)}"><span><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg>Play video<span class="visually-hidden">: {E(label)}</span></span></button>
  </div>
  <figcaption>{E(label)}</figcaption>
</figure>""")
    return f'<div class="media-grid{" all" if all_three else ""}">' + "".join(out) + "</div>"

# ---------------------------------------------------------------- HOME
def page_home():
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME, "inLanguage": "en-IN", "publisher": {"@id": SITE + "/#person"}},
        PERSON]}
    latest = "".join(post_row(a) for a in ARTICLES[:3])
    h = head(f"{NAME}: Marketing Director, Aurangabad Pipes",
             "Abhijeet Toshniwal is a mechanical engineer and former ICICI Bank family office specialist who now leads marketing at Aurangabad Pipes. Selected work, writing on markets and the economy, and how to get in touch.",
             "/", "og-home.png", ld)
    body = f"""{header("/")}
<main id="main">
<section class="hero" id="top" aria-labelledby="hero-title">
  <div class="frame hero-grid">
    <div>
      <p class="eyebrow">Aurangabad, Maharashtra</p>
      <h1 id="hero-title">Abhijeet Toshniwal</h1>
      <p class="role"><span class="live-dot" aria-hidden="true"></span><a href="/work#aurangabad-pipes">Marketing Director, Aurangabad Pipes Pvt. Ltd.</a><span class="visually-hidden">, current role since November 2026</span></p>
      <p class="lead">I connect how products are made, how money moves and how buyers decide. Trained as a mechanical engineer and shaped by private banking at ICICI Bank, I now take a seamless tube maker with more than 25 years in the industry to new customers in India and abroad.</p>
      <div class="actions">
        <a class="btn btn-primary" href="/work" data-track="cta_work">See selected work</a>
        <a class="btn" href="/contact" data-track="cta_contact_hero">Start a conversation</a>
      </div>
    </div>
    <aside class="hero-aside" aria-label="Career path and reach">
      <ol class="journey">
        <li><span class="n">01</span><div><b>Engineer</b><span>Mechanical engineering, VIT · R&amp;D on a shop floor</span></div></li>
        <li><span class="n">02</span><div><b>Banker</b><span>Family office, ICICI Bank · 10 UHNW families</span></div></li>
        <li class="now"><span class="n">03</span><div><b>Marketer</b><span>Aurangabad Pipes · EdgeX Academy</span></div></li>
      </ol>
      <ul class="facts">
        <li><b id="statFollowers">{STATS["followers"]}</b><span>LinkedIn followers</span></li>
        <li><b id="statImpressions">{STATS["impressions"]}</b><span>post impressions</span></li>
        <li><b>Daily</b><span><a href="/insights">writing on markets and the economy</a></span></li>
      </ul>
    </aside>
  </div>
</section>

<section class="section" id="work" aria-labelledby="h-useful">
  <div class="frame section-grid">
    <p class="section-label">Where I am useful</p>
    <div class="section-body">
      <h2 id="h-useful">Three problems I work on</h2>
      <ol class="problems">
        <li><div><h3>Taking an industrial product to new buyers</h3><p>Positioning, outreach and brand for engineered products sold to OEMs, EPC projects and plants, in India and overseas.</p></div><a class="text-link arrow" href="/work#aurangabad-pipes">Current role</a></li>
        <li><div><h3>Building a channel, not just a deal</h3><p>Campus and institutional partnerships, referral and ambassador programmes, and a pipeline ranked by where to go first.</p></div><a class="text-link arrow" href="/work#edgex-academy">EdgeX Academy</a></li>
        <li><div><h3>Making money decisions clearer</h3><p>Deposits, credit, trade, forex and investments for families with complex needs, and cost models that hold up on the shop floor.</p></div><a class="text-link arrow" href="/work#icici-bank">ICICI Bank</a></li>
      </ol>
    </div>
  </div>
</section>

<section class="section" id="experience" aria-labelledby="h-evidence">
  <div class="frame section-grid">
    <p class="section-label">Evidence</p>
    <div class="section-body">
      <h2 id="h-evidence">What the numbers actually say</h2>
      <p class="section-intro">Each figure carries its qualifier. A pipeline is not a partnership, and a target is not a result.</p>
      <div class="evidence">{evidence_items()}</div>
      <p style="margin-top:24px"><a class="text-link arrow" href="/work">All work, with context and my role</a></p>
    </div>
  </div>
</section>

<section class="section" id="story" aria-labelledby="h-lens">
  <div class="frame section-grid">
    <p class="section-label">How I think</p>
    <div class="section-body">
      <h2 id="h-lens">One signal, three readings</h2>
      <p class="section-intro">I am most useful when I join dots that other people treat as separate. Here is one chain, read the way each part of my career taught me to read it.</p>
      {lens_block()}
    </div>
  </div>
</section>

<section class="section" id="news" aria-labelledby="h-latest">
  <div class="frame section-grid">
    <p class="section-label">Latest writing</p>
    <div class="section-body">
      <h2 id="h-latest">My take on the news</h2>
      <p class="section-intro">News moves fast. Most days I trace what it means for markets, money and business: oil, gold, IPOs, the RBI, banking, crypto, geopolitics and, now and then, sport. Each piece first appeared on LinkedIn.</p>
      <ul class="posts">{latest}</ul>
      <p style="margin-top:24px"><a class="text-link arrow" href="/insights">All insights</a> <span class="note">&nbsp;·&nbsp; A separate daily briefing of other publishers' headlines refreshes at 11:00 AM IST.</span></p>
    </div>
  </div>
</section>

<section class="section" id="profile" aria-labelledby="h-person">
  <div class="frame section-grid">
    <p class="section-label">Beyond work</p>
    <div class="section-body">
      <div class="split">
        <div id="music">
          <h2 id="h-person">Music keeps the timing honest</h2>
          <p>I play 12+ instruments, mostly keys, flute and strings. At Goa Institute of Management I led the official band across 15+ campus events. Music is where I practise what client work quietly depends on: patience, timing, and knowing what to leave out.</p>
          <p><a class="text-link arrow" href="/about#music">Watch and listen</a></p>
        </div>
        <div id="philosophy">
          <blockquote class="quote"><p>“{QUOTES[0]}”</p><cite>Abhijeet Toshniwal</cite></blockquote>
        </div>
      </div>
      <div style="margin-top:32px">{media_block()}</div>
    </div>
  </div>
</section>

<section class="section" id="contact" aria-labelledby="h-contact">
  <div class="frame section-grid">
    <p class="section-label">Contact</p>
    <div class="section-body">
      <h2 id="h-contact">Start the right conversation</h2>
      <p class="section-intro">Drop me a message. I reply.</p>
      <ul class="routes">
        <li><a href="/contact?topic=tubes" data-track="cta_route_tubes"><b>Sourcing seamless tubes</b><span>For boilers, heat exchangers, process piping, hydraulic, automotive or mechanical use.</span></a></li>
        <li><a href="/contact?topic=consulting" data-track="cta_route_consulting"><b>A growth or marketing problem</b><span>Positioning, go-to-market, partnerships and channels.</span></a></li>
        <li><a href="/contact?topic=students" data-track="cta_route_students"><b>Students and placements</b><span>Preparing for business careers, group discussions or interviews.</span></a></li>
        <li><a href="/contact?topic=writing" data-track="cta_route_writing"><b>Something I wrote</b><span>Think I got my last post wrong? Tell me.</span></a></li>
      </ul>
    </div>
  </div>
</section>
</main>
{footer()}"""
    write("index.html", h + body)

# ---------------------------------------------------------------- WORK
def role_entry(r):
    badge = '<span class="badge">Current</span>' if r["current"] else ""
    ctx = "".join(f"<p>{E(c)}</p>" for c in r["context"])
    acts = "".join(f"<li>{E(a)}</li>" for a in r["role"])
    extra = ""
    if r["id"] == "aurangabad-pipes":
        extra = f'<dt>Links</dt><dd><a class="text-link" href="{APPL_SITE}" rel="noopener">aurangabadpipes.com</a> &nbsp;·&nbsp; <a class="text-link" href="{li_post(COMPANY_POSTS[0]["urn"])}" rel="noopener">Launch post on LinkedIn</a> &nbsp;·&nbsp; <a class="text-link" href="/contact?topic=tubes" data-track="cta_route_tubes">Sourcing tubes? Talk to me</a></dd>'
    if r["id"] == "edgex-academy":
        extra = '<dt>Next step</dt><dd><a class="text-link" href="/contact?topic=students" data-track="cta_route_students">Students: ask about placements or GD practice</a></dd>'
    if r["id"] == "icici-bank":
        extra = '<dt>Next step</dt><dd><a class="text-link" href="/contact?topic=consulting" data-track="cta_route_consulting">Discuss a growth or money question</a></dd>'
    return f"""<article class="entry" id="{r["id"]}" aria-labelledby="t-{r["id"]}">
  <div class="entry-head">
    <h2 id="t-{r["id"]}">{E(r["title"])}{badge}</h2>
    <p class="entry-meta"><span class="entry-org">{E(r["org"])}</span> · {E(r["when"])} · {E(r["kind"])}</p>
  </div>
  <dl class="car">
    <dt>Problem</dt><dd>{E(r["problem"])}</dd>
    <dt>Context</dt><dd>{ctx}</dd>
    <dt>My role</dt><dd><ul>{acts}</ul></dd>
    <dt>Result or target</dt><dd>{E(r["result"])} <span class="qual">{E(r["qualifier"])}</span></dd>
    <dt>Skills</dt><dd><ul class="chips">{"".join(f"<li>{E(s)}</li>" for s in r["skills"])}</ul></dd>
    {extra}
  </dl>
</article>"""

def page_work():
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": SITE + "/work#webpage", "url": SITE + "/work", "name": f"Work | {NAME}", "about": {"@id": SITE + "/#person"}, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Work", "item": SITE + "/work"}]}]}
    h = head(f"Work | {NAME}", "Selected work by Abhijeet Toshniwal, organised by problem: industrial marketing at Aurangabad Pipes, campus growth at EdgeX Academy, family office work at ICICI Bank, and engineering and supply-chain projects.", "/work", "og-work.png", ld)
    jump = "".join(f'<li><a href="#{r["id"]}">{E(r["org"])}{" (intern)" if r["id"]=="icici-internship" else ""}</a></li>' for r in ROLES)
    caps = [
        ("B2B and industrial marketing", "Positioning, brand and outreach for engineered products sold to OEMs, EPC projects and plants."),
        ("Growth strategy", "Choosing the market, the channel and the first move, then turning it into a plan a team can repeat."),
        ("Partnerships", "Institutional and B2B partnerships that open a whole channel, not just a single deal."),
        ("Client relationships", "High-trust relationships with founders and families, coordinated across every specialist team they need."),
        ("Finance and wealth", "Deposits, credit, trade, forex and investments, with the judgement to make money decisions clearer."),
        ("Cost and operations", "Cost models and process changes that hold up on a spreadsheet and on the shop floor."),
        ("Brand and storytelling", "Positioning, voice and narrative that make a business easier to understand and remember."),
    ]
    approach = [("Understand the real problem", "I start by listening closely and separating signal from noise, so the real challenge becomes clear."),
                ("Define the sharp move", "Whether it is positioning, go-to-market or a system change, I focus people on the action that creates leverage."),
                ("Build what lasts", "Good decisions scale when the process behind them is simple, repeatable and aligned with the bigger goal.")]
    body = f"""{header("/work")}
<main id="main">
<div class="frame page-head">
  <p class="eyebrow">Work</p>
  <h1>Selected work, organised by the problem it solved</h1>
  <p class="section-intro">Each entry separates what I did from what was a target, a proposal or a pipeline. Two roles are current; the rest are earlier jobs, internships and projects.</p>
  <ul class="anchor-nav" aria-label="Jump to">{jump}</ul>
</div>
<div class="frame">{"".join(role_entry(r) for r in ROLES)}</div>

<section class="section" aria-labelledby="h-caps">
  <div class="frame section-grid">
    <p class="section-label">Capabilities</p>
    <div class="section-body">
      <h2 id="h-caps">What carries across roles</h2>
      <ul class="def-list cols-2">{"".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a, b in caps)}</ul>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="h-approach">
  <div class="frame section-grid">
    <p class="section-label">Approach</p>
    <div class="section-body">
      <h2 id="h-approach">How I approach a problem</h2>
      <ol class="problems">{"".join(f"<li><div><h3>{E(a)}</h3><p>{E(b)}</p></div></li>" for a, b in approach)}</ol>
      <p style="margin-top:20px" class="note">Services I offer: {", ".join(SERVICES)}.</p>
      <div class="actions" style="margin-top:20px"><a class="btn btn-primary" href="/contact?topic=consulting" data-track="cta_contact_work">Discuss a growth problem</a><a class="btn" href="/about">About me</a></div>
    </div>
  </div>
</section>
</main>
{footer()}"""
    write("work.html", h + body)

# ---------------------------------------------------------------- ABOUT
def page_about():
    ld = {"@context": "https://schema.org", "@type": "ProfilePage", "@id": SITE + "/about#webpage", "url": SITE + "/about",
          "name": f"About {NAME}", "dateModified": TODAY, "mainEntity": PERSON}
    h = head(f"About | {NAME}", "Abhijeet Toshniwal's story, from mechanical engineering and the shop floor to private banking at ICICI Bank and marketing at Aurangabad Pipes. Education, certifications, skills and music.", "/about", "og-about.png", ld, og_type="profile")
    tl = "".join(f'<li><span class="when">{E(r["when"])}</span><div><b>{E(r["title"])}</b> · <span class="org">{E(r["org"])}</span><p>{E(r["kind"])}. <a href="/work#{r["id"]}">Details</a></p></div></li>' for r in ROLES)
    edu = "".join(f'<li><span class="when">{a}</span><div><b>{E(b)}</b><p>{E(c)}{(" " + E(d)) if d else ""}</p></div></li>' for a, b, c, d in EDUCATION)
    certs = "".join(f'<li><b>{E(t)}</b><span>{E(i)} · {E(w)}</span></li>' for i, t, w in CERTS)
    body = f"""{header("/about")}
<main id="main">
<div class="frame page-head">
  <p class="eyebrow">About</p>
  <h1>Engineer, then banker, now marketer</h1>
  <p class="section-intro">He/Him · Aurangabad, Maharashtra</p>
  <ul class="anchor-nav" aria-label="On this page"><li><a href="#about">Story</a></li><li><a href="#experience">Career</a></li><li><a href="#education">Education</a></li><li><a href="#certifications">Certifications</a></li><li><a href="#skills">Skills</a></li><li><a href="#music">Music</a></li></ul>
</div>

<section class="section" id="about" aria-labelledby="h-story" style="border-top:0;padding-top:8px">
  <div class="frame section-grid">
    <p class="section-label">Story</p>
    <div class="section-body prose">
      <h2 id="h-story" class="visually-hidden">My story</h2>
      <p>I'm an engineer who became a banker who became a marketer. Somewhere along the way I realised I'm most useful when I'm joining dots that other people treat as separate.</p>
      <p>I grew up in a business environment, close to manufacturing companies such as Disha Auto Components and Aurangabad Pipes. That is where I first saw how a shop floor, a balance sheet and long-standing customer relationships hold a company together, and where I did my first real work as an engineer.</p>
      <p>I studied mechanical engineering at VIT Vellore, then marketing and finance at Goa Institute of Management. As an R&amp;D intern at Disha Auto Components I watched parts go from a drawing to a machine to a customer. Then came ICICI Bank: a sales and marketing internship in Mumbai, and later Kolkata, as a Family Office Specialist across 28 branches in the Alipore Zone, looking after the money of families who don't hand out trust easily.</p>
      <p>Today I'm the Marketing Director at Aurangabad Pipes Pvt. Ltd. We make seamless steel tubes and pipes, hot-finished and cold-drawn, in carbon and alloy steel. My job is easy to say and hard to do: get more people in India and abroad to know us, trust us and buy from us. On the side, I help EdgeX Academy grow, mostly by building campus partnerships.</p>
      <p>Most days I write about oil, gold, IPOs, the RBI, banking, crypto, geopolitics and, now and then, sport. People ask why I don't pick a lane. I don't see separate lanes. When a tanker gets hit near Hormuz, it shows up in the rupee, then in inflation, then in what a factory pays for its inputs. I like tracing that chain and putting it in plain words.</p>
      <p>Different cities, different rooms, one lesson: people buy from people they trust.</p>
    </div>
  </div>
</section>

<section class="section" id="experience" aria-labelledby="h-career">
  <div class="frame section-grid">
    <p class="section-label">Career</p>
    <div class="section-body"><h2 id="h-career">Roles and projects</h2><ol class="timeline">{tl}</ol></div>
  </div>
</section>

<section class="section" id="education" aria-labelledby="h-edu">
  <div class="frame section-grid">
    <p class="section-label">Education</p>
    <div class="section-body"><h2 id="h-edu">Education</h2><ol class="timeline">{edu}</ol></div>
  </div>
</section>

<section class="section" id="certifications" aria-labelledby="h-certs">
  <div class="frame section-grid">
    <p class="section-label">Certifications</p>
    <div class="section-body"><h2 id="h-certs">Licences and certifications</h2><ul class="def-list cols-2">{certs}</ul></div>
  </div>
</section>

<section class="section" id="skills" aria-labelledby="h-skills">
  <div class="frame section-grid">
    <p class="section-label">Skills</p>
    <div class="section-body">
      <h2 id="h-skills">Skills and services</h2>
      <h3 class="eyebrow" style="margin-top:8px">Top skills</h3>
      <ul class="chips top">{"".join(f"<li>{E(s)}</li>" for s in TOP_SKILLS)}</ul>
      <h3 class="eyebrow" style="margin-top:24px">Also</h3>
      <ul class="chips">{"".join(f"<li>{E(s)}</li>" for s in MORE_SKILLS)}</ul>
      <h3 class="eyebrow" style="margin-top:24px">Services</h3>
      <ul class="chips">{"".join(f"<li>{E(s)}</li>" for s in SERVICES)}</ul>
    </div>
  </div>
</section>

<section class="section" id="music" aria-labelledby="h-music">
  <div class="frame section-grid">
    <p class="section-label">Music</p>
    <div class="section-body">
      <h2 id="h-music">12+ instruments, one habit of practice</h2>
      <p class="section-intro">Keys, flute and strings. At GIM I led the official band across 15+ campus events. Off the clock, music is where I practise patience, timing and knowing what to leave out.</p>
      {media_block(True)}
      <p style="margin-top:20px"><a class="text-link" href="{IG_MUSIC}" rel="me noopener">More on Instagram: @abhijeet.acoustic02</a></p>
    </div>
  </div>
</section>

<section class="section" id="writing" aria-labelledby="h-words">
  <div class="frame section-grid">
    <p class="section-label">In my own words</p>
    <div class="section-body">
      <h2 id="h-words" class="visually-hidden">Two thoughts I keep coming back to</h2>
      <div class="cols-2" style="gap:32px 40px">{"".join(f'<blockquote class="quote"><p>“{E(q)}”</p><cite>Abhijeet Toshniwal</cite></blockquote>' for q in QUOTES)}</div>
      <p style="margin-top:24px"><a class="text-link arrow" href="/insights">Read my analysis</a> &nbsp; <a class="text-link" href="{IG_WRITING}" rel="me noopener">More thoughts on Instagram: @thoughts_at_02</a></p>
    </div>
  </div>
</section>

<section class="section" id="connect" aria-labelledby="h-connect">
  <div class="frame section-grid">
    <p class="section-label">Connect</p>
    <div class="section-body">
      <h2 id="h-connect">Looking for seamless tubes? Preparing for placements? Or think I got my last post wrong?</h2>
      <p class="section-intro">Drop me a message. I reply.</p>
      <div class="actions"><a class="btn btn-primary" href="/contact" data-track="cta_contact_about">Send a message</a><a class="btn" href="{LINKEDIN}" rel="me noopener" data-track="outbound_linkedin">Connect on LinkedIn</a></div>
    </div>
  </div>
</section>
</main>
{footer()}"""
    write("about.html", h + body)

# ---------------------------------------------------------------- INSIGHTS
def page_insights():
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/insights/{a['slug']}", "name": a["title"]} for i, a in enumerate(ARTICLES)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": SITE + "/insights#webpage", "url": SITE + "/insights", "name": f"Insights | {NAME}", "author": {"@id": SITE + "/#person"}},
        {"@type": "ItemList", "itemListElement": items}]}
    h = head(f"Insights | {NAME}", "Abhijeet Toshniwal's analysis of markets, the economy, policy and business, plus a clearly separate daily briefing of other publishers' headlines and a delayed market snapshot.", "/insights", "og-insights.png", ld)
    own = "".join(post_row(a) for a in ARTICLES)
    more = "".join(post_row(a, True) for a in MORE_POSTS)
    sk = '<div class="brief-topic"><h4>{t}</h4><span class="sk"></span><span class="sk w70"></span></div>'
    body = f"""{header("/insights")}
<main id="main">
<div class="frame page-head">
  <p class="eyebrow">Insights</p>
  <h1>Markets, economy and business, traced end to end</h1>
  <p class="section-intro">My reading of the news comes first. Below it, kept separate, is an automatic briefing of other publishers' headlines and a delayed market snapshot.</p>
  <ul class="anchor-nav" aria-label="On this page"><li><a href="#analysis">My take on the news</a></li><li><a href="#more">More on LinkedIn</a></li><li><a href="#briefing">Daily briefing</a></li><li><a href="#markets">Market snapshot</a></li></ul>
</div>

<section class="section" id="analysis" aria-labelledby="h-analysis" style="border-top:0;padding-top:8px">
  <div class="frame section-grid">
    <p class="section-label">My take</p>
    <div class="section-body">
      <h2 id="h-analysis">My take on the news</h2>
      <p class="section-intro">News moves fast. I trace what it means for markets, money and business. Each piece first appeared on LinkedIn, and the reporting it builds on is credited at the end. Views are personal and are not investment advice.</p>
      <ul class="posts">{own}</ul>
    </div>
  </div>
</section>

<section class="section" id="more" aria-labelledby="h-more">
  <div class="frame section-grid">
    <p class="section-label">More posts</p>
    <div class="section-body">
      <h2 id="h-more">More of my posts, on LinkedIn</h2>
      <ul class="posts">{more}</ul>
      <p style="margin-top:20px"><a class="text-link" href="{LINKEDIN_ACTIVITY}" rel="noopener">All my recent activity on LinkedIn</a></p>
    </div>
  </div>
</section>

<section class="section" id="briefing" aria-labelledby="h-brief">
  <div class="frame section-grid">
    <p class="section-label">Daily briefing</p>
    <div class="section-body">
      <h2 id="h-brief">Today's headlines from other publishers</h2>
      <p class="section-intro">Selected automatically from Indian and international business publishers each day at 11:00 AM IST. These are not my views, and placement here does not imply any link between stories. Each headline opens the original publisher.</p>
      <div class="panel" aria-live="polite">
        <div class="panel-head"><h3 id="briefingMeta">Loading today's edition</h3><span class="status" id="briefingStatus">Loading</span></div>
        <div class="brief-grid" id="briefingGrid">{"".join(sk.format(t=t) for t in ["Markets", "Policy", "Oil", "Economy"])}</div>
        <noscript><p class="note">The briefing needs JavaScript. My posts above do not.</p></noscript>
      </div>
    </div>
  </div>
</section>

<section class="section" id="markets" aria-labelledby="h-markets">
  <div class="frame section-grid">
    <p class="section-label">Market snapshot</p>
    <div class="section-body">
      <h2 id="h-markets">Indian indices, with their timestamps</h2>
      <div class="panel" aria-live="polite">
        <div class="panel-head"><h3>NIFTY 50, SENSEX, BANK NIFTY</h3><span class="status" id="marketStatus">Loading</span></div>
        <div class="table-scroll"><table class="quotes-table"><caption class="visually-hidden">Index levels and daily change</caption>
          <thead><tr><th scope="col">Index</th><th scope="col" class="num" style="text-align:right">Level</th><th scope="col" style="text-align:right">Day change</th></tr></thead>
          <tbody id="marketRows"><tr><td colspan="3"><span class="sk"></span></td></tr></tbody></table></div>
        <p class="note" id="marketMeta" style="margin:12px 0 0">Timestamps appear once quotes load.</p>
        <p class="note" style="margin:4px 0 0">Source: Yahoo Finance. Quotes can be delayed and are not live; outside market hours they show the last close. Not investment advice.</p>
      </div>
    </div>
  </div>
</section>
</main>
{footer()}"""
    write("insights.html", h + body)

# ---------------------------------------------------------------- ARTICLES
def render_body(blocks):
    out = []
    for kind, val in blocks:
        if kind == "p": out.append(f"<p>{E(val)}</p>")
        elif kind == "h2": out.append(f"<h2>{E(val)}</h2>")
        elif kind == "ul": out.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in val) + "</ul>")
        elif kind == "chain": out.append('<ol class="chain-text">' + "".join(f"<li>{'→ ' if i else ''}{E(x)}</li>" for i, x in enumerate(val)) + "</ol>")
        elif kind == "callout": out.append(f'<p class="callout">{E(val)}</p>')
        elif kind == "note": out.append(f'<p class="note">{E(val)}</p>')
        elif kind == "table":
            hd, rows = val[0], val[1:]
            out.append('<div class="table-scroll"><table><thead><tr>' + "".join(f'<th scope="col">{E(c)}</th>' for c in hd) + "</tr></thead><tbody>" +
                       "".join("<tr>" + "".join((f'<th scope="row">{E(c)}</th>' if j == 0 else f"<td>{E(c)}</td>") for j, c in enumerate(r)) + "</tr>" for r in rows) + "</tbody></table></div>")
    return "".join(out)

def page_article(i, a):
    url = f"{SITE}/insights/{a['slug']}"
    iso = f"{a['date']}T{a['time']}:00+05:30"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": a["title"], "description": a["summary"], "datePublished": iso, "dateModified": iso,
         "author": {"@type": "Person", "@id": SITE + "/#person", "name": NAME, "url": SITE + "/about"}, "publisher": {"@id": SITE + "/#person"},
         "mainEntityOfPage": url, "image": f"{SITE}/assets/og-{a['slug']}.png", "articleSection": a["topic"], "inLanguage": "en-IN",
         "isBasedOn": li_post(a["urn"])},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Insights", "item": SITE + "/insights"}, {"@type": "ListItem", "position": 2, "name": a["title"], "item": url}]}]}
    extra = f'<meta property="article:published_time" content="{iso}">\n<meta property="article:author" content="{SITE}/about">\n<meta property="article:section" content="{E(a["topic"])}">\n'
    h = head(f"{a['title']} | {NAME}", a["summary"], f"/insights/{a['slug']}", f"og-{a['slug']}.png", ld, og_type="article", extra=extra)
    prev_a = ARTICLES[i + 1] if i + 1 < len(ARTICLES) else None
    next_a = ARTICLES[i - 1] if i > 0 else None
    pager = '<nav class="pager" aria-label="More analysis">'
    pager += (f'<a class="text-link" href="/insights/{prev_a["slug"]}">← Older: {E(prev_a["title"])}</a>' if prev_a else "<span></span>")
    pager += (f'<a class="text-link" href="/insights/{next_a["slug"]}">Newer: {E(next_a["title"])} →</a>' if next_a else "")
    pager += "</nav>"
    body = f"""{header("/insights")}
<main id="main">
<article class="frame" aria-labelledby="a-title">
  <header class="article-head">
    <p class="eyebrow"><a href="/insights" style="text-decoration:none">Insights</a> · {E(a["topic"])}</p>
    <h1 id="a-title">{E(a["title"])}</h1>
    <p class="byline"><span>By <a href="/about">{NAME}</a></span><span>First published <a href="{li_post(a["urn"])}" rel="noopener" data-track="insight_linkedin">on LinkedIn</a>, <time datetime="{iso}">{fmt_date(a["date"])}</time></span></p>
  </header>
  <div class="prose">
    {render_body(a["body"])}
    <p class="note"><strong>Sources:</strong> {E(a["sources"])}</p>
    <p class="note">Views are personal. Not investment advice. Do your own research.</p>
    <div class="article-foot">
      <p style="margin:0">Have a view on this? <a class="text-link" href="{li_post(a["urn"])}" rel="noopener" data-track="insight_discuss">Join the discussion on LinkedIn</a> or <a class="text-link" href="/contact?topic=writing" data-track="cta_route_writing">write to me</a>.</p>
      {pager}
    </div>
  </div>
</article>
</main>
{footer()}"""
    write(f"insights/{a['slug']}.html", h + body)

# ---------------------------------------------------------------- CONTACT
def page_contact():
    ld = {"@context": "https://schema.org", "@type": "ContactPage", "@id": SITE + "/contact#webpage", "url": SITE + "/contact", "name": f"Contact {NAME}", "about": {"@id": SITE + "/#person"}}
    h = head(f"Contact | {NAME}", "Contact Abhijeet Toshniwal about sourcing seamless tubes from Aurangabad Pipes, a growth or marketing problem, students and placements, or something he wrote.", "/contact", "og-contact.png", ld)
    topics = [("tubes", "Sourcing seamless tubes (Aurangabad Pipes)"), ("consulting", "A growth, marketing or strategy problem"),
              ("partnership", "Partnership or collaboration"), ("students", "Students, placements and mentoring"),
              ("writing", "Something I wrote"), ("music", "Music"), ("general", "Something else")]
    opts = "".join(f'<option value="{v}">{E(t)}</option>' for v, t in topics)
    body = f"""{header("/contact")}
<main id="main">
<div class="frame page-head">
  <p class="eyebrow">Contact</p>
  <h1>Tell me what you're working on</h1>
  <p class="section-intro">Drop me a message. I read every one and reply personally.</p>
</div>
<section class="section" style="border-top:0;padding-top:0" aria-label="Contact form and other ways to reach me">
  <div class="frame">
    <div class="split">
      <form class="form" id="contactForm" action="https://formsubmit.co/{EMAIL}" method="POST" aria-describedby="formNote">
        <input type="hidden" name="_subject" value="New message from abhijeettoshniwal.com">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="source" value="">
        <div class="hp" aria-hidden="true"><label for="hpf">Leave this empty</label><input type="text" id="hpf" name="_honey" tabindex="-1" autocomplete="off"></div>
        <div class="field"><label for="topic">What is this about?</label>
          <select id="topic" name="topic">{opts}</select></div>
        <div class="field"><label for="name">Your name</label>
          <input type="text" id="name" name="name" autocomplete="name" required aria-describedby="name-err"><span class="err" id="name-err" hidden></span></div>
        <div class="field"><label for="email">Email</label>
          <input type="email" id="email" name="email" autocomplete="email" required aria-describedby="email-err"><span class="err" id="email-err" hidden></span></div>
        <div class="field"><label for="message">Message</label>
          <span class="hint" id="message-hint">A few lines on what you need is enough.</span>
          <textarea id="message" name="message" required minlength="10" aria-describedby="message-hint message-err"></textarea><span class="err" id="message-err" hidden></span></div>
        <div><button class="btn btn-primary" type="submit">Send message</button></div>
        <p class="note" id="formNote" style="margin:0">Your message goes to my inbox through FormSubmit. I use your email only to reply.</p>
        <div class="form-status" id="formStatus" role="status" tabindex="-1" hidden></div>
      </form>
      <aside aria-label="Other ways to reach me">
        <h2 style="font-size:var(--step-2)">Other ways to reach me</h2>
        <ul class="contact-alt">
          <li><span>Email</span><a href="mailto:{EMAIL}" data-track="contact_email">{EMAIL}</a></li>
          <li><span>LinkedIn</span><a href="{LINKEDIN}" rel="me noopener" data-track="outbound_linkedin">Abhijeet Toshniwal</a></li>
          <li><span>WhatsApp</span><a href="{WHATSAPP}" rel="noopener" data-track="contact_whatsapp">{WHATSAPP_DISPLAY}</a></li>
          <li><span>Aurangabad Pipes</span><a href="{APPL_SITE}" rel="noopener">aurangabadpipes.com</a></li>
        </ul>
      </aside>
    </div>
  </div>
</section>
</main>
{footer()}"""
    write("contact.html", h + body)

def page_404():
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Page not found"}
    h = head(f"Page not found | {NAME}", "This page does not exist or has moved.", "/404", "og-home.png", ld, extra='<meta name="robots" content="noindex">\n')
    body = f"""{header("")}
<main id="main">
<div class="frame page-head">
  <p class="eyebrow">404</p>
  <h1>This page has moved or never existed</h1>
  <p class="section-intro">The site was reorganised in November 2026. The old profile page is now About, and the news page is now Insights.</p>
  <ul class="anchor-nav"><li><a href="/">Home</a></li><li><a href="/work">Work</a></li><li><a href="/about">About</a></li><li><a href="/insights">Insights</a></li><li><a href="/contact">Contact</a></li></ul>
</div>
</main>
{footer()}"""
    write("404.html", h + body)

def sitemap():
    urls = [("/", "1.0"), ("/work", "0.9"), ("/about", "0.9"), ("/insights", "0.8"), ("/contact", "0.6")] + [(f"/insights/{a['slug']}", "0.7") for a in ARTICLES]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u, p in urls:
        x += f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n"
    write("sitemap.xml", x + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n")

page_home(); page_work(); page_about(); page_insights(); page_contact(); page_404()
for i, a in enumerate(ARTICLES): page_article(i, a)
sitemap()
print("built")
