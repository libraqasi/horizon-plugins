import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import { buildFixture } from '../scripts/build-cash-delivery-fixture.mjs';
import {
  fixture,
  formatAccountLabel,
  formatAddress,
  formatArrivalWindow,
  formatMoney,
} from '../src/data/cashDeliveryData.js';

const projectDirectory = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

test('adapter output is deterministic and matches the committed fixture', async () => {
  const temporaryDirectory = await mkdtemp(path.join(os.tmpdir(), 'horizon-cash-delivery-'));
  try {
    const firstPath = path.join(temporaryDirectory, 'first.json');
    const secondPath = path.join(temporaryDirectory, 'second.json');
    const [first, second, committed] = await Promise.all([
      buildFixture(firstPath),
      buildFixture(secondPath),
      readFile(path.join(projectDirectory, 'src', 'data', 'horizon-cash-delivery.fixture.json'), 'utf8'),
    ]);
    assert.equal(first.serialized, second.serialized);
    assert.equal(first.serialized, committed);
  } finally {
    await rm(temporaryDirectory, { recursive: true, force: true });
  }
});

test('fixture exposes one safe, eligible synthetic customer relationship', () => {
  assert.equal(fixture.metadata.synthetic, true);
  assert.equal(fixture.metadata.scenarioDate, '2026-08-05');
  assert.equal(fixture.customer.displayName, 'Avery Garcia');
  assert.equal(fixture.fundingAccount.displayLast4, '4821');
  assert.equal(fixture.fundingAccount.type, 'checking');
  assert.equal(fixture.fundingAccount.status, 'open');
  assert.equal(fixture.fundingAccount.cashDeliveryEligible, true);
  assert.equal('contact' in fixture.customer, false);
  assert.equal('dateOfBirth' in fixture.customer, false);
  assert.equal('address' in fixture.deliveryService.dropSpots[0], false);

  const serialized = JSON.stringify(fixture).toLowerCase();
  for (const forbidden of ['password', 'routing_number', 'account_number', 'card_number', 'social_security', 'security_answer']) {
    assert.equal(serialized.includes(forbidden), false, `Fixture must not contain ${forbidden}`);
  }
});

test('money, delivery choices, and display values derive from fixture facts', () => {
  const { amountOptionsMinor, defaultAmountMinor, feeMinor } = fixture.deliveryService;
  assert(amountOptionsMinor.every(Number.isInteger));
  assert(Number.isInteger(fixture.fundingAccount.availableBalanceMinor));
  assert(Math.max(...amountOptionsMinor) + feeMinor <= fixture.fundingAccount.availableBalanceMinor);
  assert(amountOptionsMinor.includes(defaultAmountMinor));
  assert.equal(defaultAmountMinor + feeMinor, 20000);
  assert.equal(formatMoney(fixture.fundingAccount.availableBalanceMinor), '$2,089.48');
  assert.equal(formatMoney(defaultAmountMinor, { whole: true }), '$200');
  assert.equal(formatAccountLabel(), 'Everyday Checking ••4821');
  assert.equal(formatAddress(), '100 Demo Avenue, Charlotte, NC 28202');
});

test('delivery windows are ordered, non-overlapping, future-looking, and scenario-relative', () => {
  const requestAsOf = Date.parse(fixture.metadata.requestAsOf);
  let previousEnd = requestAsOf;
  fixture.deliveryService.arrivalWindows.forEach((window, index) => {
    const start = Date.parse(window.startsAt);
    const end = Date.parse(window.endsAt);
    assert(start >= previousEnd);
    assert(end > start);
    assert.match(window.startsAt, /-04:00$/);
    assert.match(window.endsAt, /-04:00$/);
    assert.match(formatArrivalWindow(window), new RegExp(index < 2 ? '^Today, ' : '^Tomorrow, '));
    previousEnd = end;
  });
});

test('legacy hard-coded customer facts no longer remain in runtime source', async () => {
  const sourceFiles = [
    'App.jsx',
    'components/DeliveryMap.jsx',
    'screens/RequestScreen.jsx',
    'screens/ReviewScreen.jsx',
    'screens/StatusScreen.jsx',
  ];
  const source = (await Promise.all(sourceFiles.map((file) => readFile(path.join(projectDirectory, 'src', file), 'utf8')))).join('\n');
  assert.equal(source.includes('118 Oak Street'), false);
  assert.equal(source.includes('$2,480.75'), false);
  assert.equal(source.includes('Everyday Checking ••4821'), false);
});
