import DeliveryMap from '../components/DeliveryMap.jsx';
import Timeline from '../components/Timeline.jsx';
import { CheckCircleIcon } from '../components/Icons.jsx';
import { fixture, formatMoney } from '../data/cashDeliveryData.js';

const statusCopy = {
  preparing: ['Cash is being prepared', 'Your cash is being counted and secured for delivery.'],
  on_way: ['Your drone is on the way', 'The delivery is headed to your selected drop spot.'],
  delivered: ['Your cash has arrived', 'The delivery was completed at your selected drop spot.'],
};

export default function StatusScreen({ delivery, onAdvance, onBack }) {
  const [title, body] = statusCopy[delivery.status] ?? statusCopy.preparing;
  const advanceLabel = delivery.status === 'preparing' ? 'Mark drone on the way' : 'Mark delivery complete';
  return (
    <main className="flow-main status-screen" id="main">
      <div className="preview-label"><span />Preview</div>
      <button className="back-link" type="button" onClick={onBack}>
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 5-7 7 7 7" /></svg>
        Back to summary
      </button>
      <h1>Delivery status</h1>
      <DeliveryMap status={delivery.status} address={fixture.customer.homeAddress} />
      <section className="status-callout" aria-live="polite">
        <CheckCircleIcon />
        <div><h2>{title}</h2><p>{body}</p></div>
      </section>
      <Timeline status={delivery.status} />
      <dl className="status-details">
        <div><dt>Drop spot</dt><dd>{delivery.dropSpot.label}</dd></div>
        <div><dt>Address</dt><dd>{fixture.customer.homeAddress.line1}</dd></div>
        <div><dt>Cash amount</dt><dd>{formatMoney(delivery.selectedAmountMinor)}</dd></div>
      </dl>
      <div className="flow-actions flow-actions--bottom">
        {delivery.status !== 'delivered' && <button className="button button--primary" type="button" onClick={onAdvance}>{advanceLabel}</button>}
        <button className="button button--tertiary" type="button" onClick={onBack}>Back to delivery summary</button>
      </div>
    </main>
  );
}
