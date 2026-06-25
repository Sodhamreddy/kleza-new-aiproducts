import type { Metadata } from "next";
import DesignPage from "../_components/DesignPage";

export const metadata: Metadata = {
  title: "Home Test - Kleza",
};

export default function HomeTestPage() {
  return (
    <>
      <DesignPage file="Kleza.html" />
      <style
        dangerouslySetInnerHTML={{
          __html: `
            :is(h1, h2, h3, h4, h5, h6) {
              font-family: "Plus Jakarta Sans", var(--sans) !important;
            }

            .ecosystem-header h2 {
              font-size: clamp(40px, 5vw, 72px) !important;
              line-height: 1.04 !important;
              letter-spacing: -0.045em !important;
              word-spacing: 0.06em !important;
            }

            .section-head h2 {
              font-size: clamp(36px, 4.7vw, 64px) !important;
              line-height: 1.04 !important;
              letter-spacing: -0.045em !important;
              word-spacing: 0.06em !important;
            }

            .stats-text h2 {
              font-size: clamp(34px, 4.2vw, 55px) !important;
              line-height: 1.05 !important;
              letter-spacing: -0.045em !important;
              word-spacing: 0.06em !important;
            }

            .ecosystem-header h2 .ital {
              word-spacing: 0.12em !important;
            }
          `,
        }}
      />
    </>
  );
}
