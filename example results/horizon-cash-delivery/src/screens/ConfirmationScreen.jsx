import DeliveryMap from '../components/DeliveryMap.jsx';
import Timeline from '../components/Timeline.jsx';
import { BoxIcon, CheckCircleIcon } from '../components/Icons.jsx';
import { fixture } from '../data/cashDeliveryData.js';

export default function ConfirmationScreen({ delivery, canCancel, onCancel, onStatus }) {
  return (
    <main className="flow-main flow-main--confirmation" id="main">
      <div className="preview-label"><span />Preview</div>
      <h1>{delivery.status === 'delivered' ? 'Cash delivered' : 'Cash delivery scheduled'}</h1>
      <p className="success-line"><CheckCircleIcon />{delivery.status === 'delivered' ? 'Delivery complete' : 'Request confirmed'}</p>
      <section className="tracking-card" aria-label="Current delivery">
        <DeliveryMap status={delivery.status} address={fixture.customer.homeAddress} />
        <div className="tracking-summary">
          <span className="selection-icon selection-icon--green"><BoxIcon /></span>
          <span><strong>{delivery.status === 'delivered' ? 'Delivered to your drop spot' : delivery.status === 'on_way' ? 'Your drone is on the way' : 'Preparing your delivery'}</strong><small>{delivery.dropSpot.label} · {fixture.customer.homeAddress.line1}</small></span>
        </div>
      </section>
      <Timeline status={delivery.status} />
      <div className="flow-actions flow-actions--bottom">
        {canCancel && <button className="button button--secondary-danger" type="button" onClick={onCancel}>Cancel request</button>}
        <button className="button button--primary" type="button" onClick={onStatus}>View delivery status</button>
      </div>
    </main>
  );
}
