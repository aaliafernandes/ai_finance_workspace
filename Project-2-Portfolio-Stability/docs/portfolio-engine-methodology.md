# Phase 3B portfolio-engine methodology

This is educational coursework, not investment advice. The engine produces gross historical analytics and rule-level evidence statuses. It does not produce a committee recommendation.

## Approved input boundary

The engine accepts only `data/processed/approved_monthly_prices.csv`. Its loader rejects every other path and requires the exact headers `PeriodLabel,BIL,IEF,LQD,VT`, first-of-month source labels, positive finite values, ascending unique monthly labels, and no missing month. The source-label date is not described as a month-end close or a tradable execution price. The preserved raw JSON and defective `data/processed/prices.csv` remain evidence only.

## Portfolios and rebalance convention

The three displayed strategies are equal weight (25% each), the 0% BIL / 0% IEF / 40% LQD / 60% VT policy benchmark, and a long-only BIL/IEF/LQD/VT constrained minimum-volatility portfolio on a 5-percentage-point grid.

At the first approved source label, the engine applies target weights from the explicitly hypothetical 60% VT / 40% LQD starting allocation and records the initial one-way turnover. Returns then accrue from each source label to the next while units remain unchanged. Before the interval beginning at the matching source-label month in each subsequent year, it computes drifted weights from current units and prices, records turnover, and resets units to target weights. Thus there is one initial trade and annual rebalances; there is no monthly constant-weight rebalancing.

One-way turnover is `0.5 × sum(abs(target weight − pre-trade weight))`. The initial pre-trade weights are hypothetical rather than evidence of Meridian's holdings. A candidate must have turnover no greater than 25% at every modeled event when that constraint is applied.

## Gross analytics

All calculations use decimal returns; reported percentages are decimal values times 100. Costs and taxes are excluded, so no net-performance claim is made.

- Monthly portfolio return: portfolio value at next source label divided by value at the current source label, minus one.
- Gross geometric annualized return: `(product(1 + monthly return))^(12/n) − 1`, with `n` monthly returns.
- Sample annualized volatility: monthly sample standard deviation (`n − 1` denominator) times `sqrt(12)`.
- Annualized zero-target downside deviation: `sqrt(sum(min(0, monthly return)^2) / n) × sqrt(12)`.
- Maximum drawdown: the minimum of cumulative wealth divided by its prior running peak minus one, beginning wealth at 1.00.
- Calendar-year gross return: the compounded 12 monthly returns whose intervals end January through December of that calendar year. Partial years are excluded.

## Grid objective and feasibility

The optimizer enumerates all long-only four-ETF weights on the 5% grid that sum to 100%. It ranks a feasible candidate by the annualized sample volatility of its **realized annual-rebalance path**, not a covariance approximation. It uses that identical path-volatility definition in the candidate rank field, reported analytics, and deterministic test. Ties use: (1) lower volatility, (2) lower sum of modeled turnover events, then (3) lexicographic BIL/IEF/LQD/VT weights.

An optional 10% BIL floor is separately labelled as a student-proposed scenario. It is not added to the mandate. If no candidate satisfies the mathematical constraints, the engine returns `INFEASIBLE`; it does not select a fallback.

## Verdict boundary

`src/mandate_verdicts.py` marks the approved universe, long-only status, 100% weight sum, and turnover as PASS or FAIL where arithmetic is available. It keeps these conditions UNVERIFIED: 3% reserve eligibility, 90% redemption, issuer concentration/look-through, CPI + 4% net five-year objective, net calendar-year loss trigger, and credit-spread rule. An UNVERIFIED condition cannot become PASS or make a portfolio decision-ready.

ETF expense ratios are not subtracted from adjusted-close returns because doing so could double count embedded fund expenses. Transaction-cost deductions remain blocked until the Phase 2B cost-ledger evidence requirements are met.

## Validation scope and limitations

The tests cover exact input boundary and headers, known-return/risk arithmetic, initial and drift turnover, no fallback for an infeasible grid, deterministic selection, and verdict behavior. A two-asset 80%/20% theoretical minimum-variance calculation is included only as a covariance sanity check; it is explicitly not the production selection objective. Historical results do not establish future performance, liquidity, tradability, mandate compliance, or a recommendation.
