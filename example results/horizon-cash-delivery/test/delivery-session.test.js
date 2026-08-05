import assert from 'node:assert/strict';
import test from 'node:test';

import { fixture } from '../src/data/cashDeliveryData.js';
import {
  STORAGE_KEY,
  advanceStatus,
  canCancel,
  createInitialSession,
  persistSession,
  readSession,
} from '../src/deliverySession.js';

function memoryStorage(initialValue = null) {
  const values = new Map(initialValue === null ? [] : [[STORAGE_KEY, initialValue]]);
  return {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
    removeItem: (key) => values.delete(key),
  };
}

test('valid session state persists with dataset and schema versions', () => {
  const storage = memoryStorage();
  const session = { ...createInitialSession('request'), selectedAmountMinor: 30000 };
  persistSession(storage, session);
  assert.deepEqual(readSession(storage), session);
  const envelope = JSON.parse(storage.getItem(STORAGE_KEY));
  assert.equal(envelope.datasetId, fixture.metadata.datasetId);
  assert.equal(envelope.schemaVersion, fixture.metadata.schemaVersion);
});

test('disabled browser storage does not break session initialization or persistence', () => {
  const unavailableStorage = {
    getItem: () => { throw new Error('storage disabled'); },
    setItem: () => { throw new Error('storage disabled'); },
  };
  assert.deepEqual(readSession(unavailableStorage), createInitialSession());
  assert.doesNotThrow(() => persistSession(unavailableStorage, createInitialSession()));
});

test('stale, malformed, and invalid stored sessions reset to fixture defaults', () => {
  const validSession = createInitialSession('request');
  const cases = [
    '{bad json',
    JSON.stringify({ schemaVersion: fixture.metadata.schemaVersion, datasetId: 'stale', session: validSession }),
    JSON.stringify({ schemaVersion: fixture.metadata.schemaVersion, datasetId: fixture.metadata.datasetId, session: { ...validSession, dropSpotId: 'missing' } }),
    JSON.stringify({ schemaVersion: fixture.metadata.schemaVersion, datasetId: fixture.metadata.datasetId, session: { ...validSession, selectedAmountMinor: 99999 } }),
  ];
  for (const stored of cases) assert.deepEqual(readSession(memoryStorage(stored)), createInitialSession());
});

test('request progresses deterministically and cancellation closes before dispatch', () => {
  assert.equal(advanceStatus('draft'), 'preparing');
  assert.equal(advanceStatus('preparing'), 'on_way');
  assert.equal(advanceStatus('on_way'), 'delivered');
  assert.equal(advanceStatus('delivered'), 'delivered');
  assert.equal(canCancel('draft'), true);
  assert.equal(canCancel('preparing'), true);
  assert.equal(canCancel('on_way'), false);
  assert.equal(canCancel('delivered'), false);
});

test('restart and reset use independent fixture-backed session objects', () => {
  const first = createInitialSession('request');
  const second = createInitialSession();
  first.selectedAmountMinor = 10000;
  assert.equal(second.selectedAmountMinor, fixture.deliveryService.defaultAmountMinor);
  assert.equal(first.screen, 'request');
  assert.equal(second.screen, 'landing');
  assert.equal(second.status, 'draft');
});
