export default function CanceledScreen({ onRestart }) {
  return (
    <main className="flow-main state-screen" id="main">
      <div className="preview-label"><span />Preview</div>
      <div className="state-icon state-icon--canceled" aria-hidden="true">×</div>
      <h1>Delivery canceled</h1>
      <p>Your request was canceled. This preview did not debit a real account.</p>
      <button className="button button--primary" type="button" onClick={onRestart}>Start a new request</button>
    </main>
  );
}
