# Kleza — Next.js site

The Kleza marketing site (AI Transformation Company) built with **Next.js 14 (App Router)** from the
Claude Design handoff bundle. The primary page is **About**; all seven pages are implemented.

## Run

```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # production build
npm start        # serve the production build
```

## Routes

| Route                    | Source prototype             |
| ------------------------ | ---------------------------- |
| `/`                      | `content/Kleza.html` (home)  |
| `/about`                 | `content/about.html`         |
| `/ai-products`           | `content/ai-products.html`   |
| `/ai-services`           | `content/ai-services.html`   |
| `/enterprise-services`   | `content/enterprise-services.html` |
| `/resources`             | `content/resources.html`     |
| `/contact`               | `content/contact.html`       |

### Fully-designed sub-pages (second handoff)

These mega-menu items now have a complete prototype page of their own, mapped via
[`lib/pageOverrides.ts`](lib/pageOverrides.ts):

| Route                                          | Source prototype                       |
| ---------------------------------------------- | -------------------------------------- |
| `/about/careers`                               | `content/careers.html`                 |
| `/ai-services/training`                        | `content/ai-training.html`             |
| `/resources/articles`                          | `content/Blog.html`                    |
| `/enterprise-services/website-development`     | `content/Website Development.html`     |
| `/enterprise-services/digital-marketing`       | `content/Digital Marketing.html`       |
| `/enterprise-services/operational-outsourcing` | `content/Operational Outsourcing.html` |
| `/enterprise-services/remote-it-services`      | `content/Remote IT Services.html`      |
| `/enterprise-services/automation-tools`        | `content/Automation Tools.html`        |
| `/enterprise-services/search-visibility`       | `content/Search Visibility.html`       |
| `/enterprise-services/monitoring-verification` | `content/Monitoring Verification.html` |

## Sub-pages (one per remaining mega-menu item)

Mega-menu links without a designed page still resolve to a hand-built page under the
dynamic `[slug]` route per section — e.g. `/ai-products/voica`, `/resources/newsletter`:

- [`lib/menu.ts`](lib/menu.ts) — the menu data (name, copy, feature list) for every item.
- [`app/_components/SubPage.tsx`](app/_components/SubPage.tsx) — the detail-page template
  (breadcrumb → hero → feature block → CTA).
- [`app/_components/Chrome.tsx`](app/_components/Chrome.tsx) — shared header/footer reused
  from the prototype so the chrome matches the section pages exactly.

The link rewriter ([`lib/loadPage.ts`](lib/loadPage.ts)) keeps fragments that exist as real
in-page sections as anchors (`about.html#story → /about#story`) and maps the rest onto
sub-routes (`ai-products.html#voica → /ai-products/voica`).

## How it's wired

The design medium was hand-authored HTML/CSS/JS. To recreate it pixel-perfectly without lossy
hand-conversion, each page's authored markup lives in [`content/`](content/) and is rendered at build
time:

- [`lib/loadPage.ts`](lib/loadPage.ts) — reads a prototype file, extracts its `<style>`, `<body>` markup,
  and interaction scripts, and rewrites prototype links (`about.html#x → /about#x`, `assets/… → /assets/…`).
  The design-tool-only bits (React/Babel CDN, the "Tweaks" panel) are stripped out.
- [`app/_components/DesignPage.tsx`](app/_components/DesignPage.tsx) — server component that injects the
  page CSS + body markup.
- [`app/_components/PageScripts.tsx`](app/_components/PageScripts.tsx) — client component that re-runs the
  genuine interaction scripts (sticky header, mega-menu, accordion, testimonial carousel) and mirrors the
  original `<body>` attributes onto the real `<body>`.
- [`app/globals.css`](app/globals.css) — the shared design system (`shared.css` + `inner.css`).
- Static assets (logo, client logos, `nav.js`) are served from [`public/assets/`](public/assets/).

The original export lives in `_design_handoff/` (gitignored) for reference.
# kleza-new-aiproducts
