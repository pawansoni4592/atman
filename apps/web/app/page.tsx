export default function Home() {
  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "80px 24px", fontFamily: "system-ui" }}>
      <p style={{ fontSize: 14, letterSpacing: 2, textTransform: "uppercase", opacity: 0.6 }}>ATMAN</p>
      <h1 style={{ fontSize: 52, lineHeight: 1.05, margin: "16px 0" }}>Your personal AI mentor.</h1>
      <p style={{ fontSize: 20, lineHeight: 1.6, maxWidth: 680 }}>
        Atman will remember what matters to you, understand your goals, and help you make better decisions over time.
      </p>
      <div style={{ marginTop: 40, padding: 24, border: "1px solid #ddd", borderRadius: 16 }}>
        <strong>Foundation is live.</strong>
        <p style={{ marginBottom: 0, opacity: 0.7 }}>Next: connect this interface to the Atman API and persistent memory.</p>
      </div>
    </main>
  );
}
