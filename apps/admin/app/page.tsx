export default function AdminHome() {
  return (
    <main style={{ maxWidth: 1000, margin: "0 auto", padding: "64px 24px", fontFamily: "system-ui" }}>
      <h1>Atman Admin</h1>
      <p>Administration and observability for the Atman platform.</p>
      <section style={{ marginTop: 32, padding: 24, border: "1px solid #ddd", borderRadius: 16 }}>
        <strong>System status</strong>
        <p style={{ marginBottom: 0 }}>Dashboard foundation is ready.</p>
      </section>
    </main>
  );
}
