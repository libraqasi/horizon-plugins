import { fixture, formatAccountLabel, formatMoney } from '../data/cashDeliveryData.js';

export default function ReviewScreen({ delivery, onConfirm, onEdit }) {
  const totalDebitMinor = delivery.selectedAmountMinor + fixture.deliveryService.feeMinor;
  return (
    <main className="flow-main" id="main">
      <div className="preview-label"><span />Preview</div>
      <h1>Review your delivery</h1>
      <section className="review-card" aria-label="Delivery summary">
        <dl>
          <div><dt>From</dt><dd>{formatAccountLabel()}</dd></div>
          <div><dt>Cash amount</dt><dd>{formatMoney(delivery.selectedAmountMinor)}</dd></div>
          <div><dt>Drop spot</dt><dd>{delivery.dropSpot.label}, {fixture.customer.homeAddress.line1}</dd></div>
          <div><dt>Arrival</dt><dd>{delivery.arrivalLabel}</dd></div>
          <div><dt>Delivery fee</dt><dd>{formatMoney(fixture.deliveryService.feeMinor)}</dd></div>
        </dl>
        <div className="review-total"><strong>Total debit</strong><strong>{formatMoney(totalDebitMinor)}</strong></div>
      </section>
      <p className="review-note">This preview does not debit a real account.</p>
      <div className="flow-actions flow-actions--bottom">
        <button className="button button--primary" type="button" onClick={onConfirm}>Confirm delivery</button>
        <button className="button button--tertiary" type="button" onClick={onEdit}>Edit request</button>
      </div>
    </main>
  );
}
