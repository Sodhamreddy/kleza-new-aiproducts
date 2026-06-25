import { readFile } from "fs/promises";
import path from "path";

export interface ScriptDesc {
  src?: string;
  code?: string;
}

export interface PageData {
  title: string;
  bodyHtml: string;
  css: string;
  scripts: ScriptDesc[];
  bodyAttrs: Record<string, string>;
  /** `application/ld+json` blocks lifted from the prototype's <head>. */
  jsonLd: string[];
}

/** Map the prototype's flat .html filenames onto Next.js routes. */
const PAGE_MAP: Record<string, string> = {
  "Kleza.html": "/",
  "about.html": "/about",
  "ai-products.html": "/ai-products",
  "ai-services.html": "/ai-services",
  "enterprise-services.html": "/enterprise-services",
  "resources.html": "/resources",
  "contact.html": "/contact",
  // Full sub-pages added in the second design handoff.
  "careers.html": "/about/careers",
  "partners.html": "/about/partners",
  "ai-training.html": "/ai-services/training",
  "ai-assistant.html": "/ai-services/assistant",
  "Blog.html": "/resources/articles",
  "Website Development.html": "/enterprise-services/website-development",
  "Digital Marketing.html": "/enterprise-services/digital-marketing",
  "Operational Outsourcing.html": "/enterprise-services/operational-outsourcing",
  "Remote IT Services.html": "/enterprise-services/remote-it-services",
  "Automation Tools.html": "/enterprise-services/automation-tools",
  "Search Visibility.html": "/enterprise-services/search-visibility",
  "Monitoring Verification.html": "/enterprise-services/monitoring-verification",
};

/**
 * Fragments that exist as real in-page section ids in the prototypes —
 * these stay `#anchors` on the page route. Every other `page.html#frag`
 * link is a mega-menu item that maps onto its own sub-route.
 */
const IN_PAGE_ANCHORS: Record<string, string[]> = {
  "/": ["solutions", "products", "proof", "contact"],
  "/about": ["story", "vision", "healthcare", "partnerships", "careers"],
  "/contact": ["form", "schedule", "experts"],
};

/** Scripts that belong to the design tool, not the real site. */
function isDesignToolScript(attrs: string, code: string): boolean {
  if (/type\s*=\s*["']text\/babel["']/i.test(attrs)) return true;
  if (/src\s*=\s*["'][^"']*(unpkg\.com|react|babel|\.jsx)[^"']*["']/i.test(attrs)) return true;
  return false;
}

function parseAttrs(attrStr: string): Record<string, string> {
  const attrs: Record<string, string> = {};
  const re = /([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*"([^"]*)"/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(attrStr)) !== null) {
    attrs[m[1]] = m[2];
  }
  return attrs;
}

/** Matches every prototype filename (incl. ones with spaces) + optional #fragment. */
const LINK_RE = new RegExp(
  "(" +
    Object.keys(PAGE_MAP)
      .sort((a, b) => b.length - a.length)
      .map((f) => f.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/ /g, "(?: |%20)"))
      .join("|") +
    ")(#[A-Za-z0-9_-]+)?",
  "g"
);

/** Rewrite prototype asset + page links onto Next.js paths. */
function rewriteLinks(html: string): string {
  // assets/foo.png  ->  /assets/foo.png  (inside attributes & url())
  let out = html.replace(/(["'(=])assets\//g, "$1/assets/");
  // Page links:
  //   about.html#story            -> /about#story   (real in-page anchor)
  //   ai-products.html#voica      -> /ai-products/voica   (mega-menu sub-route)
  //   Website Development.html    -> /enterprise-services/website-development
  out = out.replace(LINK_RE, (_m, file: string, frag?: string) => {
    const route = PAGE_MAP[file.replace(/%20/g, " ")];
    if (!frag) return route;
    const id = frag.slice(1);
    if ((IN_PAGE_ANCHORS[route] ?? []).includes(id)) return `${route}${frag}`;
    return route === "/" ? `/${frag}` : `${route}/${id}`;
  });
  out = out.replace(
    /(<a class="nav-link" href="\/enterprise-services">Enterprise Services)<\/a>/g,
    `$1
            <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </a>`
  );
  return out;
}

/**
 * Extracts the shared header + footer markup from a reference prototype so new
 * (hand-built) sub-pages can reuse the exact same chrome.
 */
export async function loadChrome(): Promise<{
  headerHtml: string;
  footerHtml: string;
}> {
  const full = path.join(process.cwd(), "content", "about.html");
  const raw = await readFile(full, "utf8");
  const header = raw.match(/<header[\s\S]*?<\/header>/i)?.[0] ?? "";
  const footer = raw.match(/<footer[\s\S]*?<\/footer>/i)?.[0] ?? "";
  return {
    headerHtml: rewriteLinks(header),
    footerHtml: rewriteLinks(footer),
  };
}

export async function loadPage(file: string): Promise<PageData> {
  const full = path.join(process.cwd(), "content", file);
  const raw = await readFile(full, "utf8");

  const titleMatch = raw.match(/<title>([\s\S]*?)<\/title>/i);
  const title = (titleMatch ? titleMatch[1].trim() : "Kleza")
    .replace(/&mdash;/g, "—")
    .replace(/&ndash;/g, "–")
    .replace(/&amp;/g, "&");

  // All <style> blocks (page-specific CSS lives in the <head>).
  const css = Array.from(raw.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi))
    .map((m) => m[1])
    .join("\n");

  // Structured data (JobPosting / FAQPage / Organization, …) lives in <head>;
  // lift it out so the rendered route keeps its schema.org markup.
  const jsonLd = Array.from(
    raw.matchAll(
      /<script\b[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi
    )
  )
    .map((m) => m[1].trim())
    .filter(Boolean);

  // Body element + its attributes.
  const bodyMatch = raw.match(/<body([^>]*)>([\s\S]*?)<\/body>/i);
  const bodyAttrsRaw = bodyMatch ? bodyMatch[1] : "";
  let bodyInner = bodyMatch ? bodyMatch[2] : "";
  const bodyAttrs = parseAttrs(bodyAttrsRaw);

  bodyInner = rewriteLinks(bodyInner);

  // Pull scripts out of the body so dangerouslySetInnerHTML stays inert,
  // then re-run the genuine interaction scripts on the client.
  const scripts: ScriptDesc[] = [];
  bodyInner = bodyInner.replace(
    /<script\b([^>]*)>([\s\S]*?)<\/script>/gi,
    (_full, attrs: string, code: string) => {
      if (isDesignToolScript(attrs, code)) return "";
      const srcMatch = attrs.match(/src\s*=\s*"([^"]*)"/i);
      if (srcMatch) scripts.push({ src: srcMatch[1] });
      else if (code.trim()) scripts.push({ code });
      return "";
    }
  );

  // Drop the design-tool tweaks mount + bundler thumbnail template (inert noise).
  bodyInner = bodyInner
    .replace(/<div id="kleza-tweaks-root"[\s\S]*?<\/div>/i, "")
    .replace(/<template id="__bundler_thumbnail"[\s\S]*?<\/template>/i, "");

  return { title, bodyHtml: bodyInner, css, scripts, bodyAttrs, jsonLd };
}

export function pageRoutes() {
  return PAGE_MAP;
}
