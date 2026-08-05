import { useCallback, useEffect, useState } from 'react';
import BrandHeader from './components/BrandHeader.jsx';
import Modal from './components/Modal.jsx';
import LandingPage from './screens/LandingPage.jsx';
import RequestScreen from './screens/RequestScreen.jsx';
import ReviewScreen from './screens/ReviewScreen.jsx';
import ConfirmationScreen from './screens/ConfirmationScreen.jsx';
import StatusScreen from './screens/StatusScreen.jsx';
import CanceledScreen from './screens/CanceledScreen.jsx';
import { fixture, formatArrivalWindow, getArrivalWindow, getDropSpot } from './data/cashDeliveryData.js';
import { STORAGE_KEY, advanceStatus, canCancel, createInitialSession, persistSession, readSession } from './deliverySession.js';

export default function App() {
  const [delivery, setDelivery] = useState(() => readSession(window.localStorage));
  const [modal, setModal] = useState(null);

  useEffect(() => {
    persistSession(window.localStorage, delivery);
    window.scrollTo({ top: 0, behavior: 'auto' });
  }, [delivery]);

  const update = (changes) => setDelivery((current) => ({ ...current, ...changes }));
  const closeModal = useCallback(() => setModal(null), []);
  const reset = () => {
    localStorage.removeItem(STORAGE_KEY);
    setModal(null);
    setDelivery(createInitialSession());
  };
  const restart = () => setDelivery(createInitialSession('request'));
  const advance = () => update({ status: advanceStatus(delivery.status) });
  const dropSpot = getDropSpot(delivery.dropSpotId);
  const arrivalWindow = getArrivalWindow(delivery.arrivalWindowId);
  const deliveryView = {
    ...delivery,
    dropSpot,
    arrivalWindow,
    arrivalLabel: formatArrivalWindow(arrivalWindow),
  };

  if (delivery.screen === 'landing') return <LandingPage onLogin={() => update({ screen: 'request' })} />;

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main">Skip to content</a>
      <BrandHeader onReset={reset} />
      <div className="flow-shell">
        {delivery.screen === 'request' && (
          <RequestScreen
            delivery={deliveryView}
            setAmount={(selectedAmountMinor) => update({ selectedAmountMinor })}
            onDropSpot={() => setModal('dropSpot')}
            onArrival={() => setModal('arrival')}
            onReview={() => update({ screen: 'review' })}
          />
        )}
        {delivery.screen === 'review' && <ReviewScreen delivery={deliveryView} onConfirm={() => update({ screen: 'confirmation', status: 'preparing' })} onEdit={() => update({ screen: 'request' })} />}
        {delivery.screen === 'confirmation' && <ConfirmationScreen delivery={deliveryView} canCancel={canCancel(delivery.status)} onCancel={() => setModal('cancel')} onStatus={() => update({ screen: 'status' })} />}
        {delivery.screen === 'status' && <StatusScreen delivery={deliveryView} onAdvance={advance} onBack={() => update({ screen: 'confirmation' })} />}
        {delivery.screen === 'canceled' && <CanceledScreen onRestart={restart} />}
      </div>

      <Modal open={modal === 'dropSpot'} title="Choose a drop spot" description="Select where the drone should leave your delivery." onClose={closeModal}>
        <div className="option-list">
          {fixture.deliveryService.dropSpots.map((spot) => (
            <button key={spot.id} className={delivery.dropSpotId === spot.id ? 'is-selected' : ''} type="button" onClick={() => { update({ dropSpotId: spot.id }); closeModal(); }}>
              <span><strong>{spot.label}</strong><small>{fixture.customer.homeAddress.line1}</small></span>
              <span aria-hidden="true">{delivery.dropSpotId === spot.id ? '✓' : ''}</span>
            </button>
          ))}
        </div>
      </Modal>

      <Modal open={modal === 'arrival'} title="Choose an arrival time" description="Select a delivery window." onClose={closeModal}>
        <div className="option-list">
          {fixture.deliveryService.arrivalWindows.map((arrival) => (
            <button key={arrival.id} className={delivery.arrivalWindowId === arrival.id ? 'is-selected' : ''} type="button" onClick={() => { update({ arrivalWindowId: arrival.id }); closeModal(); }}>
              <strong>{formatArrivalWindow(arrival)}</strong><span aria-hidden="true">{delivery.arrivalWindowId === arrival.id ? '✓' : ''}</span>
            </button>
          ))}
        </div>
      </Modal>

      <Modal open={modal === 'cancel'} title="Cancel this delivery?" description="Your request will be canceled. This preview never debits a real account." onClose={closeModal} variant="dialog">
        <div className="dialog-actions">
          <button className="button button--secondary" type="button" onClick={closeModal}>Keep delivery</button>
          <button className="button button--danger" type="button" onClick={() => { update({ screen: 'canceled', status: 'canceled' }); closeModal(); }}>Cancel delivery</button>
        </div>
      </Modal>
    </div>
  );
}
