# Single source of truth for the site's facts. Qualifiers are deliberate:
# a pipeline is not a partnership, a target is not a result, a project is not
# employment, a relationship book is not personally owned capital.

SITE = "https://www.abhijeettoshniwal.com"
NAME = "Abhijeet Toshniwal"
EMAIL = "abhijeettoshniwal14@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/abhijeet-toshniwal-aa3577292/"
LINKEDIN_ACTIVITY = "https://www.linkedin.com/in/abhijeet-toshniwal-aa3577292/recent-activity/all/"
IG_MUSIC = "https://www.instagram.com/abhijeet.acoustic02/"
IG_WRITING = "https://www.instagram.com/thoughts_at_02/"
WHATSAPP = "https://wa.me/918149441411?text=Hi%20Abhijeet%2C%20I%20found%20your%20website%20and%20wanted%20to%20connect."
WHATSAPP_DISPLAY = "+91 81494 41411"
APPL_SITE = "https://www.aurangabadpipes.com/"

def li_post(urn):
    return f"https://www.linkedin.com/feed/update/urn:li:activity:{urn}/"

STATS = {"followers": "3,700+", "impressions": "260k+"}

ROLES = [
    dict(id="aurangabad-pipes", title="Marketing Director", org="Aurangabad Pipes Pvt. Ltd.", when="Nov 2026 to present",
         kind="Full-time · On-site, Aurangabad, Maharashtra", current=True,
         problem="Take a seamless tube maker with more than 25 years in the industry to buyers who have not heard of it yet, in India and abroad.",
         context=["Aurangabad Pipes makes hot-finished and cold-drawn seamless steel tubes and pipes in carbon and alloy steel.",
                  "Its tubes go into boilers, heat exchangers, process piping, hydraulic cylinders, automobiles, machines and steel structures.",
                  "The company is ISO 9001:2015, IBR and PED certified. Every tube starts as a billet on its own hot mill, is checked in its own lab with eddy current and hydro tests, and carries a heat number for traceability."],
         role=["Marketing and new business, domestic and international.",
               "Making the brand look as good as the product already is, so OEMs, EPC projects and plants can find and trust it."],
         result="Started in November 2026. On 4 November 2026 the company website, aurangabadpipes.com, went live, a team effort I announced on LinkedIn. Commercial results will be added here as they are earned.",
         qualifier="New role: no results claimed yet",
         skills=["B2B marketing", "Go-to-market", "Business development", "Exports", "Brand"]),
    dict(id="edgex-academy", title="Growth Consultant", org="EdgeX Academy", when="Sep 2026 to present",
         kind="Part-time", current=True,
         problem="Decide where an EdTech company grows next, and build the campus channel to get there.",
         context=["EdgeX Academy is a Bengaluru-based EdTech team started by ISB and IIM alumni. It helps students and working professionals prepare for business careers.",
                  "One of its programmes, GD Labs, offers live group discussion practice with a real moderator and written feedback after every session."],
         role=["Mapped 100 MBA institutions into a prioritised outreach pipeline.",
               "Building the campus channel through partnerships with B-school clubs, placement teams and faculty.",
               "Designed the ambassador, referral and GD Labs programmes for campus acquisition.",
               "Shaping where to grow next, which campuses to partner with, and how the brand should come across."],
         result="A prioritised pipeline of 100 MBA institutions.",
         qualifier="A pipeline, not signed partnerships",
         skills=["Business growth", "Growth marketing", "Campus partnerships", "Brand"]),
    dict(id="icici-bank", title="Family Office Specialist", org="ICICI Bank", when="Apr 2026 to Sep 2026",
         kind="Full-time · On-site, Kolkata · Alipore Zone, 28 branches", current=False,
         problem="Look after the banking, investment and wealth needs of families who do not hand out trust easily.",
         context=["The Family Office desk for ICICI Bank's Alipore Zone in Kolkata, covering 28 branches."],
         role=["Managed 10 ultra-high-net-worth family relationships, a relationship book of ₹750 Cr.",
               "Brought in 5 new-to-bank families, typically with investable surplus above ₹100 Cr.",
               "Coordinated deposits, credit, trade, forex and investment solutions with branch teams and ICICI Securities.",
               "Family Office point of contact for 28 branches in the Alipore Zone."],
         result="₹750 Cr relationship book across 10 UHNW families; 5 new-to-bank families.",
         qualifier="Client assets managed, not personally owned",
         skills=["Wealth management", "Relationship management", "Finance"]),
    dict(id="icici-internship", title="Sales and Marketing Intern", org="ICICI Bank", when="Apr 2025 to Jun 2025",
         kind="Internship · On-site, Mumbai", current=False,
         problem="Understand why import-export clients drift away, and what would keep them.",
         context=["A summer internship with ICICI Bank in Mumbai, working with import-export clients."],
         role=["Analysed churn across 42+ import-export clients.",
               "Proposed three fixes to reduce regulatory pendency."],
         result="Three proposed fixes.",
         qualifier="Proposals, not implemented changes",
         skills=["Marketing", "Marketing strategy"]),
    dict(id="reliance-resq", title="Live project, Reliance ResQ", org="Reliance Retail", when="2024",
         kind="Project, not employment", current=False,
         problem="Bring down the cost of a service supply chain.",
         context=["A live project on Reliance ResQ, Reliance Retail's service arm."],
         role=["Rebuilt the supply-chain cost model around distribution-centre monetisation and centralised just-in-time inventory."],
         result="A cost model targeting a reduction in supply-chain cost from 12% to 7%.",
         qualifier="A modelled target, not a realised result",
         skills=["Supply chain", "Cost modelling"]),
    dict(id="disha-auto", title="Research and Development Engineer (Intern)", org="Disha Auto Components Pvt. Ltd.", when="Jan 2024 to May 2024",
         kind="Internship · On-site, Aurangabad", current=False,
         problem="Speed up a slow step on the production line.",
         context=["Watched parts go from a drawing to a machine to a customer, and learned how much care sits behind every piece that ships."],
         role=["Designed a conveyor concept to cut paint curing time from 8 hours to 10 minutes.",
               "Automated stencilling on the production line."],
         result="A conveyor concept aimed at cutting paint curing from 8 hours to 10 minutes; automated stencilling.",
         qualifier="The curing figure is a design target",
         skills=["Research and development", "CAD/CAM"]),
]

EDUCATION = [
    ("2024 to 2026", "Goa Institute of Management (GIM)", "PGDM, Marketing and Finance", "Led the official campus band across 15+ events."),
    ("2020 to 2024", "Vellore Institute of Technology", "B.Tech, Mechanical Engineering · CGPA 8.86", ""),
    ("2019 to 2020", "Vidyadham Junior College", "Class 12, Science · 87.38%", ""),
    ("2017 to 2018", "Maharashtra Public School", "Class 10 · 96.80%", ""),
]

CERTS = [
    ("LinkedIn", "Content and Creative Design Certification", "Issued Oct 2026 · valid to Oct 2028"),
    ("LinkedIn", "Marketing Measurement Certification", "Issued Oct 2026 · valid to Oct 2028"),
    ("National Institute of Securities Markets (NISM)", "NISM-Series-V-A: Mutual Fund Distributors", "Issued May 2026 · valid to May 2029"),
    ("Interactive Brokers", "Derivatives: Options and Futures", "Issued Oct 2024"),
    ("University of Pennsylvania", "Introduction to Marketing", "Issued Sep 2024"),
]

TOP_SKILLS = ["Business growth", "Business-to-business (B2B)", "Marketing", "Finance"]
MORE_SKILLS = ["Go-to-market strategy", "Business development", "Growth marketing", "Top-line growth", "B2B integration",
               "Marketing strategy", "Economic development", "Financial accounting", "Smart dashboards", "Research and development", "CAD/CAM"]
SERVICES = ["Marketing consulting", "Growth marketing", "Business consulting"]

QUOTES = [
    "Knowledge fills the mind, Logic creates the subject.",
    "My birth was celebrated within my family. I wish my death would be remembered by the world.",
]

# Original writing republished from LinkedIn (dates decoded from post IDs, IST).
ARTICLES = [
    dict(slug="foreign-money-korea-india", urn="7523572931361390592", date="2026-11-04", time="08:02",
         title="Why foreign money sold Korea and bought India on the same day", topic="Markets",
         summary="AI-spending doubts pushed funds out of chip-heavy Korea. India's lack of an AI hardware story suddenly looked like a hedge.",
         body=[
            ("p", "On Tuesday, foreign investors sold 1.52 trillion of Korean stocks. The same day, they bought ₹6,837 crore of Indian ones. Same money. Opposite directions. Here's why."),
            ("p", "On 3 November the KOSPI fell 3.6%. Samsung and SK hynix, the memory-chip giants riding the AI boom, dropped 4 to 5%."),
            ("p", "The trigger? Growing unease about how US Big Tech is paying for its AI build-out. Oracle alone is raising $20 billion through stock and bonds."),
            ("p", "Mumbai, same day: Nifty up 1.6%, Sensex up 1,225 points, a fourth straight gain. FIIs posted their biggest single-day buying since October 2025. FMCG led, not tech."),
            ("h2", "How I connect the dots"),
            ("chain", ["AI spending doubts", "money exits chip-heavy markets like Korea", "funds look for growth that doesn't depend on AI hardware", "India's mix (banks, consumption, autos) suddenly looks like a hedge", "FII inflows support large caps and the rupee (~94.7/$)"]),
            ("p", "For two years India was under-owned partly because it had no AI chip story. That same gap is now the attraction. Easing crude and decent Q2 earnings helped too."),
            ("p", "But two good days are not a trend. Analysts are calling these early signs, not a reversal. If oil spikes again or the AI trade bounces back, this money can turn just as fast."),
            ("callout", "Takeaway: in global markets, what you don't own matters as much as what you do."),
            ("p", "Is India's “no-AI” profile a strength or a blind spot?"),
         ],
         sources="Business Standard, 3 Nov 2026; Seoul Economic Daily and Aju Press, 3 Nov 2026; HDFC Sky market close, 3 Nov 2026; IANS, 1 Nov 2026."),
    dict(slug="sebi-zero-tax-pitch-foreign-investors", urn="7523280194212626433", date="2026-11-03", time="12:39",
         title="Sebi's zero-tax pitch to bring foreign investors back", topic="Policy",
         summary="Scrapping long-term capital gains tax for foreign portfolio investors would lift their returns. It would also cost revenue and start a fairness debate.",
         body=[
            ("p", "Foreign investors have pulled a record ~$31 billion out of Indian stocks in 2026. Now the market regulator is pitching a zero-tax fix."),
            ("p", "Picture a fund manager in Singapore. She can buy Taiwan's chip stocks, Korea's AI plays, or India."),
            ("p", "On Indian shares held over a year, she pays 12.5% long-term capital gains (LTCG) tax. If she sells within a year, it's 20%."),
            ("p", "On Monday, Reuters reported that Sebi has recommended, in its pre-Budget wishlist, that the government scrap LTCG tax for foreign portfolio investors (FPIs). It also wants switches between mutual fund schemes (units held 1+ year) not to count as a taxable sale."),
            ("h2", "How I connect the dots"),
            ("chain", ["No LTCG", "foreign investors' returns rise by ~2.3 percentage points (IIFL estimate)", "India looks better against other emerging markets on an after-tax basis", "more dollars could come back, supporting the rupee and the large caps FPIs own most", "but the government gives up revenue: equity LTCG brought in ₹1.3 trillion in FY25"]),
            ("p", "Markets noticed. LTCG hopes were one of the reasons cited as the Sensex jumped 1,233 points on Monday."),
            ("callout", "A tax cut opens the door, but earnings growth is what brings money in. And there's a fairness test coming. If a foreign fund pays 0% while an Indian SIP investor pays 12.5%, expect a loud debate before the Budget in February."),
            ("p", "For now it's a proposal, and it isn't binding. The government decides."),
            ("p", "Should India scrap LTCG for foreigners only, for everyone, or not at all?"),
         ],
         sources="Reuters via Business Standard, 2 Nov 2026; Business Today, 2 Nov 2026; Tribune/ANI, 2 Nov 2026."),
    dict(slug="october-gst-festive-demand", urn="7522869753942659074", date="2026-11-02", time="09:28",
         title="October's GST: India wants to spend. Can it keep spending?", topic="Economy",
         summary="Record October GST and record car sales show festive demand. Domestic GST is the cleaner signal; the import figure is partly a weaker rupee.",
         body=[
            ("p", "₹2.31 lakh crore. That's how much GST India collected in October 2026. It's up 22.9% from a year ago."),
            ("p", "Picture a car showroom this Navratri and Dussehra season: families booking SUVs so they can drive home before Diwali. The numbers match that picture:"),
            ("ul", ["Maruti Suzuki: highest-ever monthly domestic sales, up 20%", "Hyundai: a record month, up 16.7%", "Tata Motors (passenger vehicles): up 21%"]),
            ("h2", "How I connect the dots"),
            ("ul", ["Event: festive buying pushes up big-ticket purchases", "Economy: domestic GST up 15.8%, GST on imports up 42.2%, net GST up 25.6%", "Market: Nifty rose 2% last week as foreign investors (FIIs) turned net buyers"]),
            ("p", "My read: don't treat the 22.9% as pure demand. Domestic GST (up 15.8%) is the cleaner signal of what Indians are actually buying. Part of the 42% jump on imports may just be a weaker rupee making every import cost more in rupee terms."),
            ("p", "Stronger tax collections also give the government more room on its deficit, and bond markets watch that."),
            ("p", "The real test comes after Diwali. Does demand hold in November and December, or did the festive calendar pull October's buying forward?"),
            ("callout", "Takeaway: festive data shows India wants to spend. Post-festive data shows whether it can keep spending."),
         ],
         sources="IANS, 1 Nov 2026; Bombay Samachar, 1 Nov 2026; Business Today, 1 Nov 2026; Autocar India, 1 Nov 2026; Liquide weekly market review, 1 Nov 2026."),
    dict(slug="oil-flowing-again-why-118", urn="7522169251231662080", date="2026-10-31", time="11:05",
         title="Oil is flowing again. So why did it just touch $118?", topic="Oil",
         summary="Gulf barrels still arrive, but war-risk insurance has pushed freight to about ten times normal. A green index can hide a nervous market.",
         body=[
            ("p", "Picture a tanker crossing the Strait of Hormuz this week. Gulf crude exports are back above pre-war levels."),
            ("p", "But on Friday, a tanker in the strait was hit by explosives attached to a small boat. So the barrels still arrive. They just cost far more to move. Al Jazeera reports freight near $40 a barrel, about ten times normal, driven by war-risk insurance."),
            ("h2", "How I connect the dots"),
            ("chain", ["Hormuz attacks", "insurance and freight jump; Brent touched ~$118 on 30 Oct", "India relies heavily on imported crude, so it needs more dollars: pressure on the rupee and on inflation", "the RBI had already raised the repo rate by 25 bps to 5.50% on 7 Oct, its first hike in nearly four years", "markets: Nifty rose 0.51% on Friday, lifted by IT (+2.3%) and pharma, sectors that earn in dollars; energy and PSU banks fell over 1%, and midcaps and smallcaps slid"]),
            ("callout", "My read: a green index can hide a nervous market. When exporters lead, the market is quietly pricing in costlier oil and a costlier dollar."),
            ("p", "Next on the watchlist: the US midterms on 3 November. Traders fear the war could intensify after them."),
            ("p", "Is your portfolio built for $118 oil, or for the oil prices we had before this war?"),
         ],
         sources="Al Jazeera, 30 Oct 2026; The Nation/Reuters data, 31 Oct 2026; HDFC Sky market close, 30 Oct 2026; Business Today, 7 Oct 2026."),
    dict(slug="icici-ceo-factory", urn="7511704449489498113", date="2026-10-02", time="14:01",
         title="ICICI: the CEO factory of India?", topic="Banking",
         summary="HDFC Bank's incoming CEO spent 34 years at ICICI. He is far from the only Indian financial leader the group produced.",
         body=[
            ("p", "HDFC Bank's incoming MD and CEO Anup Bagchi has spent 34 years in the ICICI Group. And then I started looking at where some of India's other financial-sector leaders came from. The pattern is difficult to ignore."),
            ("table", [["Leader", "Years at ICICI", "Leadership elsewhere"],
                       ["Anup Bagchi", "~34", "Incoming MD & CEO, HDFC Bank"],
                       ["Shikha Sharma", "~29", "Former MD & CEO, Axis Bank"],
                       ["Kalpana Morparia", "~33", "Former CEO/Chairperson, J.P. Morgan South & Southeast Asia"],
                       ["Vishakha Mulye", "~30", "MD & CEO, Aditya Birla Capital"],
                       ["Hitesh Sethia", "20+", "MD & CEO, Jio Financial Services"],
                       ["Renuka Ramnath", "20+", "Founder, MD & CEO, Multiples; including 8 years as MD & CEO of ICICI Venture"],
                       ["Sonjoy Chatterjee", "16", "Chairman & former CEO, Goldman Sachs India"],
                       ["Anup Kumar Saha", "14", "Incoming MD & CEO, Kotak Mahindra Bank"],
                       ["V. Vaidyanathan", "10", "MD & CEO, IDFC FIRST Bank"],
                       ["Sudipta Roy", "~13", "MD & CEO, L&T Finance"],
                       ["Vedika Bhandarkar", "9", "Former MD & Vice Chairman, Credit Suisse Securities India"],
                       ["Ajay Srinivasan", "~6, across two stints", "Former CEO, Aditya Birla Group Financial Services"]]),
            ("p", "And these aren't merely employees who happened to move companies. Many were given exposure across retail banking, corporate banking, investment banking, insurance, asset management, international banking, credit and P&L leadership relatively early in their careers."),
            ("p", "There may be another reason too. Former ICICI chairman N. Vaghul reportedly had ICICI send appointment letters directly to the top 20 rankers in the Chartered Accountancy exams, sometimes without even interviewing them."),
            ("callout", "Maybe that's the real story. Hire exceptional people. Give them responsibility. Rotate them across businesses. Let them build. And eventually, some of them build institutions themselves."),
            ("p", "ICICI didn't just build businesses across Indian financial services. It helped build a generation of people who would go on to lead them. And with Anup Bagchi now moving to HDFC Bank, perhaps the phrase “ICICI, India's CEO factory” has never looked more relevant."),
            ("note", "Tenures are approximate in cases where publicly available biographies provide years rather than exact joining or leaving dates."),
         ],
         sources="HDFC Bank/Reuters, Kotak Mahindra Bank, IDFC FIRST Bank, Aditya Birla Capital, L&T Finance, Tata Consumer, Multiples, Fortune India, IIM Bangalore and Standard Chartered."),
]

# Other original posts, linked to LinkedIn (not republished here).
MORE_POSTS = [
    dict(urn="7523973312939511808", date="2026-11-05", topic="Markets", title="Nykaa and Lenskart: same day, same pattern", summary="Sales up about 30%, profits up two to three times, from two Indian consumer brands reporting on the same day."),
    dict(urn="7523794720796364800", date="2026-11-04", topic="Geopolitics", title="The President's party lost Congress. The Dow jumped 1,000 points.", summary="Why Wall Street cheered a result that sounds like bad news."),
    dict(urn="7523114860201750528", date="2026-11-03", topic="Oil", title="Oil dropped about 4%. Nobody signed anything.", summary="Markets aren't pricing peace. They're pricing fewer worst-case scenarios."),
    dict(urn="7522958256512831488", date="2026-11-02", topic="Infrastructure", title="Delhi to Agra in 58 minutes?", summary="What a proposed Delhi to Patna bullet train could change, and what is still only a proposal."),
    dict(urn="7522703881995214848", date="2026-11-01", topic="Gold", title="The Fed didn't raise rates. Gold took the hit anyway.", summary="When safe bonds pay close to 4.9%, holding gold costs more."),
    dict(urn="7522036507734368256", date="2026-10-31", topic="Crypto", title="Twenty minutes. Billions moved.", summary="A multibillion-dollar exchange theft, and why custody deserves a place beside returns."),
    dict(urn="7520202160677175296", date="2026-10-26", topic="Energy", title="Jamnagar and India's refining advantage", summary="Refining flexibility is not the same as energy independence."),
    dict(urn="7511463164962623489", date="2026-10-01", topic="Banking", title="HDFC Bank's ADR jumped after the new CEO announcement", summary="Why the first market reaction to Anup Bagchi's appointment came from the US."),
]

COMPANY_POSTS = [
    dict(urn="7523637505548746752", date="2026-11-04", title="Aurangabad Pipes is online", summary="The company website, aurangabadpipes.com, went live."),
    dict(urn="7522545963534626816", date="2026-11-01", title="Starting as Director, Marketing at Aurangabad Pipes", summary="From a shop floor to a bank and back to manufacturing in Aurangabad. One lesson: people buy from people they trust."),
]
