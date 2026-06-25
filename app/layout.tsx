import type { Metadata } from "next";
import "./globals.css";
import VoiceAssistant from "./_components/VoiceAssistant";

export const metadata: Metadata = {
  title: "Kleza — Intelligence, engineered for the work of care.",
  description:
    "Kleza is a fast-growing AI Transformation Company built on a singular vision: to humanize technology and make intelligence accessible, ethical, and meaningful for every business.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        {/* eslint-disable-next-line @next/next/google-font-preconnect */}
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Instrument+Serif:ital,wght@0,400;1,400&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        {children}
        <VoiceAssistant />
      </body>
    </html>
  );
}
