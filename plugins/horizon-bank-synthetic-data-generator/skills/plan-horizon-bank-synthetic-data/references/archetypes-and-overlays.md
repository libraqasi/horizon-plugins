# Archetypes and overlays

Treat archetypes as financial relationship patterns, not predictions about a demographic. Apply channels and overlays independently.

## Customer archetypes

| ID | Relationship pattern | Useful modules |
|---|---|---|
| `youth-guardian` | Youth checking/savings with guardian visibility and approvals | household, guardian, allowance, goals, card controls |
| `emerging-adult` | Student or early-career customer building independent finances | income, checking, savings, credit, education, goals |
| `everyday-banking` | Employed adult using core deposits, bills, card, and savings | accounts, transactions, budgets, rewards, alerts |
| `family-homebuyer` | Household coordinating expenses, emergency savings, and housing | household, mortgage, goals, bills, insurance |
| `affluent-investor` | Relationship customer with deposits, investments, retirement, and service | investments, retirement, rewards, advisor interactions |
| `small-business-owner` | Owner with linked personal and business cash flow | business, business accounts, payroll, credit, service |
| `gig-multi-income` | Customer with variable deposits and irregular expenses | multiple incomes, tax reserve, cash-flow budget, goals |
| `retiree-fixed-income` | Household using fixed income, healthcare planning, and conservative savings | fixed income, investments, healthcare, beneficiaries |
| `agentic-digital-wallet` | Customer delegating bounded purchases to software agents and wallets | devices, wallet, delegations, approvals, authorization events |

## Composable overlays

- `payday`: post a scheduled income deposit.
- `low-balance`: leave the primary checking account below its configured cushion.
- `overdraft-risk`: add an upcoming debit that would cross the cushion or zero.
- `pending-card-charge`: add a visible pending card transaction excluded from posted balance.
- `card-dispute`: reference a posted transaction with an open dispute.
- `fraud-review`: create a review event and restrained account alert.
- `missed-payment`: mark a loan/card payment late without inventing legal outcomes.
- `travel`: add travel spending and a travel-aware alert or card event.
- `move-home`: add deposit, rent, mortgage, or address-change planning context.
- `job-change`: change an income stream at a clear effective date.
- `healthcare-expense`: add a healthcare debit and budget impact.
- `new-dependent`: add a household relationship and planning goal.

## Selection rules

- Include one of each archetype in the default small dataset.
- Use explicit weights for medium and large datasets.
- Give overlays stable event IDs and link them to affected customers, accounts, and transactions.
- Do not use age, gender, language, ethnicity, immigration history, disability, or family status to calculate rates, risk, creditworthiness, fraud, or eligibility.
- Use multilingual, remittance, accessibility, and life-event needs as optional experience overlays when the journey requires them.
