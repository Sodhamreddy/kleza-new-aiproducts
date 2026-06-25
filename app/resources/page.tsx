import type { Metadata } from "next";
import DesignPage from "../_components/DesignPage";

export const metadata: Metadata = { title: "Resources — Kleza" };

export default function ResourcesPage() {
  return <DesignPage file="resources.html" />;
}
