import DeliveryMap from '../components/DeliveryMap.jsx';
import { ChevronRight, HomeIcon } from '../components/Icons.jsx';
import { clockIcon } from '../assets.js';
import { fixture, formatAccountLabel, formatMoney } from '../data/cashDeliveryData.js';

export default function RequestScreen({ delivery, setAmount, onDropSpot, onArrival, onReview }) {
  return (
    <main className="flow-main" id="main">
      <div className="preview-label"><span />Preview</div>
      <h1>Get cash delivered</h1>
      <section className="account-card" aria-label="Funding account">
        <strong>{formatAccountLabel()}</strong>
        <span><small>Available balance</small>{formatMoney(fixture.fundingAccount.availableBalanceMinor)}</span>
      </section>

      <fieldset className="amount-fieldset">
        <legend>Cash amount</legend>
        <div className="amount-options">
          {fixture.deliveryService.amountOptionsMinor.map((amount) => (
            <button key={amount} className={delivery.selectedAmountMinor === amount ? 'is-selected' : ''} type="button" aria-pressed={delivery.selectedAmountMinor === amount} onClick={() => setAmount(amount)}>{formatMoney(amount, { whole: true })}</button>
          ))}
        </div>
      </fieldset>

      <section className="flow-section" aria-labelledby="location-heading">
        <h2 id="location-heading">Where should we deliver?</h2>
        <button className="location-card" type="button" onClick={onDropSpot}>
          <DeliveryMap status="request" address={fixture.customer.homeAddress} compact />
          <span className="selection-row">
            <span className="selection-icon"><HomeIcon /></span>
            <span className="selection-copy"><strong>{delivery.dropSpot.label}</strong><span>{fixture.customer.homeAddress.line1}</span></span>
            <ChevronRight />
          </span>
        </button>
      </section>

      <section className="flow-section" aria-labelledby="arrival-heading">
        <h2 id="arrival-heading">When should it arrive?</h2>
        <button className="selection-button" type="button" onClick={onArrival}>
          <span className="selection-icon"><img src={clockIcon} alt="" /></span>
          <span>{delivery.arrivalLabel}</span>
          <ChevronRight />
        </button>
      </section>

      <div className="flow-actions">
        <button className="button button--primary" type="button" onClick={onReview}>Review delivery</button>
        <button className="button button--tertiary" type="button" onClick={onDropSpot}>Choose another drop spot</button>
      </div>
    </main>
  );
}
