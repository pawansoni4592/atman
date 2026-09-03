import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Atman",
  description: "Your personal AI mentor.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
