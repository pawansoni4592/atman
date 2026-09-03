import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Atman Admin",
  description: "Atman administration console.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
