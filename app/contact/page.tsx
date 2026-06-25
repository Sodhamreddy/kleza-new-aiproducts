import type { Metadata } from "next";
import DesignPage from "../_components/DesignPage";

export const metadata: Metadata = { title: "Contact — Kleza" };

export default function ContactPage() {
  return <DesignPage file="contact.html" />;
}
