import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const projectDirectory = path.resolve(scriptDirectory, '..');
const canonicalDirectory = path.join(projectDirectory, 'synthetic-data', 'canonical');
const defaultOutput = path.join(projectDirectory, 'src', 'data', 'horizon-cash-delivery.fixture.json');

const deliveryService = {
  amountOptionsMinor: [10000, 20000, 30000],
  defaultAmountMinor: 20000,
  feeMinor: 0,
  dropSpots: [
    { id: 'front_porch', label: 'Front porch' },
    { id: 'side_entrance', label: 'Side entrance' },
    { id: 'back_patio', label: 'Back patio' },
  ],
  arrivalWindows: [
    {
      id: 'window_20260805_1430',
      startsAt: '2026-08-05T14:30:00-04:00',
      endsAt: '2026-08-05T15:00:00-04:00',
    },
    {
      id: 'window_20260805_1600',
      startsAt: '2026-08-05T16:00:00-04:00',
      endsAt: '2026-08-05T16:30:00-04:00',
    },
    {
      id: 'window_20260806_0900',
      startsAt: '2026-08-06T09:00:00-04:00',
      endsAt: '2026-08-06T09:30:00-04:00',
    },
  ],
  statusFlow: ['draft', 'preparing', 'on_way', 'delivered'],
  cancelableStatuses: ['draft', 'preparing'],
};

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function validateDeliveryService(account) {
  const { amountOptionsMinor, defaultAmountMinor, feeMinor, dropSpots, arrivalWindows } = deliveryService;
  assert(amountOptionsMinor.length > 0, 'At least one cash amount is required');
  assert(amountOptionsMinor.every((amount) => Number.isInteger(amount) && amount > 0), 'Cash amounts must be positive integer minor units');
  assert(amountOptionsMinor.includes(defaultAmountMinor), 'Default cash amount must be an available option');
  assert(Math.max(...amountOptionsMinor) + feeMinor <= account.available_balance_minor, 'Cash options must fit within the available balance');
  assert(Number.isInteger(feeMinor) && feeMinor >= 0, 'Fee must be a non-negative integer minor-unit value');
  assert(new Set(dropSpots.map(({ id }) => id)).size === dropSpots.length, 'Drop-spot IDs must be unique');

  const requestAsOf = Date.parse('2026-08-05T13:30:00-04:00');
  let previousEnd = requestAsOf;
  for (const window of arrivalWindows) {
    const start = Date.parse(window.startsAt);
    const end = Date.parse(window.endsAt);
    assert(Number.isFinite(start) && Number.isFinite(end), `Delivery window ${window.id} must use valid ISO timestamps`);
    assert(/-04:00$/.test(window.startsAt) && /-04:00$/.test(window.endsAt), `Delivery window ${window.id} must use the scenario offset`);
    assert(start >= previousEnd && end > start, `Delivery window ${window.id} must be ordered and non-overlapping`);
    previousEnd = end;
  }
}

export async function buildFixture(outputPath = defaultOutput) {
  const [bundle, manifest] = await Promise.all([
    readFile(path.join(canonicalDirectory, 'bundle.json'), 'utf8').then(JSON.parse),
    readFile(path.join(canonicalDirectory, 'manifest.json'), 'utf8').then(JSON.parse),
  ]);

  assert(bundle.customers?.length === 1, 'Canonical bundle must contain exactly one customer');
  const customer = bundle.customers[0];
  const checkingAccounts = bundle.accounts.filter((account) => (
    account.customer_id === customer.id && account.type === 'checking' && account.status === 'open'
  ));
  assert(checkingAccounts.length === 1, 'Customer must have exactly one open checking account');
  const account = checkingAccounts[0];

  assert(bundle.metadata.synthetic === true && customer.synthetic === true && account.synthetic === true, 'All source records must be explicitly synthetic');
  assert(customer.archetype === 'everyday-banking', 'Customer must use the everyday-banking archetype');
  assert(account.display_last4 === '4821', 'Checking account must preserve display last four 4821');
  assert(Number.isInteger(account.available_balance_minor), 'Available balance must use integer minor units');
  validateDeliveryService(account);

  const configDataset = manifest.config?.dataset;
  assert(configDataset?.timezone && configDataset?.locale && configDataset?.currency, 'Manifest must contain locale, timezone, and currency');

  const fixture = {
    metadata: {
      schemaVersion: bundle.metadata.schema_version,
      datasetId: bundle.metadata.dataset_id,
      scenarioDate: bundle.metadata.scenario_date,
      requestAsOf: '2026-08-05T13:30:00-04:00',
      timezone: configDataset.timezone,
      locale: configDataset.locale,
      currency: configDataset.currency,
      synthetic: true,
    },
    customer: {
      id: customer.id,
      displayName: customer.name.display,
      homeAddress: {
        line1: customer.address.line1,
        city: customer.address.city,
        state: customer.address.state,
        postalCode: customer.address.postal_code,
        country: customer.address.country,
      },
    },
    fundingAccount: {
      id: account.id,
      productName: account.product_name,
      type: account.type,
      displayLast4: account.display_last4,
      availableBalanceMinor: account.available_balance_minor,
      currency: account.currency,
      status: account.status,
      cashDeliveryEligible: true,
    },
    deliveryService,
    initialSession: {
      screen: 'landing',
      selectedAmountMinor: deliveryService.defaultAmountMinor,
      dropSpotId: deliveryService.dropSpots[0].id,
      arrivalWindowId: deliveryService.arrivalWindows[0].id,
      status: 'draft',
    },
  };

  const serialized = `${JSON.stringify(fixture, null, 2)}\n`;
  await writeFile(outputPath, serialized, 'utf8');
  return { fixture, serialized, outputPath };
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const outputArgument = process.argv.indexOf('--out');
  const outputPath = outputArgument >= 0 ? path.resolve(process.argv[outputArgument + 1]) : defaultOutput;
  const result = await buildFixture(outputPath);
  console.log(`Wrote ${result.outputPath}`);
}
