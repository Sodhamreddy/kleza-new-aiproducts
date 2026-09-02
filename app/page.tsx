import DesignPage from "./_components/DesignPage";

export default function HomePage() {
  return (
    <>
      <DesignPage file="Kleza.html" />
      <style
        dangerouslySetInnerHTML={{
          __html: `
            :is(h1, h2, h3, h4, h5, h6),
            :is(h1, h2, h3, h4, h5, h6) * {
              font-family: "Playfair Display", ui-serif, Georgia, serif !important;
              font-weight: 600 !important;
            }

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
