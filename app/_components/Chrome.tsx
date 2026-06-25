import { loadChrome } from "@/lib/loadPage";
import PageScripts from "./PageScripts";

/**
 * Shared page chrome (sticky mega-menu header + footer) reused by the
 * hand-built sub-pages. The header/footer markup is lifted verbatim from the
 * prototype so it matches the section pages exactly; nav.js drives the menu.
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
