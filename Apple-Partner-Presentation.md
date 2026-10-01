# Apple Partner Presentation — FIN 43900

**Presenter:** [Your name] (A or B)  
**Reviewer:** [Partner's name] (B or A)  
**Company:** Apple Inc. (NASDAQ: AAPL)  
**Valuation date / currency / share basis:** September 10, 2026; USD; diluted EPS/share basis where stated.  
**Purpose:** Educational coursework only; not personalized investment advice.

## Opening — current conclusion (about 1 minute)

> My current conclusion is **Watch — defer initiation**. Apple has a durable ecosystem, profitable Services growth, and strong reported earnings, but my DCF is not yet a defensible fair-value estimate because its starting FCFF and WACC are unresolved. My qualified peer P/E exercise produces a **$204.66–$229.32 per-share reference range**, below the **$326.57** September 10, 2026 market close, but the peers have different economic engines. I will not average that range with the broken DCF.

> I will show how I got there, the assumptions that matter most, and the evidence that could change my mind.

---

## Stop 1 — Target selection: why Apple?

**Show:** `Apple proforma.md` — company and initial-thesis sections.

> I selected Apple because it combines a hardware ecosystem with recurring Services revenue. The important question was whether its installed base and higher-margin Services business could support durable cash-flow growth, while still recognizing risks from product demand, regulation, China exposure, competition, and supply-chain costs.

> My initial view was Watch — defer initiation, not because Apple lacks quality, but because quality alone does not establish an attractive valuation-adjusted return.

**Evidence to point to:** Apple FY2025 total sales were $416.161 billion, up 6%; Services sales were $109.158 billion, up 14%.

## Stop 2 — Company and evidence: how Apple earns money

**Show:** `Apple proforma.md` evidence table, or Apple FY2025 Form 10-K, MD&A and statements.

> Apple earns most revenue from products—iPhone, Mac, iPad, wearables, and accessories—and also earns recurring Services revenue from areas such as the App Store, advertising, cloud, subscriptions, AppleCare, and payments.

> The key operating driver in my analysis is Services. In FY2025 it grew faster than total sales, and its gross margin was **75.4%**, compared with **36.8%** for Products. That does not mean Services growth will continue forever, but it explains why Services mix can support consolidated profitability.

**Source, period, units:** Apple FY2025 Form 10-K, fiscal year ended September 27, 2025, filed October 31, 2025; USD millions except per-share figures.

## Stop 3 — Pro-forma: how history becomes a forecast

**Show:** `Lab-11-Apple/Lab-11-Part-R-Apple.md`, then `Lab-11-Apple/apple_proforma_sensitivity.py`.

> I started from FY2025 revenue of **$416,161 million** and operating income of **$133,050 million**, which is roughly a **32% operating margin**. My base revenue-growth path is **6%, 5%, 4%, 3%, and 3%** over Years 1–5. My base operating margin is **32%** each year.

> These are judgment assumptions, not company guidance. The revenue-growth path starts with reported FY2025 6% growth and tapers because Apple is already very large. The margin range reflects possible changes in Services mix, product mix, pricing, and operating costs.

> The model links revenue → operating profit → FCFF proxy. The FCFF proxy uses FY2025 operating cash flow less capex: $111,482 million minus $12,715 million, before the unresolved cash-interest-paid add-back. This is an operating forecast, not a full linked three-statement model, so a balance-sheet check does not apply; the revenue-to-profit and profit-to-cash-flow links do pass.

## Stop 4 — Valuation: what I can and cannot support

**Show:** `Lab-08-Deal-Evidence-and-Valuation-Triangulation-Apple.md` — DCF comparison and conditional conclusion.

> My DCF uses a 3% terminal-growth estimate, but its saved output of **negative $4.08 per diluted share** is **not** an Apple valuation conclusion. It used a $100 million starting-FCFF training placeholder and a 10% WACC training placeholder. That FCFF input is far too small relative to Apple’s reported cash flow, which creates a scale mismatch. I documented the problem rather than changing inputs to force a market-like result.

> My useful valuation evidence is therefore the qualified peer P/E exercise. Microsoft and Alphabet met my pre-set platform, Services, scale, and profitability policy, but neither is a close Apple substitute: Microsoft has more enterprise-cloud exposure and Alphabet has mainly advertising-driven economics.

> Their September 10, 2026 P/E multiples imply an Apple reference range of **$204.66–$229.32 per share**, with a median of **$216.99**, versus Apple’s same-date close of **$326.57**. This is a reference range, not fair value; it is not averaged with the unusable DCF.

**If asked about reverse DCF:** The existing DCF could not reach its $315.34 target price within a uniform –5 to +10 percentage-point shift to the explicit growth rates while holding FCFF, WACC, terminal growth, cash, debt, and shares fixed. That result mainly demonstrates the placeholder scale problem, not mispricing.

## Stop 5 — Sensitivity and drivers: what moves the forecast

**Show:** `Lab-11-Apple/Lab-11-Part-I-Apple.md` and `Lab-11-Apple/Lab-11-Part-E-Apple.md`.

> I tested one input at a time, keeping every other independent input at base. Revenue-growth paths were lower 4/3/2/1/1%, base 6/5/4/3/3%, and higher 8/7/6/5/5%. Operating-margin cases were 30%, 32%, and 34% each year.

> Over these selected ranges, total revenue growth had the larger effect:

| Driver | Final-year operating-profit span | Final-year FCFF-proxy span |
|---|---:|---:|
| Revenue growth | $31,416.0M | $23,321.0M |
| Operating margin | $20,442.0M | $15,174.7M |

> Here is the calculation trace for the higher revenue-growth case. Final-year revenue increases from **$511,051.1M** to **$562,022.1M**. With margin held at 32%, operating profit rises from **$163,536.4M** to **$179,847.1M**, a **$16,310.7M** increase. The fixed conversion then raises the FCFF proxy from **$121,397.9M** to **$133,505.9M**, a **$12,107.9M** increase.

> The ranking does **not** prove revenue growth is always Apple’s most important driver. It reflects these five-year compounded paths and the ranges I chose. Value per share is unavailable in the sensitivity because a valid FCFF valuation and dated WACC have not yet been built.

## Stop 6 — Interpretation: conclusion, changes of mind, and next evidence

**Show:** `Lab-08-Deal-Evidence-and-Valuation-Triangulation-Apple.md` conclusion.

> I began with a qualitative Watch view. The later work makes that conclusion more specific: Apple’s operating evidence is strong, and revenue growth is the larger tested driver of forecast operating profit and the FCFF proxy. However, the valuation evidence remains incomplete. The peer range is below the saved market price but is only a qualified comparison, and the DCF cannot corroborate it.

> I therefore keep **Watch — defer initiation**. The first assumption I would research next is a fully sourced, consistently scaled starting FCFF, including the cash-interest-paid treatment, followed by a dated WACC. I would also investigate Services durability, particularly regulatory pressure on the App Store and advertising, as well as product demand and Greater China.

> Evidence that would change my mind includes: a repaired DCF with sourced FCFF and WACC that overlaps—or clearly conflicts with—the peer reference range; evidence of sustained Services deceleration or margin pressure; or stronger evidence that a more directly comparable hardware-and-services peer supports a different valuation conclusion.

---

## Reviewer question prompts for your partner (10 minutes)

Ask and record at least one of each:

1. **Selection and evidence:** “Why does Services matter to Apple’s valuation, and can you show me the cited FY2025 source for its 14% growth or 75.4% gross margin?”
2. **Model and valuation:** “Trace the higher revenue-growth case from revenue through operating profit and FCFF proxy. Why should I not treat the negative $4.08 DCF output as Apple’s value?”
3. **Sensitivity and interpretation:** “Could revenue growth rank first because of your selected ranges and compounding? What evidence would change your Watch conclusion?”

**One evidence check to complete together:** Open `Lab-11-Apple/Lab-11-Part-V-Apple.md` and recompute: $179,847.1M − $163,536.4M = **+$16,310.7M**. Confirm that operating margin remains 32% in the base and higher-revenue cases.

## Explain-back and feedback record (5 minutes)

**Ask your partner to say:**

> “Your conclusion is Watch — defer initiation. Your main tested driver is revenue growth over your chosen ranges. Your biggest limitation is that the DCF has unresolved, mismatched FCFF and an unresolved WACC, so the peer P/E result is only a qualified reference.”

**Record their feedback:**

- Strength supported by evidence: ________________________________
- Specific improvement: _________________________________________
- What I will keep, revise, or investigate: ______________________
- Does the review change my valuation conclusion or research priority? Why? _______________________________________________

## Files to have open before class

1. `Apple-Partner-Presentation.md` (this guide)
2. `Apple proforma.md` or the Apple FY2025 Form 10-K
3. `Lab-08-Deal-Evidence-and-Valuation-Triangulation-Apple.md`
4. `Lab-11-Apple/Lab-11-Part-I-Apple.md`
5. `Lab-11-Apple/Lab-11-Part-V-Apple.md`
6. `Lab-11-Apple/Lab-11-Part-E-Apple.md`

## Source record

- Apple Inc., FY2025 Form 10-K, fiscal year ended September 27, 2025; filed October 31, 2025; accessed September 24, 2026. https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm
- Historical market-price and peer-source details are recorded in `Lab-08-Deal-Evidence-and-Valuation-Triangulation-Apple.md`, retrieved September 24, 2026.
