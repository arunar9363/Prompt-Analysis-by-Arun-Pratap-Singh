import type { Metadata } from "next";
import { Oxanium, Space_Mono } from "next/font/google";
import "./globals.css";
import { CyberNav } from "@/components/layout/CyberNav";
import { ScrollProgress } from "@/components/layout/ScrollProgress";

const oxanium = Oxanium({
  subsets: ["latin"],
  variable: "--font-oxanium",
  display: "swap",
});

const spaceMono = Space_Mono({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-space-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "XAVIER_NEON // Full-Stack Architect Portfolio",
  description:
    "Interactive developer storytelling portfolio of Xavier Neon, Senior Full-Stack Frontend Architect & Creative UI Engineer. Core reactive systems & hyper-performance digital spaces.",
  keywords: [
    "Cyberpunk Portfolio",
    "Frontend Architect",
    "Creative Developer",
    "Next.js Portfolio",
    "Framer Motion Portfolio",
    "Xavier Neon",
    "React Engineer",
  ],
  authors: [{ name: "Xavier Neon" }],
  openGraph: {
    title: "XAVIER_NEON // Full-Stack Architect Portfolio",
    description:
      "Interactive developer storytelling portfolio of Xavier Neon. Core reactive systems & hyper-performance digital spaces.",
    url: "https://cyberdomain.tech",
    siteName: "Xavier Neon Portfolio",
    images: [
      {
        url: "https://cyberdomain.tech/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Xavier Neon Cyberpunk Portfolio",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "XAVIER_NEON // Full-Stack Architect Portfolio",
    description:
      "Interactive developer storytelling portfolio of Xavier Neon. Core reactive systems & hyper-performance digital spaces.",
    images: ["https://cyberdomain.tech/og-image.jpg"],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${oxanium.variable} ${spaceMono.variable} scroll-smooth`}>
      <body className="font-sans antialiased min-h-screen flex flex-col bg-cyber-bg text-white selection:bg-cyber-cyan selection:text-cyber-darker">
        {/* Navigation & Progress Bar */}
        <ScrollProgress />
        <CyberNav />

        {/* Scanlines & CRT overlays for retro-futuristic atmosphere */}
        <div className="fixed inset-0 pointer-events-none z-50 bg-cyber-scanlines opacity-30" />
        <div className="fixed inset-0 pointer-events-none z-50 bg-gradient-to-b from-cyber-cyan/5 via-transparent to-cyber-pink/5" />

        <div className="flex-1 flex flex-col">{children}</div>
      </body>
    </html>
  );
}
