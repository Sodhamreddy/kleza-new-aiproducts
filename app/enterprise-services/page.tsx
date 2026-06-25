import type { Metadata } from "next";
import DesignPage from "../_components/DesignPage";

export const metadata: Metadata = { title: "Enterprise Services — Kleza" };

export default function EnterpriseServicesPage() {
  return <DesignPage file="enterprise-services.html" />;
}
