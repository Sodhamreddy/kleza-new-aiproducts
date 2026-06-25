import type { Metadata } from "next";
import DesignPage from "../_components/DesignPage";

export const metadata: Metadata = { title: "AI Products — Kleza" };

export default function AiProductsPage() {
  return <DesignPage file="ai-products.html" />;
}
