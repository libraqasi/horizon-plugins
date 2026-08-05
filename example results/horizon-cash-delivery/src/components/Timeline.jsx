import { fixture } from '../data/cashDeliveryData.js';

const labels = {
  draft: 'Request confirmed',
  preparing: 'Cash is being prepared',
  on_way: 'Drone is on the way',
  delivered: 'Delivery complete',
};

export default function Timeline({ status }) {
  const steps = fixture.deliveryService.statusFlow;
  const current = Math.max(steps.indexOf(status), 1);
  return (
    <ol className="timeline" aria-label="Delivery progress">
      {steps.map((key, index) => (
        <li key={key} className={`${index < current ? 'is-complete' : ''} ${index === current ? 'is-current' : ''}`}>
          <span className="timeline-marker" aria-hidden="true">{index < current ? '✓' : ''}</span>
          <span>{labels[key]}{index === current && <span className="sr-only">, current status</span>}</span>
        </li>
      ))}
    </ol>
  );
}
