# Site generator

The pages (index, work, about, insights, contact, 404, insights/*.html, sitemap.xml, robots.txt) are generated.

- `content.py` holds every fact on the site: roles, education, certifications, skills, quotes, articles and posts.
- `build.py` turns it into HTML. Styles live in `assets/site.css`, behaviour in `assets/site.js`.

To change content: edit `content.py`, then from this folder run `python3 build.py` (Python 3.9+, no packages).
It writes into the repository root (the folder above this one).
Commit the regenerated HTML. Vercel deploys `main` to production and any other branch to a preview URL.

LinkedIn follower and impression figures are not in content.py: they live in `assets/linkedin-stats.json`.
