import type { Metadata } from "next";
import DesignPage from "../_components/DesignPage";

export const metadata: Metadata = { title: "About — Kleza" };

export default function AboutPage() {
  return <DesignPage file="about.html" />;
}
