import { loadChrome } from "@/lib/loadPage";
import PageScripts from "./PageScripts";

/**
 * Shared page chrome (sticky mega-menu header + footer) for the hand-built
 * sub-pages. Both come from `content/_chrome.html` — the one file the menu is
 * defined in — which `DesignPage` renders too, so every page stays in step.
 * nav.js drives the menu.
 */
export default async function Chrome({
  children,
}: {
  children: React.ReactNode;
}) {
  const { headerHtml, footerHtml } = await loadChrome();
  return (
    <>
      <div dangerouslySetInnerHTML={{ __html: headerHtml }} />
      {children}
      <div dangerouslySetInnerHTML={{ __html: footerHtml }} />
      <PageScripts scripts={[{ src: "/assets/nav.js" }]} bodyAttrs={{}} />
    </>
  );
}
