import DesignPage from "./_components/DesignPage";

export default function HomePage() {
  return (
    <>
      <DesignPage file="Kleza.html" />
      <style
        dangerouslySetInnerHTML={{
          __html: `
            /* The heading face now lives in globals.css, site-wide; this page
               no longer forces its own heavier weight, so its headings match
               every other page. What stays here is purely heading sizing. */
            .ecosystem-header h2,
            .section-head h2 {
              font-size: clamp(26px, 3.4vw, 44px) !important;
              line-height: 1.35 !important;
            }

            .stats-text h2,
            .testi-head h2 {
              font-size: clamp(24px, 3vw, 38px) !important;
              line-height: 1.35 !important;
            }

            .products-head h2 {
              font-size: clamp(22px, 2.6vw, 34px) !important;
              line-height: 1.35 !important;
            }

            .cta h2 {
              font-size: clamp(26px, 3.4vw, 42px) !important;
              line-height: 1.35 !important;
            }
          `,
        }}
      />
    </>
  );
}
