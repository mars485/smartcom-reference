# IT Services — SmartCom-inspired reference

An independently implemented responsive, Russian-language IT services website. **Not affiliated with SmartCom**. Original SmartCom imagery, logos, copy and contact details are not used.

**Live preview:** https://mars485.github.io/smartcom-reference/

## Included

- Home page, three service pages, team and contacts pages
- Consistent responsive navigation across all six pages, services, workflow, FAQ, and a contact-form demo
- Local SVG favicon, custom 404 page, sitemap and robots.txt
- GitHub Actions checks for links, metadata, basic accessibility landmarks, sitemap consistency, and JavaScript syntax
- Plain HTML, CSS and JavaScript: no dependencies or build step

## Run locally

Open `index.html` or start a static web server:

```bash
python3 -m http.server 8000
```

## Validate

```bash
python3 scripts/check_site.py
node --check assets/js/main.js
```

## Contact form

**Demo only.** Use test data. The browser validates fields locally; no data is transmitted or stored. The form deliberately retains entered values after validation so users can see what was checked. To accept real inquiries, add an approved backend endpoint, spam protection, privacy notice, and verified business contact details. Never commit API keys or secrets to this public repository.

## Deployment

GitHub Pages publishes from `main` / repository root. A separate workflow checks links and assets on every push.

## Release status

The static reference is ready for review. Production lead handling and business identity require verified contact details, privacy text, and an approved backend. The project is independent and is not affiliated with SmartCom.
