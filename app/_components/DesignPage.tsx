import { loadChrome, loadPage } from "@/lib/loadPage";
import PageScripts from "./PageScripts";

/**
 * Server component that renders one prototype page faithfully:
 * injects the page-specific CSS, the (link-rewritten) body markup, and
 * re-runs the interaction scripts on the client.
 *
 * The header and footer come from `content/_chrome.html` — the single place
 * the menu is defined — not from the page file, so a menu change lands on
 * every page at once. `loadPage` drops any header/footer still embedded in a
 * page so nothing renders twice.
 */
export default async function DesignPage({ file }: { file: string }) {
  const [{ bodyHtml, css, scripts, bodyAttrs, jsonLd }, { headerHtml, footerHtml }] =
    await Promise.all([loadPage(file), loadChrome()]);

  return (
    <>
      {jsonLd.map((block, i) => (
        <script
          key={i}
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: block }}
        />
      ))}
      <style dangerouslySetInnerHTML={{ __html: css }} />
      <div dangerouslySetInnerHTML={{ __html: headerHtml }} />
      <div dangerouslySetInnerHTML={{ __html: bodyHtml }} />
      <div dangerouslySetInnerHTML={{ __html: footerHtml }} />
      <PageScripts scripts={scripts} bodyAttrs={bodyAttrs} />
    </>
  );
}
