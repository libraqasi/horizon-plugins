import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const emptyDashboard = {
  balances: { totalDigitalAssetValueMinor: 0, custodyBalanceMinor: 0, walletBalanceMinor: 0 },
  activities: [],
  activitySummary: { total: 0, posted: 0, pending: 0 },
  custody: { accounts: [], fundingAccounts: [], alerts: [] },
  stablecoins: { symbol: 'USDC', network: 'Ethereum (ERC-20)', custodyBalanceMinor: 0, pendingBalanceMinor: 0, postedActivityCount: 0, pendingActivityCount: 0 },
  walletDetails: { address: '', network: 'Ethereum (ERC-20)', balanceMinor: 0, activity: [], delegations: [] },
  asset: { symbol: 'USDC', network: 'Ethereum (ERC-20)' },
  wallet: { address: '', network: 'Ethereum (ERC-20)' },
};

const navItems = [
  ['overview', 'Overview', HomeIcon],
  ['custody', 'Custody', ShieldIcon],
  ['stablecoins', 'Stablecoins', CoinIcon],
  ['wallet', 'Wallet', WalletIcon],
  ['activity', 'Activity', HistoryIcon],
];
const navIds = new Set(navItems.map(([id]) => id));

function formatCurrency(minor) {
  return `$${(Number(minor || 0) / 100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function formatSignedCurrency(minor) {
  const amount = Number(minor || 0);
  return `${amount < 0 ? '-' : ''}${formatCurrency(Math.abs(amount))}`;
}

function Icon({ children, size = 22, className = '' }) {
  return <svg className={`icon ${className}`} width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{children}</svg>;
}

function HomeIcon() { return <Icon><path d="m3 10 9-7 9 7" /><path d="M5.5 9.5v10h13v-10" /><path d="M9.5 19.5v-5h5v5" /></Icon>; }
function ShieldIcon() { return <Icon><path d="M12 3 19 6v5.2c0 4.2-2.7 7.9-7 9.8-4.3-1.9-7-5.6-7-9.8V6l7-3Z" /><path d="m9.5 12 1.7 1.7 3.5-3.5" /></Icon>; }
function CoinIcon() { return <Icon><circle cx="12" cy="12" r="8.3" /><path d="M12 7.3v9.4M14.5 9.2c-.6-.7-1.4-1.1-2.5-1.1-1.4 0-2.3.8-2.3 1.8 0 2.5 4.8 1 4.8 3.6 0 1.1-1 1.9-2.5 1.9-1.1 0-2-.4-2.7-1.2" /></Icon>; }
function WalletIcon() { return <Icon><path d="M4 6.5h13.5A2.5 2.5 0 0 1 20 9v9.5H5.5A2.5 2.5 0 0 1 3 16V6.8A2.8 2.8 0 0 1 5.8 4H18" /><path d="M20 11h-5a2 2 0 0 0 0 4h5" /><circle cx="15" cy="13" r=".4" fill="currentColor" stroke="none" /></Icon>; }
function HistoryIcon() { return <Icon><path d="M4 7.5V4m0 3.5h3.5" /><path d="M5.1 7.6A8 8 0 1 1 4.3 14" /><path d="M12 8v4l2.7 1.6" /></Icon>; }
function SupportIcon() { return <Icon><path d="M4 13v-1a8 8 0 0 1 16 0v1" /><path d="M4 13h2.5v5H4.8A1.8 1.8 0 0 1 3 16.2v-1.4A1.8 1.8 0 0 1 4.8 13ZM20 13h-2.5v5h1.7a1.8 1.8 0 0 0 1.8-1.8v-1.4A1.8 1.8 0 0 0 19.2 13Z" /><path d="M17.5 18c-.6 1.4-1.8 2.1-3.7 2.1h-1" /></Icon>; }
function SignOutIcon() { return <Icon><path d="M13 5h6v14h-6" /><path d="M3 12h10m-3-3 3 3-3 3" /></Icon>; }
function BellIcon() { return <Icon size={24}><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9ZM10 21h4" /></Icon>; }
function UserIcon() { return <Icon size={25}><circle cx="12" cy="12" r="9" /><circle cx="12" cy="9" r="2.6" /><path d="M7.7 17c1-2.2 2.5-3.3 4.3-3.3s3.3 1.1 4.3 3.3" /></Icon>; }
function CopyIcon() { return <Icon size={21}><rect x="8" y="8" width="11" height="11" rx="1.5" /><path d="M16 8V5.8A1.8 1.8 0 0 0 14.2 4H5.8A1.8 1.8 0 0 0 4 5.8v8.4A1.8 1.8 0 0 0 5.8 16H8" /></Icon>; }
function ArrowDownIcon() { return <Icon size={24}><path d="M12 4v15m-5-5 5 5 5-5" /></Icon>; }
function ArrowUpIcon() { return <Icon size={24}><path d="M12 20V5m-5 5 5-5 5 5" /></Icon>; }
function InfoIcon() { return <Icon size={24}><circle cx="12" cy="12" r="9" /><path d="M12 11v5m0-8.2v.2" /></Icon>; }
function GridIcon() { return <Icon size={24}><circle cx="6" cy="6" r="1" fill="currentColor" stroke="none" /><circle cx="12" cy="6" r="1" fill="currentColor" stroke="none" /><circle cx="18" cy="6" r="1" fill="currentColor" stroke="none" /><circle cx="6" cy="12" r="1" fill="currentColor" stroke="none" /><circle cx="12" cy="12" r="1" fill="currentColor" stroke="none" /><circle cx="18" cy="12" r="1" fill="currentColor" stroke="none" /><circle cx="6" cy="18" r="1" fill="currentColor" stroke="none" /><circle cx="12" cy="18" r="1" fill="currentColor" stroke="none" /><circle cx="18" cy="18" r="1" fill="currentColor" stroke="none" /></Icon>; }
function ChevronIcon() { return <Icon size={18}><path d="m7 9 5 5 5-5" /></Icon>; }

function PageTitle({ title, description }) {
  return <div className="title-row"><div><h1>{title}</h1>{description && <p className="title-description">{description}</p>}</div></div>;
}

function BalanceStrip({ data }) {
  return <section className="balance-strip" aria-labelledby="balance-heading">
    <div><p className="eyebrow" id="balance-heading">Total digital asset value</p><p className="balance-value">{formatCurrency(data.balances.totalDigitalAssetValueMinor)}</p></div>
    <div className="balance-divider" />
    <div className="custody-value"><p className="eyebrow">Custody balance</p><div className="custody-line"><span>{data.asset.symbol}</span><strong>{formatCurrency(data.balances.custodyBalanceMinor)}</strong></div></div>
  </section>;
}

function ActivityTable({ activities, activityFilter, setActivityFilter, compact = false }) {
  const filters = ['All activity', 'Pending', 'Posted'];
  const filteredActivities = activityFilter === 'All activity' ? activities : activities.filter((activity) => activity.status === activityFilter);
  return <section className={`panel activity-panel ${compact ? 'activity-panel--compact' : ''}`} aria-labelledby="activity-heading">
    <div className="section-header"><div><h2 id="activity-heading">Recent activity</h2>{compact && <p className="panel-description">Your latest custody and wallet movements.</p>}</div><div className="activity-tabs" role="tablist" aria-label="Activity filter">{filters.map((filter) => <button key={filter} className={activityFilter === filter ? 'activity-tab--active' : ''} onClick={() => setActivityFilter(filter)} role="tab" aria-selected={activityFilter === filter}>{filter}</button>)}</div></div>
    <div className="table-wrap"><table><caption className="horizon-sr-only">Recent digital asset activity</caption><thead><tr><th scope="col">Date</th><th scope="col">Description</th><th scope="col">Type</th><th scope="col">Status</th><th scope="col" className="amount-col">Amount</th></tr></thead><tbody>{filteredActivities.map((activity) => <tr key={activity.id}><td>{activity.date}</td><td>{activity.description}</td><td>{activity.type}</td><td><span className={`status status--${activity.tone}`}><span className="status-dot" />{activity.status}</span></td><td className="amount-col amount">{formatSignedCurrency(activity.amountMinor)}</td></tr>)}</tbody></table></div>
    {filteredActivities.length === 0 && <div className="empty-state">There are no {activityFilter.toLowerCase()} items to show.</div>}
  </section>;
}

function ActionCard({ icon: CardIcon, title, detail, action, onClick }) {
  return <section className="panel action-card"><div className="action-card-icon"><CardIcon /></div><div><h2>{title}</h2><p className="panel-description">{detail}</p></div><button className="horizon-button horizon-button--secondary" onClick={onClick}>{action}</button></section>;
}

function StablecoinTrade({ data, tradeMode, setTradeMode, payAmount, setPayAmount, onReview }) {
  const receiveAmount = useMemo(() => {
    const numeric = Number(payAmount.replace(/,/g, ''));
    if (!numeric) return '0.00';
    return (tradeMode === 'buy' ? numeric : numeric / 0.999).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }, [payAmount, tradeMode]);
  return <section className="panel trading-panel" aria-labelledby="trading-heading">
    <h2 id="trading-heading">Stablecoin trading</h2>
    <p className="panel-description">Buy or sell {data.asset.symbol} using your Horizon funding account.</p>
    <div className="tabs" role="tablist" aria-label="Stablecoin trade type"><button className={`tab ${tradeMode === 'buy' ? 'tab--active' : ''}`} onClick={() => setTradeMode('buy')} role="tab" aria-selected={tradeMode === 'buy'}>Buy</button><button className={`tab ${tradeMode === 'sell' ? 'tab--active' : ''}`} onClick={() => setTradeMode('sell')} role="tab" aria-selected={tradeMode === 'sell'}>Sell</button></div>
    <form className="trade-form" onSubmit={onReview}>
      <label htmlFor="pay-amount">{tradeMode === 'buy' ? 'You pay' : 'You sell'}</label>
      <div className="money-field"><span className="currency-prefix">$</span><input id="pay-amount" inputMode="decimal" value={payAmount} onChange={(event) => setPayAmount(event.target.value.replace(/[^0-9.]/g, ''))} placeholder="0.00" aria-describedby="pay-currency" /><span className="field-suffix">{tradeMode === 'buy' ? 'USD' : data.asset.symbol}<ChevronIcon /></span></div>
      <span className="field-help" id="pay-currency">{tradeMode === 'buy' ? 'US Dollar' : 'USD Coin (USDC)'}</span>
      <label htmlFor="receive-amount">You receive</label>
      <div className="money-field money-field--receive"><input id="receive-amount" value={receiveAmount} readOnly aria-describedby="receive-currency" /><span className="field-suffix">{tradeMode === 'buy' ? data.asset.symbol : 'USD'}<ChevronIcon /></span></div>
      <span className="field-help" id="receive-currency">{tradeMode === 'buy' ? 'USD Coin (USDC)' : 'US Dollar'}</span>
      <button className="horizon-button horizon-button--primary review-button" type="submit">Review order</button>
    </form>
  </section>;
}

function WalletPanel({ data, onNotice, onAction, compact = false }) {
  const wallet = data.walletDetails;
  const copyAddress = () => { navigator.clipboard?.writeText(wallet.address); onNotice('Wallet address copied.'); };
  return <section className={`panel wallet-panel ${compact ? 'wallet-panel--compact' : ''}`} aria-labelledby="wallet-heading">
    <div className="section-heading-row"><div><h2 id="wallet-heading">Digital wallet</h2><p className="panel-description">Your self-directed wallet for receiving and sending {data.asset.symbol}.</p></div>{!compact && <span className="status status--posted"><span className="status-dot" />Active</span>}</div>
    <div className="wallet-balance"><span>Wallet balance</span><strong>{formatCurrency(wallet.balanceMinor)}</strong></div>
    <div className="wallet-actions"><button className="wallet-action" onClick={() => onAction('wallet_receive', 'Receive flow selected. Share the address only after confirming the network.')}><ArrowDownIcon /><span>Receive</span></button><button className="wallet-action" onClick={() => onAction('wallet_send', 'Send flow selected. Review the destination and network before confirming.')}><ArrowUpIcon /><span>Send</span></button></div>
    <div className="wallet-detail"><p className="detail-label">Wallet address</p><div className="address-row"><code>{wallet.address || 'Loading…'}</code><button className="copy-button" onClick={copyAddress} aria-label="Copy wallet address" disabled={!wallet.address}><CopyIcon /></button></div></div>
    <div className="network-detail"><p className="detail-label">Network</p><p>{wallet.network}</p></div>
    {!compact && wallet.delegations?.map((delegation) => <div className="delegation-row" key={delegation.id}><div><p className="detail-label">Delegated access</p><p>{delegation.delegate_display_name}</p></div><span className="status status--posted">{delegation.status}</span></div>)}
    {!compact && wallet.recentActions?.length > 0 && <div className="control-log"><p className="detail-label">Latest control activity</p><p>{wallet.recentActions[0].detail}</p><span>{wallet.recentActions[0].status}</span></div>}
  </section>;
}

function OverviewView({ data, onNavigate, activityFilter, setActivityFilter }) {
  return <>
    <PageTitle title="Overview" description="A clear view of your Horizon digital asset relationship." />
    <BalanceStrip data={data} />
    <div className="overview-grid">
      <ActionCard icon={ShieldIcon} title="Custody" detail={`${formatCurrency(data.balances.custodyBalanceMinor)} held in Horizon custody`} action="Open custody" onClick={() => onNavigate('custody')} />
      <ActionCard icon={CoinIcon} title="Stablecoins" detail={`${data.stablecoins.pendingActivityCount} pending activity item${data.stablecoins.pendingActivityCount === 1 ? '' : 's'} to review`} action={`Trade ${data.asset.symbol}`} onClick={() => onNavigate('stablecoins')} />
      <ActionCard icon={WalletIcon} title="Wallet" detail={`${formatCurrency(data.walletDetails.balanceMinor)} available on ${data.walletDetails.network}`} action="Open wallet" onClick={() => onNavigate('wallet')} />
      <ActionCard icon={HistoryIcon} title="Activity" detail={`${data.activitySummary.posted} posted · ${data.activitySummary.pending} pending`} action="View activity" onClick={() => onNavigate('activity')} />
    </div>
    <ActivityTable activities={data.activities.slice(0, 5)} activityFilter={activityFilter} setActivityFilter={setActivityFilter} compact />
  </>;
}

function CustodyView({ data, onNavigate, onNotice, onAction }) {
  return <>
    <PageTitle title="Custody" description="See where your digital assets are held and how they are moving." />
    <BalanceStrip data={data} />
    <div className="section-grid">
      <section className="panel" aria-labelledby="holdings-heading"><h2 id="holdings-heading">Asset holdings</h2><div className="holding-list">{data.custody.accounts.map((account) => <div className="holding-row" key={account.id}><div><strong>{account.label}</strong><span>{account.assetSymbol} · {account.network}</span></div><div className="holding-amount"><strong>{formatCurrency(account.balanceMinor)}</strong><span>{account.postedCount} posted · {account.pendingCount} pending</span></div></div>)}</div></section>
      <section className="panel" aria-labelledby="funding-heading"><h2 id="funding-heading">Linked funding accounts</h2><div className="funding-list">{data.custody.fundingAccounts.map((account) => <div className="funding-row" key={account.id}><div><strong>{account.productName}</strong><span>{account.type} · •••• {account.displayLast4}</span></div><strong>{formatCurrency(account.availableBalanceMinor)}</strong></div>)}</div><button className="horizon-button horizon-button--secondary panel-action" onClick={() => onAction('funding_review', 'Funding account review recorded for the next transfer.')}>Review funding account</button></section>
    </div>
    {data.custody.alerts.length > 0 && <section className="panel custody-alert" aria-labelledby="custody-alert-heading"><InfoIcon /><div><h2 id="custody-alert-heading">Account summary available</h2><p>{data.custody.alerts[0].message}</p></div><button className="horizon-button horizon-button--secondary" onClick={() => onNavigate('activity')}>View activity</button></section>}
  </>;
}

function StablecoinsView({ data, tradeMode, setTradeMode, payAmount, setPayAmount, onReview, activityFilter, setActivityFilter }) {
  return <>
    <PageTitle title="Stablecoins" description={`Buy, sell, and monitor your ${data.asset.symbol} position.`} />
    <div className="stablecoin-layout"><StablecoinTrade data={data} tradeMode={tradeMode} setTradeMode={setTradeMode} payAmount={payAmount} setPayAmount={setPayAmount} onReview={onReview} /><section className="panel stablecoin-summary" aria-labelledby="stablecoin-summary-heading"><h2 id="stablecoin-summary-heading">{data.asset.symbol} position</h2><div className="large-stat"><span>Custody balance</span><strong>{formatCurrency(data.stablecoins.custodyBalanceMinor)}</strong></div><div className="stat-list"><div><span>Pending balance</span><strong>{formatSignedCurrency(data.stablecoins.pendingBalanceMinor)}</strong></div><div><span>Posted activity</span><strong>{data.stablecoins.postedActivityCount}</strong></div><div><span>Network</span><strong>{data.stablecoins.network}</strong></div></div><button className="horizon-button horizon-button--secondary panel-action" onClick={() => setTradeMode('buy')}>Start a new buy</button></section></div>
    <ActivityTable activities={data.activities.filter((activity) => activity.description.includes(data.asset.symbol))} activityFilter={activityFilter} setActivityFilter={setActivityFilter} compact />
  </>;
}

function WalletView({ data, onNotice, onAction, onNavigate, activityFilter, setActivityFilter }) {
  return <>
    <PageTitle title="Wallet" description="Manage your wallet address, network, and transfer activity." />
    <WalletPanel data={data} onNotice={onNotice} onAction={onAction} />
    <div className="wallet-lower-grid"><section className="panel" aria-labelledby="wallet-guidance-heading"><h2 id="wallet-guidance-heading">Before you send</h2><ul className="guidance-list"><li>Confirm the destination address and network.</li><li>Review the amount and any applicable fees.</li><li>Transfers are shown as pending until posted.</li></ul><button className="horizon-button horizon-button--secondary" onClick={() => onNavigate('activity')}>Review wallet activity</button></section><ActivityTable activities={data.walletDetails.activity.slice(0, 5)} activityFilter={activityFilter} setActivityFilter={setActivityFilter} compact /></div>
  </>;
}

function ActivityView({ data, activityFilter, setActivityFilter }) {
  return <>
    <PageTitle title="Activity" description="Review every stablecoin and wallet movement from the SQLite ledger." />
    <div className="summary-strip"><div><span>Total activity</span><strong>{data.activitySummary.total}</strong></div><div><span>Posted</span><strong>{data.activitySummary.posted}</strong></div><div><span>Pending</span><strong>{data.activitySummary.pending}</strong></div></div>
    <ActivityTable activities={data.activities} activityFilter={activityFilter} setActivityFilter={setActivityFilter} />
  </>;
}

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [loadError, setLoadError] = useState('');
  const [activeNav, setActiveNav] = useState(() => navIds.has(window.location.hash.slice(1)) ? window.location.hash.slice(1) : 'overview');
  const [tradeMode, setTradeMode] = useState('buy');
  const [payAmount, setPayAmount] = useState('');
  const [activityFilter, setActivityFilter] = useState('All activity');
  const [walletNotice, setWalletNotice] = useState('');
  const [orderReview, setOrderReview] = useState(false);
  const [orderComplete, setOrderComplete] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetch('/api/dashboard')
      .then((response) => { if (!response.ok) throw new Error('The local SQLite API is unavailable.'); return response.json(); })
      .then((data) => { if (!cancelled) setDashboard(data); })
      .catch((error) => { if (!cancelled) setLoadError(error.message); });
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    const syncFromUrl = () => {
      const next = window.location.hash.slice(1);
      if (navIds.has(next)) setActiveNav(next);
    };
    window.addEventListener('popstate', syncFromUrl);
    window.addEventListener('hashchange', syncFromUrl);
    return () => { window.removeEventListener('popstate', syncFromUrl); window.removeEventListener('hashchange', syncFromUrl); };
  }, []);

  const data = dashboard || emptyDashboard;

  function selectNav(id) { setActiveNav(id); setMenuOpen(false); setActivityFilter('All activity'); window.history.pushState({}, '', `#${id}`); }
  function submitOrder(event) { event.preventDefault(); if (!payAmount || Number(payAmount) <= 0) return; setOrderReview(true); }
  async function recordAction(actionType, detail) {
    try {
      const response = await fetch('/api/actions', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ actionType, detail }) });
      if (!response.ok) throw new Error('The action could not be saved to SQLite.');
      const result = await response.json(); setDashboard(result.dashboard); setWalletNotice(detail);
    } catch (error) { setWalletNotice(error.message); }
  }
  async function completeOrder() {
    try {
      const response = await fetch('/api/orders', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ direction: tradeMode, amountMinor: Math.round(Number(payAmount) * 100) }) });
      if (!response.ok) throw new Error('The simulated order could not be saved to SQLite.');
      const result = await response.json();
      setDashboard(result.dashboard); setOrderReview(false); setOrderComplete(true); setPayAmount('');
    } catch (error) { setOrderReview(false); setWalletNotice(error.message); }
  }

  function renderPage() {
    const props = { data, onNotice: setWalletNotice, onAction: recordAction, onNavigate: selectNav, activityFilter, setActivityFilter };
    if (activeNav === 'custody') return <CustodyView {...props} />;
    if (activeNav === 'stablecoins') return <StablecoinsView {...props} tradeMode={tradeMode} setTradeMode={setTradeMode} payAmount={payAmount} setPayAmount={setPayAmount} onReview={submitOrder} />;
    if (activeNav === 'wallet') return <WalletView {...props} />;
    if (activeNav === 'activity') return <ActivityView {...props} />;
    return <OverviewView {...props} />;
  }

  return <div className="app-shell">
    <a className="skip-link" href="#main-content">Skip to main content</a>
    <header className="masthead"><div className="masthead-inner"><img src="/assets/logos/horizon-bank-wordmark-white.svg" alt="Horizon Bank" className="brand-logo" /><div className="masthead-actions"><button className="icon-button" aria-label="Notifications" onClick={() => setWalletNotice(`${data.activitySummary.pending} pending activity item${data.activitySummary.pending === 1 ? '' : 's'} require review.`)}><BellIcon /></button><button className="profile-button" aria-label="Open profile menu"><UserIcon /><span>Sign off</span></button></div></div><div className="brand-rule" /></header>
    <div className="mobile-bar"><button className="mobile-menu-button" onClick={() => setMenuOpen((open) => !open)} aria-expanded={menuOpen} aria-controls="primary-navigation"><GridIcon /><span>Digital assets</span></button><button className="mobile-signoff" onClick={() => setWalletNotice('Your session is ready to sign off safely.')}>Sign off</button></div>
    <div className="body-frame"><aside className={`sidebar ${menuOpen ? 'sidebar--open' : ''}`} id="primary-navigation" aria-label="Digital assets navigation"><div className="sidebar-title"><GridIcon /><span>Digital assets</span></div><nav className="nav-list">{navItems.map(([id, label, NavIcon]) => <button key={id} className={`nav-item ${activeNav === id ? 'nav-item--active' : ''}`} onClick={() => selectNav(id)} aria-current={activeNav === id ? 'page' : undefined}><NavIcon /><span>{label}</span></button>)}</nav><div className="sidebar-footer"><button className="nav-item" onClick={() => setWalletNotice('Support is available for this design review flow.')}><SupportIcon /><span>Support</span></button><button className="nav-item" onClick={() => setWalletNotice('Your session is ready to sign off safely.')}><SignOutIcon /><span>Sign off</span></button></div></aside>
      <main className="main-content" id="main-content"><div className="content-width">{loadError && <div className="api-error" role="alert">{loadError} Start the local SQLite API with <code>python3 server.py</code>.</div>}{dashboard ? renderPage() : <div className="loading-state" role="status">Loading your digital asset data…</div>}<section className="disclosure" aria-label="Digital asset disclosure"><InfoIcon /><p>Digital assets are not FDIC insured, are not deposits or other obligations of, or guaranteed by Horizon Bank, and are subject to investment risks, including possible loss of principal. <a href="#disclosures">Review important disclosures.</a></p></section><div className="footer-row"><span>Sample data — for design review only</span><a href="#mobile-preview">View on mobile <span className="phone-glyph" aria-hidden="true">▯</span></a></div></div></main></div>
    {walletNotice && <div className="toast" role="status"><span>{walletNotice}</span><button onClick={() => setWalletNotice('')} aria-label="Dismiss notification">×</button></div>}
    {orderReview && <div className="modal-backdrop" role="presentation"><div className="modal" role="dialog" aria-modal="true" aria-labelledby="review-title"><button className="modal-close" onClick={() => setOrderReview(false)} aria-label="Close review">×</button><p className="eyebrow">Review order</p><h2 id="review-title">Confirm your stablecoin {tradeMode}</h2><div className="review-lines"><div><span>{tradeMode === 'buy' ? 'You pay' : 'You sell'}</span><strong>${Number(payAmount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} {tradeMode === 'buy' ? 'USD' : data.asset.symbol}</strong></div><div><span>You receive</span><strong>{Number(payAmount || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} {tradeMode === 'buy' ? data.asset.symbol : 'USD'}</strong></div><div><span>Network</span><strong>{data.asset.network}</strong></div></div><p className="review-note">This is a simulated review step for design review. A final product would show applicable fees, timing, and required disclosures before completion.</p><div className="modal-actions"><button className="horizon-button horizon-button--secondary" onClick={() => setOrderReview(false)}>Go back</button><button className="horizon-button horizon-button--primary" onClick={completeOrder}>Confirm simulated order</button></div></div></div>}
    {orderComplete && <div className="modal-backdrop" role="presentation"><div className="modal modal--success" role="dialog" aria-modal="true" aria-labelledby="complete-title"><div className="success-mark">✓</div><h2 id="complete-title">Order submitted for review</h2><p>Your simulated stablecoin {tradeMode} request is complete for this design review. No real transaction was placed.</p><button className="horizon-button horizon-button--primary" onClick={() => setOrderComplete(false)}>Done</button></div></div>}
  </div>;
}

createRoot(document.getElementById('root')).render(<App />);
