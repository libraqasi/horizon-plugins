import fixture from './horizon-cash-delivery.fixture.json' with { type: 'json' };

export { fixture };

export function formatMoney(amountMinor, { whole = false } = {}) {
  return new Intl.NumberFormat(fixture.metadata.locale, {
    style: 'currency',
    currency: fixture.metadata.currency,
    minimumFractionDigits: whole ? 0 : 2,
    maximumFractionDigits: whole ? 0 : 2,
  }).format(amountMinor / 100);
}

export function formatAccountLabel(account = fixture.fundingAccount) {
  const product = account.productName.replace(/^Horizon\s+/, '');
  return `${product} ••${account.displayLast4}`;
}

export function formatAddress(address = fixture.customer.homeAddress) {
  return `${address.line1}, ${address.city}, ${address.state} ${address.postalCode}`;
}

export function formatArrivalWindow(window) {
  const scenario = fixture.metadata.scenarioDate.split('-').map(Number);
  const delivery = window.startsAt.slice(0, 10).split('-').map(Number);
  const dayDifference = Math.round((Date.UTC(...delivery.map((part, index) => index === 1 ? part - 1 : part))
    - Date.UTC(...scenario.map((part, index) => index === 1 ? part - 1 : part))) / 86400000);
  const dayLabel = dayDifference === 0 ? 'Today' : dayDifference === 1 ? 'Tomorrow' : new Intl.DateTimeFormat(
    fixture.metadata.locale,
    { month: 'short', day: 'numeric', timeZone: fixture.metadata.timezone },
  ).format(new Date(window.startsAt));
  const timeFormatter = new Intl.DateTimeFormat(fixture.metadata.locale, {
    hour: 'numeric',
    minute: '2-digit',
    timeZone: fixture.metadata.timezone,
  });
  return `${dayLabel}, ${timeFormatter.formatRange(new Date(window.startsAt), new Date(window.endsAt))}`;
}

export function getDropSpot(id) {
  return fixture.deliveryService.dropSpots.find((spot) => spot.id === id);
}

export function getArrivalWindow(id) {
  return fixture.deliveryService.arrivalWindows.find((window) => window.id === id);
}
