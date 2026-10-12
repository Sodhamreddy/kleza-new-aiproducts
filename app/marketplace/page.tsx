import type { Metadata } from "next";
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
 * shared chrome is untouched). `DesignPage` injects the CSS, renders the body, re-runs
 * the script on the client, and wraps it in the shared header and footer from
 * `content/_chrome.html`.
 */
export default function MarketplacePage() {
  return <DesignPage file="marketplace.html" />;
}
