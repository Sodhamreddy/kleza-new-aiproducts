import fs from "fs";
import path from "path";
import type { Metadata } from "next";
import Chrome from "../_components/Chrome";

export const metadata: Metadata = { title: "Marketplace — Kleza" };

/**
 * Marketplace page — a faithful replica of the Kleza reference marketplace
 * design (hero + Recommended + Products by Category + trust band + CTA),
 * rendered inside the shared Kleza chrome. The body markup is fully
 * inline-styled; only a handful of layout/hover classes need CSS, all scoped
 * under `.mp-scope` so the reference reset never touches our header/footer.
 */
const MP_CSS = `
  @keyframes mpfloat { 0%,100% { transform: translate(0); } 50% { transform: translate(22px,-20px); } }
  @keyframes mpfloat2 { 0%,100% { transform: translate(0); } 50% { transform: translate(-26px,18px); } }

  .mp-scope, .mp-scope * { box-sizing: border-box; }
  .mp-scope { font-family: Inter, ui-sans-serif, system-ui, sans-serif; color: rgb(28,43,74); -webkit-font-smoothing: antialiased; letter-spacing: -0.011em; background: #fff; }
  .mp-scope p, .mp-scope li { font-family: Mukta, Inter, ui-sans-serif, system-ui, sans-serif; }
  .mp-scope h1, .mp-scope h2, .mp-scope h3, .mp-scope h4 { letter-spacing: -0.035em; margin: 0; }
  .mp-scope a { text-decoration: none; color: inherit; }
  .mp-scope button { font-family: inherit; cursor: pointer; }

  .mp-scope .mp-title { font-size: 58px; }
  .mp-scope .mp-cards-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; }
  .mp-scope .mp-features-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 24px; }
  .mp-scope .mp-card { transition: transform .18s ease, box-shadow .18s ease; }
  .mp-scope .mp-card:hover { transform: translateY(-3px); box-shadow: rgba(15,23,42,.04) 0 1px 2px, rgba(15,23,42,.2) 0 22px 44px -28px; }
  .mp-scope .mp-discover { transition: transform .18s ease, border-color .18s ease, background .18s ease; }
  .mp-scope .mp-discover:hover { transform: translateY(-3px); border-color: rgb(151,130,230) !important; background: color-mix(in srgb, rgb(151,130,230) 6%, #fff) !important; }

  .mp-scope .cat-pill { transition: background .18s, color .18s, border-color .18s; }
  .mp-scope .cat-pill:not(.is-active):hover { border-color: rgb(151,130,230) !important; color: rgb(107,91,214) !important; background: color-mix(in srgb, rgb(151,130,230) 8%, #fff) !important; }
  .mp-scope .cat-pill.is-active:hover { filter: brightness(1.06); }
  .mp-scope .card-cta { transition: background .2s, color .2s, border-color .2s; }
  .mp-scope .card-cta:hover { background: rgb(124,92,219) !important; border-color: rgb(124,92,219) !important; color: #fff !important; }
  .mp-scope .btn-glass { transition: background .2s, border-color .2s, transform .2s, box-shadow .2s; }
  .mp-scope .btn-glass:hover { transform: translateY(-2px); background: #fff !important; border-color: #fff !important; box-shadow: rgba(15,23,42,.35) 0 14px 26px -14px !important; }
  .mp-scope .btn-glass:active { transform: translateY(0); }

  @media (max-width: 1024px) {
    .mp-scope .mp-title { font-size: 42px; }
    .mp-scope .mp-cards-grid, .mp-scope .mp-features-grid { grid-template-columns: 1fr 1fr; }
    .mp-scope .mp-search-row { flex-wrap: wrap; }
  }
  @media (max-width: 640px) {
    .mp-scope .mp-title { font-size: 34px; }
    .mp-scope .mp-cards-grid, .mp-scope .mp-features-grid { grid-template-columns: 1fr; }
  }
`;

export default function Page() {
  const body = fs.readFileSync(
    path.join(process.cwd(), "content", "marketplace-body.html"),
    "utf8"
  );
  return (
    <Chrome>
      <style dangerouslySetInnerHTML={{ __html: MP_CSS }} />
      <div className="mp-scope" dangerouslySetInnerHTML={{ __html: body }} />
    </Chrome>
  );
}
