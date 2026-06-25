import { loadPage } from "@/lib/loadPage";
import PageScripts from "./PageScripts";

/**
 * Server component that renders one prototype page faithfully:
 * injects the page-specific CSS, the (link-rewritten) body markup, and
 * re-runs the interaction scripts on the client.
 */
export default async function DesignPage({ file }: { file: string }) {
  const { bodyHtml, css, scripts, bodyAttrs, jsonLd } = await loadPage(file);
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
      <div dangerouslySetInnerHTML={{ __html: bodyHtml }} />
      <PageScripts scripts={scripts} bodyAttrs={bodyAttrs} />
    </>
  );
}
