# IT Services — SmartCom-inspired reference

An independently implemented responsive, Russian-language IT services website. **Not affiliated with SmartCom**. Original SmartCom imagery, logos, copy and contact details are not used.

**Live preview:** https://mars485.github.io/smartcom-reference/

## Included

- Home page, three service pages, team and contacts pages
- Responsive navigation, services, workflow, FAQ, accessible contact-form demo
- Local SVG favicon, custom 404 page, sitemap and robots.txt
- GitHub Actions static HTML/link validation
- Plain HTML, CSS and JavaScript: no dependencies or build step

## Run locally

Open `index.html` or start a static web server:

```bash
python3 -m http.server 8000
```

## Validate

```bash
python3 scripts/check_site.py
```

## Contact form

**Demo only.** Form fields are validated locally; no data is transmitted or stored. To use this for real business leads, configure a backend endpoint, spam protection, privacy notice and a real business email address. Never commit API keys or secrets to this public repository.

## Deployment

GitHub Pages publishes from `main` / repository root. A separate workflow checks links and assets on every push.

## Release status

Static demo v1.2 is complete. Production lead handling and business-specific identity require real credentials and contact details.
