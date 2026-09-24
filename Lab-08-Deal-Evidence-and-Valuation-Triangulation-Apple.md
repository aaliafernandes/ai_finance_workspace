# Lab 08 — Deal Evidence and Valuation Triangulation: Apple

Educational valuation exercise only; this is not personalized investment advice.

## Problem, comparison date, and initial policy

**Target:** Apple Inc. (NASDAQ: AAPL)  
**Comparison date:** September 10, 2026  
**Question:** What would Apple stock be worth at defensible peer P/E multiples, and what does that add to the Week 3 DCF?

Apple earns most of its revenue from its integrated device ecosystem—iPhone, Mac,
iPad, wearables, and accessories—and from related services such as advertising,
AppleCare, cloud, App Store/digital content, subscriptions, and payments. Apple
reported positive FY2025 GAAP diluted EPS of $7.46. [Apple's FY2025 Form 10-K,
Item 1 and Item 8](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm)
describes those businesses and reports the EPS.

**Policy written before selecting candidates:** a peer should be a large, profitable
operating company with a global technology ecosystem, recurring software/services
or platform revenue, substantial intellectual property, and consumer-facing
computing exposure. I will qualify rather than automatically admit firms whose
profits depend mainly on enterprise cloud/software or advertising instead of
device sales. I will exclude a candidate if it lacks both an ecosystem/services
component and comparable scale/profitability, or if its annual GAAP EPS is not
available by the comparison date.

Focused research question: *Do Microsoft and Alphabet have enough consumer
platform, devices, and recurring-services economics to be qualified P/E
references for Apple, despite their much larger enterprise-cloud or advertising
exposure?*

Evidence that would cause rejection: a filing showing the candidate lacks a
consumer platform/device ecosystem, that its annual earnings are not positive or
not public by September 10, 2026, or that the quoted security and EPS use
incompatible currency or share classes.

## Candidate decisions and evidence

| Candidate | Decision | Business evidence opened | Important difference and reason |
|---|---|---|---|
| Microsoft (MSFT) | **Qualify / use** | [FY2026 Form 10-K, Item 1—Business and operating segments](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm): software, services, devices, advertising; Productivity and Business Processes, Intelligent Cloud, and More Personal Computing. | Microsoft has devices and consumer computing, but its earnings are much more exposed to enterprise software and cloud. Its FY2026 GAAP EPS also includes the reported OpenAI-investment effect, so it is a qualified reference, not a direct Apple substitute. |
| Alphabet Class A (GOOGL) | **Qualify / use** | [FY2025 Form 10-K, Item 1A and Note 12](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm): it reports Google Services, Google Cloud, devices (smartphones, home devices, wearables), and class-specific EPS. | Alphabet has a consumer platform, devices, and cloud, but more than 70% of its 2025 revenue came from online advertising. Its P/E therefore reflects advertising/platform economics much more than Apple's hardware-led mix. |

Neither candidate was chosen for the price it produces. I kept both as qualified
references because each matches the policy's platform, services, scale, and
profitability criteria, while the stated differences limit how strongly their
multiples can transfer to Apple.

## Inputs and source record

All prices below are closing-price observations in USD on the same trading date,
September 10, 2026. Historical-price data were retrieved September 24, 2026 from
the linked market-data pages because the required date is no longer the current
quote; market-price data are not company filings. GAAP diluted EPS is kept
separate from any adjusted/non-GAAP EPS.

| Company / security | Close | Annual GAAP diluted EPS used | Fiscal year end; public by | Source and locator |
|---|---:|---:|---|---|
| Apple (AAPL), target | $326.57 | $7.46 | Sep. 27, 2025; Form 10-K filed Oct. 31, 2025 | [AAPL price history](https://stockanalysis.com/stocks/aapl/history/) (Sep. 10 row); [Apple 10-K, Consolidated Statements of Operations / Note 3](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm) |
| Microsoft (MSFT), qualified peer | $492.44 | $17.95 | Jun. 30, 2026; FY2026 results released Jul. 29, 2026 | [MSFT price history](https://www.financecharts.com/stocks/MSFT/summary/price) (Sep. 10 row); [Microsoft FY2026 earnings release, “Fiscal Year 2026 Results”](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) |
| Alphabet Class A (GOOGL), qualified peer | $332.60 | $10.82 | Dec. 31, 2025; Form 10-K filed Feb. 4, 2026 | [GOOGL price history](https://www.financecharts.com/stocks/GOOGL/summary/price) (Sep. 10 row); [Alphabet 2025 Form 10-K, Note 12—Net Income Per Share](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm) |

**Date correction:** the Week 3 DCF record listed $315.34 with a September 10,
2026 timestamp. The historical-price record identifies $315.34 as the
**September 9** close and $326.57 as the September 10 close. I use $326.57 only
for this same-date P/E comparison and do not alter the saved DCF model.

## P/E calculation and validation

The reproducible calculator is [lab_08_apple_pe.py](lab_08_apple_pe.py). Run it
with the same Python command used for the prior labs:

```powershell
python lab_08_apple_pe.py
```

It calculates P/E as price divided by GAAP diluted EPS and multiplies each peer
P/E by Apple's FY2025 diluted EPS. It does not bridge P/E with cash or debt.

| Item | Result |
|---|---:|
| Microsoft P/E = $492.44 / $17.95 | 27.433983x |
| Alphabet Class A P/E = $332.60 / $10.82 | 30.739372x |
| Median peer P/E | 29.086677x |
| Apple implied range | $204.66–$229.32 |
| Apple at peer median P/E | $216.99 |

Hand check: Microsoft’s $492.44 close divided by its $17.95 FY2026 GAAP diluted
EPS equals **27.433983x**, which matches the calculator before display rounding.

Before calculating the leave-one-out result, I predicted that removing Alphabet
would lower the implied Apple value because Alphabet has the higher P/E. The
result confirms this: removing GOOGL leaves the Microsoft-only reference estimate
of **$204.66**, a **−$12.33** change from the two-peer median estimate. With one
peer remaining there is no minimum-to-maximum peer range—only a reference
estimate. Removing Microsoft instead leaves the $229.32 Alphabet reference, a
+$12.33 change.

## DCF comparison and skeptical review

| Method | Apple's result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | Saved output: **$(4.08) per diluted share**, September 10, 2026 | The $100 million starting FCFF and 10% WACC are labelled training placeholders. The FCFF input has a scale mismatch with Apple’s reported cash flow, so this is not a defendable Apple DCF range. |
| Peer P/E | **$204.66–$229.32**, with $216.99 median-implied price; September 10, 2026 | Both peers are qualified rather than close matches. Their multiples embed different growth, risk, and profit mixes. |

**Skeptical colleague’s criticism:** The weakest supported assumption is that the
two qualified peers’ P/E values transfer to Apple. Microsoft’s enterprise-cloud
earnings and Alphabet’s advertising earnings have materially different drivers;
their current multiples may also reflect different AI-investment expectations.

**My judgment: Accept.** The source evidence supports the business differences,
so I treat the output as a qualified reference range, not a fair-value conclusion
or a number to average with the broken DCF. The direct evidence for resolving
this concern would be a peer with a more comparable hardware-plus-services mix,
and a repaired Apple DCF using consistently scaled, sourced FCFF and a dated WACC.

**Question that could change my decision:** After correcting the FCFF scale and
estimating a dated WACC, does a fully sourced Apple DCF produce a value range
that overlaps the qualified-peer P/E range?

## Conditional conclusion

**Call: Watch — defer initiation.** Apple has positive reported earnings and the
qualified-peer P/E exercise gives a transparent $204.66–$229.32 reference range.
However, the comparison does not prove Apple is fairly valued: it is below the
September 10 market close of $326.57 and rests on two peers with different
economic engines. The Week 3 DCF cannot be used to corroborate or reject that
signal because its FCFF scale is unresolved. I will not mechanically average the
methods.

I would change this call after (1) resolving the DCF's FCFF and WACC inputs,
(2) testing a more direct hardware-and-services ecosystem peer or documenting
why none is available, and (3) checking whether the newer evidence materially
changes the qualified P/E reference range. This is an educational research
conclusion, not investment advice.
