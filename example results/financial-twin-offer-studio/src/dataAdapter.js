const currency = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD', maximumFractionDigits: 0});
const TWIN_PLANNING_SCALE = 100;

export const money = (minor = 0) => currency.format(minor / 100);

export function getPortfolio(bundle) {
  const customer = bundle.customers?.[0];
  const checking = bundle.accounts?.find((account) => account.type === 'checking');
  const savings = bundle.accounts?.find((account) => account.type === 'savings');
  const card = bundle.cards?.[0];
  const goal = bundle.goals?.[0];
  const rewards = bundle.rewards?.[0];

  return {customer, checking, savings, card, goal, rewards, scenarioDate: bundle.metadata?.scenario_date, goalProgress: goal ? Math.min(100, Math.round((goal.current_minor / goal.target_minor) * 100)) : 0};
}

export function flattenTwinEvents(catalog) {
  return catalog.chapters.flatMap((chapter) => chapter.events.map((event) => ({...event, chapterId: chapter.id, chapterTitle: chapter.title, chapterMonths: chapter.months})));
}

export function getTwinPathway(catalog, pathwayId) {
  return catalog.pathways.find((pathway) => pathway.id === pathwayId) || catalog.pathways[0];
}

export function createTwinState(portfolio, pathwayId) {
  return {
    pathwayId,
    month: 1,
    cashMinor: Math.max(0, portfolio.checking?.posted_balance_minor || 0) * TWIN_PLANNING_SCALE,
    goalMinor: (portfolio.goal?.current_minor || 0) * TWIN_PLANNING_SCALE,
    goalTargetMinor: (portfolio.goal?.target_minor || 100000) * TWIN_PLANNING_SCALE,
    rewards: portfolio.rewards?.available_points || 0,
    preparedness: 52,
    ledger: [],
    undo: null,
  };
}

export function getChoiceEffects(choice, pathway, event) {
  const base = choice.effects || {};
  const isMatch = pathway.match_tags?.includes(event.tag);
  const modifier = isMatch ? pathway.modifier || {} : {};
  return {
    cash_minor: ((base.cash_minor || 0) + (modifier.cash_minor || 0)) * TWIN_PLANNING_SCALE,
    goal_minor: ((base.goal_minor || 0) + (modifier.goal_minor || 0)) * TWIN_PLANNING_SCALE,
    rewards: (base.rewards || 0) + (modifier.rewards || 0),
    preparedness: (base.preparedness || 0) + (modifier.preparedness || 0),
  };
}

export function applyTwinChoice(state, event, choice, pathway) {
  const effects = getChoiceEffects(choice, pathway, event);
  const before = {cashMinor: state.cashMinor, goalMinor: state.goalMinor, rewards: state.rewards, preparedness: state.preparedness, month: state.month};
  const record = {eventId: event.id, eventTitle: event.title, chapterId: event.chapterId, chapterTitle: event.chapterTitle, month: event.month, choiceId: choice.id, choiceLabel: choice.label, choiceBody: choice.body, effects, alternatives: event.choices.filter((item) => item.id !== choice.id)};
  return {
    ...state,
    month: Math.min(12, event.month + 1),
    cashMinor: Math.max(0, state.cashMinor + effects.cash_minor),
    goalMinor: Math.max(0, state.goalMinor + effects.goal_minor),
    rewards: Math.max(0, state.rewards + effects.rewards),
    preparedness: Math.max(0, Math.min(100, state.preparedness + effects.preparedness)),
    ledger: [...state.ledger, record],
    undo: {before, record},
  };
}

export function undoTwinChoice(state) {
  if (!state.undo) return state;
  const {before} = state.undo;
  return {...state, ...before, ledger: state.ledger.slice(0, -1), undo: null};
}

export function getTwinRecap(state) {
  const goalProgress = Math.min(100, Math.round((state.goalMinor / state.goalTargetMinor) * 100));
  const alternate = state.ledger.map((record) => {
    const lighterCash = [...record.alternatives].sort((a, b) => (b.effects.cash_minor || 0) - (a.effects.cash_minor || 0))[0];
    return lighterCash ? {eventTitle: record.eventTitle, choiceLabel: lighterCash.label, cashDifference: (lighterCash.effects.cash_minor || 0) - record.effects.cash_minor} : null;
  }).filter(Boolean).sort((a, b) => b.cashDifference - a.cashDifference)[0];
  return {goalProgress, alternate};
}

export function delta(value, kind = 'money') {
  if (!value) return 'No change';
  const sign = value > 0 ? '+' : '−';
  if (kind === 'money') return `${sign}${money(Math.abs(value))}`;
  if (kind === 'points') return `${sign}${Math.abs(value).toLocaleString()} pts`;
  return `${sign}${Math.abs(value)} pts`;
}
