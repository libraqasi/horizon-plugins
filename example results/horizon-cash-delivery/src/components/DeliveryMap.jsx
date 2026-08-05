import { droneIcon } from '../assets.js';
import { formatAddress } from '../data/cashDeliveryData.js';

export default function DeliveryMap({ status = 'request', address, compact = false }) {
  const showDrone = status !== 'request';
  const addressLabel = formatAddress(address);
  return (
    <div className={`delivery-map ${compact ? 'delivery-map--compact' : ''}`} role="img" aria-label={showDrone ? `Map showing the drone route to ${addressLabel}` : `Map showing the drop spot at ${addressLabel}`}>
      <svg viewBox="0 0 600 260" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
        <rect width="600" height="260" fill="var(--surface-warm)" />
        <g className="map-parks">
          <path d="M28 164 106 128l62 42-30 75H49Z" />
          <path d="m448 24 95 13 34 59-79 45-71-50Z" />
        </g>
        <g className="map-roads">
          <path d="M-20 48 620 206M-4 214 615 68M90-20l66 305M304-24l-32 310M493-18l-46 306" />
          <path d="M-20 122 620 32M-20 250 620 150" />
        </g>
        {showDrone && <path className="map-route" d="M112 188 C245 155 367 126 486 94" />}
        <g className="map-pin" transform="translate(468 54)">
          <path d="M18 0C8 0 0 8 0 18c0 14 18 34 18 34s18-20 18-34C36 8 28 0 18 0Z" />
          <circle cx="18" cy="18" r="7" />
        </g>
      </svg>
      {showDrone && (
        <span className={`map-drone map-drone--${status}`} aria-hidden="true">
          <img src={droneIcon} alt="" />
        </span>
      )}
    </div>
  );
}
