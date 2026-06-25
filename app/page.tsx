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
              font-size: clamp(38px, 5.2vw, 70px) !important;
            }

            .stats-text h2,
            .testi-head h2 {
              font-size: clamp(30px, 4.2vw, 54px) !important;
            }

            .products-head h2 {
              font-size: clamp(26px, 3.3vw, 44px) !important;
            }

            .cta h2 {
              font-size: clamp(34px, 5vw, 66px) !important;
            }
          `,
        }}
      />
    </>
  );
}
