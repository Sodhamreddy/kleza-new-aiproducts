import type { Metadata } from "next";
import DesignPage from "../_components/DesignPage";

export const metadata: Metadata = { title: "AI Services — Kleza" };

export default function AiServicesPage() {
  return <DesignPage file="ai-services.html" />;
}
