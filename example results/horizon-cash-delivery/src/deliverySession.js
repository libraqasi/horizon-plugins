import { fixture } from './data/cashDeliveryData.js';

export const STORAGE_KEY = 'horizon-cash-delivery-preview:v1';

const screens = new Set(['landing', 'request', 'review', 'confirmation', 'status', 'canceled']);
const statuses = new Set([...fixture.deliveryService.statusFlow, 'canceled']);

export function createInitialSession(screen = fixture.initialSession.screen) {
  return { ...fixture.initialSession, screen };
}

export function isValidSession(session) {
  return Boolean(
    session
    && screens.has(session.screen)
    && statuses.has(session.status)
    && fixture.deliveryService.amountOptionsMinor.includes(session.selectedAmountMinor)
    && fixture.deliveryService.dropSpots.some(({ id }) => id === session.dropSpotId)
    && fixture.deliveryService.arrivalWindows.some(({ id }) => id === session.arrivalWindowId),
  );
}

export function readSession(storage) {
  try {
    const stored = JSON.parse(storage.getItem(STORAGE_KEY));
    if (
      stored?.schemaVersion === fixture.metadata.schemaVersion
      && stored?.datasetId === fixture.metadata.datasetId
      && isValidSession(stored.session)
    ) {
      return stored.session;
    }
  } catch {
    // Invalid or inaccessible preview state falls back to the generated fixture.
  }
  return createInitialSession();
}

export function persistSession(storage, session) {
  try {
    storage.setItem(STORAGE_KEY, JSON.stringify({
      schemaVersion: fixture.metadata.schemaVersion,
      datasetId: fixture.metadata.datasetId,
      session,
    }));
  } catch {
    // The preview remains usable when storage is disabled or unavailable.
  }
}

export function canCancel(status) {
  return fixture.deliveryService.cancelableStatuses.includes(status);
}

export function advanceStatus(status) {
  const flow = fixture.deliveryService.statusFlow;
  const index = flow.indexOf(status);
  return index >= 0 && index < flow.length - 1 ? flow[index + 1] : status;
}
