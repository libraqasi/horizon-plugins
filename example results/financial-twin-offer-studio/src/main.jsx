import React, {useEffect, useMemo, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {ArrowLeft, ArrowRight, BadgeCheck, Check, ChevronDown, ChevronRight, CreditCard, EyeOff, Landmark, LockKeyhole, PiggyBank, Play, RotateCcw, ShieldCheck, SlidersHorizontal, Sparkles, Target, Trophy, WalletCards, X} from 'lucide-react';
import {applyTwinChoice, createTwinState, delta, flattenTwinEvents, getChoiceEffects, getPortfolio, getTwinPathway, getTwinRecap, money, undoTwinChoice} from './dataAdapter';
import './styles.css';

const goals = [
  {id: 'rewards', label: 'Make everyday spending go further', icon: CreditCard},
  {id: 'travel', label: 'Plan for travel and dining', icon: Sparkles},
  {id: 'safety', label: 'Build a stronger cash cushion', icon: PiggyBank},
  {id: 'interest', label: 'Understand lower-interest options', icon: WalletCards},
];

const rhythms = ['I want a quick starting point', 'I like to compare details', 'I am planning ahead'];

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [goal, setGoal] = useState('rewards');
  const [rhythm, setRhythm] = useState(rhythms[0]);
  const [shared, setShared] = useState({relationship: true, goals: true, spending: false, preferences: false});
  const [detail, setDetail] = useState(null);

  useEffect(() => {
    Promise.all([fetch('/data/bundle.json'), fetch('/data/financial-twin.json')])
      .then(async ([bundleResponse, twinResponse]) => {
        if (!bundleResponse.ok || !twinResponse.ok) throw new Error('The local simulation data is unavailable.');
        return {bundle: await bundleResponse.json(), twin: await twinResponse.json()};
      })
      .then(setData)
      .catch((loadError) => setError(loadError.message));
  }, []);

  const portfolio = useMemo(() => data && getPortfolio(data.bundle), [data]);
  const sharedCount = Object.values(shared).filter(Boolean).length;
  const toggleShared = (key) => setShared((current) => ({...current, [key]: !current[key]}));
  const goTo = (id) => document.getElementById(id)?.scrollIntoView({behavior: 'smooth', block: 'start'});

  if (error) return <LoadingState error={error}/>;
  if (!portfolio || !data) return <LoadingState/>;

  return <div className="offer-app">
    <a className="skip-link" href="#main">Skip to Financial Twin</a>
    <header className="brand-frame">
      <div className="masthead">
        <button className="wordmark-button" onClick={() => goTo('main')} aria-label="Horizon Bank Financial Twin home"><img src="/assets/horizon-bank-logo-horizontal-white.svg" alt="Horizon Bank"/></button>
        <nav aria-label="Offer Studio navigation"><button onClick={() => goTo('discover')}>Discover</button><button onClick={() => goTo('data-controls')}>Your data</button><button onClick={() => goTo('twin')}>Financial Twin</button></nav>
        <button className="profile-button" onClick={() => goTo('data-controls')}><span className="profile-dot" aria-hidden="true"/><span>{portfolio.customer.name.first}</span><ChevronDown aria-hidden="true"/></button>
      </div>
      <div className="brand-rule"/>
    </header>

    <main id="main">
      <section className="hero twin-hero" aria-labelledby="hero-title">
        <div className="hero-copy"><p className="eyebrow"><Sparkles aria-hidden="true"/> Financial Twin</p><h1 id="hero-title">Play out a year of choices before you make one.</h1><p className="hero-lede">Choose a product pathway, step through a life season, and see how tradeoffs can move a simulated cash cushion, goal, and rewards balance.</p><div className="hero-actions"><button className="button-primary" onClick={() => goTo('twin')}>Enter Financial Twin <Play/></button><button className="button-link" onClick={() => goTo('discover')}>Set my starting focus <ChevronRight/></button></div><p className="hero-note"><LockKeyhole aria-hidden="true"/> This is a local educational simulation. It does not show actual terms, savings, rewards, eligibility, or account activity.</p></div>
        <div className="hero-visual twin-hero-visual" role="img" aria-label="A horizon and roadway representing a financial journey"><div className="hero-card hero-card-top"><span>12-month life season</span><strong>8 moments. Your choices. One clear recap.</strong></div><div className="hero-card hero-card-bottom"><Target aria-hidden="true"/><span>Start with your real goals in view</span></div></div>
      </section>

      <section className="progress-band" aria-label="Financial Twin stages"><div><span className="progress-number">01</span><strong>Choose a focus</strong><small>Set the lens for your life season.</small></div><div><span className="progress-number">02</span><strong>Set your data controls</strong><small>Choose context for your starting view.</small></div><div><span className="progress-number">03</span><strong>Play Financial Twin</strong><small>Review tradeoffs chapter by chapter.</small></div></section>

      <section className="discovery-section section-shell" id="discover" aria-labelledby="discover-title"><div className="section-intro"><p className="eyebrow">Step 1 of 3</p><h2 id="discover-title">What would you like to plan for?</h2><p>Your focus guides the simulator introduction. You can still choose any product pathway inside Financial Twin.</p></div><div className="goal-grid" role="radiogroup" aria-label="Financial Twin focus">{goals.map((item) => {const Icon = item.icon; const selected = goal === item.id; return <button key={item.id} className={`goal-option ${selected ? 'selected' : ''}`} onClick={() => setGoal(item.id)} role="radio" aria-checked={selected}><span className="goal-icon"><Icon aria-hidden="true"/></span><span>{item.label}</span>{selected && <Check aria-label="Selected"/>}</button>;})}</div><div className="rhythm-row"><div><strong>How do you want to play?</strong><span>Your selection sets the level of narrative detail, not actual financial terms.</span></div><div className="rhythm-options">{rhythms.map((item) => <button key={item} className={rhythm === item ? 'selected' : ''} onClick={() => setRhythm(item)} aria-pressed={rhythm === item}>{item}</button>)}</div></div></section>

      <section className="data-section" id="data-controls" aria-labelledby="data-title"><div className="section-shell data-layout"><div className="data-intro"><p className="eyebrow">Step 2 of 3</p><h2 id="data-title">Choose the context behind your starting view.</h2><p>These controls shape the simulation’s opening snapshot and explanations. You can change or revoke them at any time.</p><button className="button-link data-link" onClick={() => setDetail({type: 'privacy'})}>How data controls work <ChevronRight/></button></div><div className="context-panel"><div className="context-panel-head"><div><span className="eyebrow">Your context</span><strong>{sharedCount} of 4 choices active</strong></div><span className="context-badge"><ShieldCheck aria-hidden="true"/> You decide</span></div><ContextControl icon={<Landmark/>} title="Horizon relationship" body={`Account types and balances from ${portfolio.checking.product_name} and ${portfolio.savings.product_name}.`} checked={shared.relationship} onChange={() => toggleShared('relationship')}/><ContextControl icon={<PiggyBank/>} title="Savings goals" body={`${portfolio.goal.name} progress and goal timing.`} checked={shared.goals} onChange={() => toggleShared('goals')}/><ContextControl icon={<CreditCard/>} title="Spending themes" body="High-level category totals, not merchant-level purchase history." checked={shared.spending} onChange={() => toggleShared('spending')}/><ContextControl icon={<SlidersHorizontal/>} title="Your stated preferences" body="The focus and play style you choose in this experience." checked={shared.preferences} onChange={() => toggleShared('preferences')}/></div></div><div className="section-shell privacy-boundary"><EyeOff aria-hidden="true"/><div><strong>Social profiles and inboxes are not part of Financial Twin.</strong><p>We do not use social or inbox content to set terms, determine eligibility, or shape pricing. This local simulation uses only the controls shown above.</p></div><button className="button-secondary" onClick={() => setDetail({type: 'privacy'})}>Learn why</button></div></section>

      <section className="portfolio-strip section-shell" aria-label="Starting portfolio snapshot"><div className="portfolio-title"><span className="eyebrow">Your Financial Twin starting point</span><strong>Portfolio snapshot</strong><small>As of {portfolio.scenarioDate}</small></div><Metric label={portfolio.checking.product_name} value={money(portfolio.checking.posted_balance_minor)} detail={`Ending ${portfolio.checking.display_last4}`}/><Metric label={portfolio.goal.name} value={`${portfolio.goalProgress}%`} detail={`${money(portfolio.goal.current_minor)} of ${money(portfolio.goal.target_minor)}`}/><Metric label={portfolio.rewards.program} value={`${portfolio.rewards.available_points.toLocaleString()} pts`} detail="Starting simulation value"/></section>

      <FinancialTwin id="twin" portfolio={portfolio} catalog={data.twin} sharedCount={sharedCount} goal={goal}/>
    </main>

    <footer><img src="/assets/horizon-bank-logo-horizontal-white.svg" alt="Horizon Bank"/><span>Financial Twin uses local synthetic data and an illustrative scenario catalog for this prototype.</span><button onClick={() => goTo('main')}>Back to top</button></footer>
    {detail && <DetailDialog detail={detail} onClose={() => setDetail(null)}/>}
  </div>;
}

function FinancialTwin({id, portfolio, catalog, sharedCount, goal}) {
  const [phase, setPhase] = useState('setup');
  const [pathwayId, setPathwayId] = useState(catalog.pathways[0].id);
  const [twinState, setTwinState] = useState(null);
  const [eventIndex, setEventIndex] = useState(0);
  const [pendingChoice, setPendingChoice] = useState(null);
  const [showBasis, setShowBasis] = useState(false);
  const events = useMemo(() => flattenTwinEvents(catalog), [catalog]);
  const pathway = getTwinPathway(catalog, pathwayId);
  const activeEvent = events[eventIndex];
  const recap = twinState ? getTwinRecap(twinState) : null;

  const start = () => {setTwinState(createTwinState(portfolio, pathwayId)); setEventIndex(0); setPendingChoice(null); setPhase('play');};
  const confirmChoice = () => {
    if (!pendingChoice || !activeEvent || !twinState) return;
    const nextState = applyTwinChoice(twinState, activeEvent, pendingChoice, pathway);
    setTwinState(nextState); setPendingChoice(null);
    if (eventIndex === events.length - 1) setPhase('recap'); else setEventIndex((value) => value + 1);
  };
  const undo = () => {
    const latest = twinState?.ledger.at(-1); const nextEvent = events[eventIndex];
    if (!latest || !nextEvent || latest.chapterId !== nextEvent.chapterId) return;
    setTwinState(undoTwinChoice(twinState)); setEventIndex((value) => Math.max(0, value - 1));
  };
  const replay = () => {setTwinState(createTwinState(portfolio, pathwayId)); setEventIndex(0); setPendingChoice(null); setPhase('play');};

  return <section className="financial-twin" id={id} aria-labelledby="twin-title">
    {phase === 'setup' && <div className="section-shell twin-setup"><div className="twin-setup-copy"><p className="eyebrow">Step 3 of 3</p><h2 id="twin-title">Choose your product lens, then enter the year.</h2><p>Each pathway changes a few simulated moments so you can compare how features might feel in a particular kind of year.</p><div className="twin-disclosure"><BadgeCheck aria-hidden="true"/><span>{catalog.disclosure}</span></div></div><div className="pathway-grid" role="radiogroup" aria-label="Financial Twin product pathway">{catalog.pathways.map((item) => {const selected = pathwayId === item.id; return <button className={`pathway-card ${selected ? 'selected' : ''} ${item.accent}`} key={item.id} onClick={() => setPathwayId(item.id)} role="radio" aria-checked={selected}><span>{item.eyebrow}</span><strong>{item.name}</strong><small>{item.description}</small>{selected && <Check aria-label="Selected"/>}</button>;})}</div><div className="twin-launch"><div><span>Selected life focus</span><strong>{goals.find((item) => item.id === goal)?.label}</strong></div><button className="button-primary" onClick={start}>Start my 12-month season <Play/></button></div></div>}
    {phase === 'play' && twinState && <TwinPlay state={twinState} pathway={pathway} event={activeEvent} events={events} index={eventIndex} pendingChoice={pendingChoice} setPendingChoice={setPendingChoice} confirmChoice={confirmChoice} undo={undo} showBasis={showBasis} setShowBasis={setShowBasis} sharedCount={sharedCount}/>} 
    {phase === 'recap' && twinState && recap && <TwinRecap state={twinState} pathway={pathway} recap={recap} replay={replay} restart={() => setPhase('setup')}/>} 
  </section>;
}

function TwinPlay({state, pathway, event, events, index, pendingChoice, setPendingChoice, confirmChoice, undo, showBasis, setShowBasis, sharedCount}) {
  const effects = pendingChoice ? getChoiceEffects(pendingChoice, pathway, event) : null;
  const canUndo = state.undo && events[index]?.chapterId === state.undo.record.chapterId;
  return <div className="twin-play section-shell"><div className="twin-heading"><div><p className="eyebrow">Financial Twin / Month {event.month} of 12</p><h2>{event.chapterTitle}</h2><p>{event.chapterMonths} · {event.chapterTitle === 'Starting point' ? 'Build your baseline.' : 'See how this moment can move your year.'}</p></div><button className="button-secondary" onClick={() => setShowBasis((value) => !value)}>What is this based on? <ChevronDown className={showBasis ? 'rotate' : ''}/></button></div>{showBasis && <div className="twin-basis"><ShieldCheck aria-hidden="true"/><div><strong>Your selected context is visible, not decisive.</strong><p>{sharedCount} data controls are on. Financial Twin starts from your local Horizon snapshot and uses a fixed scenario catalog. It does not use live account activity or set product terms.</p></div></div>}
    <TwinHud state={state} pathway={pathway} index={index} total={events.length}/>
    <div className="twin-layout"><aside className="twin-timeline" aria-label="Life season timeline">{events.map((item, itemIndex) => <div className={`timeline-item ${itemIndex === index ? 'active' : ''} ${itemIndex < index ? 'complete' : ''}`} key={item.id}><span>{itemIndex < index ? <Check aria-label="Completed"/> : String(item.month).padStart(2, '0')}</span><div><strong>{item.title}</strong><small>{item.chapterTitle}</small></div></div>)}</aside><div className="event-stage"><div className="event-kicker"><span>Month {event.month}</span><span>{event.chapterTitle}</span></div><h3>{event.title}</h3><p>{event.body}</p><div className="choice-stack" aria-label="Choose a response">{event.choices.map((choice) => {const selected = pendingChoice?.id === choice.id; const preview = getChoiceEffects(choice, pathway, event); return <button className={`twin-choice ${selected ? 'selected' : ''}`} key={choice.id} onClick={() => setPendingChoice(choice)} aria-pressed={selected}><span><strong>{choice.label}</strong><small>{choice.body}</small></span><EffectSummary effects={preview}/>{selected && <Check aria-label="Selected"/>}</button>;})}</div></div><aside className="choice-review"><p className="eyebrow">Review your choice</p>{pendingChoice && effects ? <><h3>{pendingChoice.label}</h3><p>{pendingChoice.body}</p><EffectList effects={effects}/><button className="button-primary" onClick={confirmChoice}>Confirm this choice <ArrowRight/></button><button className="button-link" onClick={() => setPendingChoice(null)}>Choose another response</button></> : <><h3>Pick a response to preview it.</h3><p>Every option shows its simulated effect before you confirm it.</p></>}{canUndo && <button className="undo-button" onClick={undo}><RotateCcw/> Undo my last choice</button>}</aside></div></div>;
}

function TwinHud({state, pathway, index, total}) {const goalProgress = Math.min(100, Math.round((state.goalMinor / state.goalTargetMinor) * 100)); return <div className="twin-hud"><div><span>Season progress</span><strong>{index + 1} / {total}</strong><small>moments revealed</small></div><div><span>Cash cushion</span><strong>{money(state.cashMinor)}</strong><small>simulated balance</small></div><div><span>Goal progress</span><strong>{goalProgress}%</strong><small>{money(state.goalMinor)} toward goal</small></div><div><span>Rewards</span><strong>{state.rewards.toLocaleString()} pts</strong><small>{pathway.name}</small></div><div><span>Preparedness</span><strong>{state.preparedness}/100</strong><small>simulated position</small></div></div>}

function EffectSummary({effects}) {return <span className="effect-summary"><b>{delta(effects.cash_minor)}</b><small>cash</small></span>}
function EffectList({effects}) {return <div className="effect-list"><div><span>Cash cushion</span><strong>{delta(effects.cash_minor)}</strong></div><div><span>Goal</span><strong>{delta(effects.goal_minor)}</strong></div><div><span>Rewards</span><strong>{delta(effects.rewards, 'points')}</strong></div><div><span>Preparedness</span><strong>{delta(effects.preparedness, 'score')}</strong></div></div>}

function TwinRecap({state, pathway, recap, replay, restart}) {return <div className="section-shell twin-recap"><div className="recap-hero"><div><p className="eyebrow"><Trophy/> Your year in review</p><h2>You made a season of tradeoffs, not perfect choices.</h2><p>Here is the simulated position created by your decisions and the product lens you chose.</p></div><div className="recap-pathway"><span>Saved pathway</span><strong>{pathway.name}</strong><small>{pathway.eyebrow}</small></div></div><div className="recap-metrics"><Metric label="Cash cushion" value={money(state.cashMinor)} detail="simulated ending balance"/><Metric label="Goal progress" value={`${recap.goalProgress}%`} detail={`${money(state.goalMinor)} of ${money(state.goalTargetMinor)}`}/><Metric label="Rewards" value={`${state.rewards.toLocaleString()} pts`} detail="simulated point balance"/><Metric label="Preparedness" value={`${state.preparedness}/100`} detail="simulated position"/></div><div className="recap-grid"><section className="choice-ledger"><p className="eyebrow">Your decision timeline</p><h3>What you chose</h3>{state.ledger.map((record) => <div className="ledger-row" key={record.eventId}><span>Month {record.month}</span><div><strong>{record.eventTitle}</strong><small>{record.choiceLabel}</small></div><b>{delta(record.effects.cash_minor)}</b></div>)}</section><aside className="tradeoff-card"><p className="eyebrow">One tradeoff to revisit</p><h3>{recap.alternate ? recap.alternate.eventTitle : 'Your choices are in balance'}</h3><p>{recap.alternate ? `${recap.alternate.choiceLabel} would have changed the immediate cash result by ${delta(recap.alternate.cashDifference)}. That does not make it better—only a different tradeoff.` : 'Your simulation did not surface a single clear alternate cash tradeoff.'}</p><div className="twin-disclosure"><BadgeCheck aria-hidden="true"/><span>These figures come from the local scenario rules, not actual product terms or savings estimates.</span></div></aside></div><div className="recap-actions"><button className="button-primary" onClick={replay}>Replay with a different strategy <RotateCcw/></button><button className="button-secondary" onClick={restart}>Choose another product lens <ArrowLeft/></button></div></div>}

function ContextControl({icon, title, body, checked, onChange}) {return <div className="context-control"><div className="context-icon" aria-hidden="true">{icon}</div><div className="context-copy"><strong>{title}</strong><span>{body}</span></div><label className="switch-label"><span className="sr-only">Share {title}</span><input type="checkbox" checked={checked} onChange={onChange}/><span className="switch" aria-hidden="true"/></label></div>;}
function Metric({label, value, detail}) {return <div className="metric"><span>{label}</span><strong>{value}</strong><small>{detail}</small></div>;}
function DetailDialog({detail, onClose}) {return <div className="dialog-backdrop" role="presentation"><section className="dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title"><button className="dialog-close" onClick={onClose} aria-label="Close dialog"><X/></button><div className="dialog-icon"><LockKeyhole/></div><p className="eyebrow">You are in control</p><h2 id="dialog-title">Your privacy boundary</h2><p>This experience uses the local Horizon information you explicitly switch on and the choices you make here. Social profiles and inboxes are intentionally excluded from product terms, pricing, and eligibility.</p><button className="button-primary" onClick={onClose}>Got it <ArrowRight/></button></section></div>;}
function LoadingState({error}) {return <main className="loading-state"><img src="/assets/horizon-bank-logo-horizontal.svg" alt="Horizon Bank"/><h1>{error ? 'We could not load Financial Twin' : 'Preparing Financial Twin'}</h1><p>{error || 'Loading your local simulation data…'}</p>{error && <button className="button-primary" onClick={() => window.location.reload()}>Try again</button>}</main>;}

createRoot(document.getElementById('root')).render(<App/>);
