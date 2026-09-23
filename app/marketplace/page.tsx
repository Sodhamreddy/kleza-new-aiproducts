import type { Metadata } from "next";
import Chrome from "../_components/Chrome";
import DesignPage from "../_components/DesignPage";

export const metadata: Metadata = {
  title: "Marketplace — Kleza",
  description:
    "Explore the KLEZA ecosystem of intelligent products built to simplify workflows, connect teams, and transform the work of care.",
};

/**
 * KLEZA Marketplace — the product ecosystem page: the rotating product deck
 * hero, the filterable full catalogue, the IVNA / Comes360 family panels, and
 * the value band.
 *
 * The page body, its scoped stylesheet, and its interaction script all live in
 * `content/marketplace.html` (everything is namespaced under `.mv2`, so the
 * shared chrome is untouched). `DesignPage` injects the CSS, renders the body,
 * and re-runs the script on the client; `Chrome` supplies the shared
 * mega-menu header and footer.
 */
export default function MarketplacePage() {
  return (
    <Chrome>
      <DesignPage file="marketplace.html" />
    </Chrome>
  );
}
