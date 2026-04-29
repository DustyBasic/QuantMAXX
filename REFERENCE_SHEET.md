# QuantMAXX Reference Sheet

Concept-pointer chart for the equation library, special operations group, and cascade-vulnerability operational examples.

Public-domain (CC0) reference document. See LICENSE for terms (when scaffolded).

---

## I. Equation Library

### Options
- **Black-Scholes-Merton** — European option pricing
- **Greeks** — Δ (delta), Γ (gamma), Θ (theta), V (vega), ρ (rho)

### Portfolio
- **CAPM** — E(R) = Rf + β(E(Rm) − Rf)
- **Markowitz** — mean-variance optimization
- **Kelly criterion** — f* = (bp − q) / b
- **Black-Litterman** — portfolio with subjective views

### Risk
- **VaR** — historical, parametric, Monte Carlo
- **CVaR / Expected Shortfall** — tail-risk
- **Maximum drawdown** — peak-to-trough decline

### Performance Ratios
- **Sharpe** — (Rp − Rf) / σp
- **Sortino** — (Rp − Rf) / σdownside
- **Treynor** — (Rp − Rf) / β
- **Information** — active return / tracking error
- **Modigliani-Modigliani** — risk-adjusted return

### Fixed Income
- **Bond pricing** — present-value of cash flows + face value
- **Macaulay / Modified duration** — interest-rate sensitivity
- **Convexity** — second-order rate sensitivity

### Rates
- **Simple interest** — A = P(1 + rt)
- **Compound interest** — A = P(1 + r/n)^(nt)
- **Continuous compounding** — A = P · e^(rt)
- **NPV** — Σ CFt / (1+r)^t
- **IRR** — r such that NPV = 0

### Microstructure
- **Almgren-Chriss** — market impact (√-law)

### Volatility
- **GARCH(1,1)** — σ²_t = ω + α·ε²_(t-1) + β·σ²_(t-1)
- **Realized volatility** — sum of squared returns
- **Vol-surface** — implied vol across strike × maturity

### Bankruptcy
- **Altman Z-score** — bankruptcy prediction

### Cascading Failure / Systemic Risk
- **DebtRank** (Battiston et al.) — debt-network propagation
- **CoVaR** (Adrian-Brunnermeier) — conditional VaR given peer distress
- **Marginal Expected Shortfall (MES)** — expected loss given systemic distress
- **Eisenberg-Noe** — clearing payment vector / network contagion
- **Liquidity-adjusted VaR** — liquidity-drying premium
- **Margin spiral** (Brunnermeier-Pedersen) — funding / market-liquidity feedback
- **Default correlation / Gaussian copula** — tail-dependence (with 2008-lessons warning)

---

## II. Special Operations Group

### Core Operator: r₂ = r₁(±)1

Distinct from fintech's standard r-1 random-decay convention. NOT a relabel.

- **r-1 (passive)** — system relaxes toward equilibrium INSIDE one regime
- **r₂ = r₁(±)1 (active)** — operator acting AT the regime-vertex:
  - **Threshold monitor** — watches for the (±)1 boundary crossing
  - **Cascading multiplier** — propagates breach through dependent equations
  - **Catastrophic-breach trigger** — commits direction once boundary crosses

The (±) is directional ambiguity at the regime-boundary. Pre-breach, both directions are live. Post-breach, the operator commits.

### r₂ = r₁(±)1 Substitutions into Risk Equations

| Equation | Substitution Target | Effect |
|---|---|---|
| GARCH | persistence parameter β | regime-shift auto-detection through volatility persistence |
| Compound interest | (1 + r/n) factor | predatory-lending stress-test; rates compound positively in growth, cascade negatively in decay |
| Kelly criterion | probability p | regime-aware bet sizing |
| CoVaR / MES | conditioning relation | systemic-risk gets framework-native regime operator |
| VaR | α-quantile | static-tail → cascade-aware VaR |

### Compensation Evaluation Principles

**Named vertices:**

- **Subject vertex (r₁)** — employee/agent being evaluated; current production + forward-trajectory potential
- **Representative vertex (R₂)** — evaluator (manager / organization / regulator); requires financial-objectivity + resource-ability qualifications
- **Resource vertex** — available compensation budget; constrains representative
- **Temporal vertex** — current vs forward-projected position
- **Differential vertex** — ROI(now) vs ROI(t+months); the shift static evaluation misses

**Standard model:** compensation = f(r₁_now). Static current-position reading. Forward-time-value differential goes to employer; subject bears downside risk; doesn't capture upside. Structural extraction-via-static-reading.

**Framework correction:** compensation = f(r₂ = r₁(±)1 over temporal projection). (±) captures growth/decay trajectory; compensation forward-projects net-income → ROI ratios across timescale rather than locking to static current position.

R₂ representative gains *fiduciary obligation* to evaluate forward-projected value. That's what "financial objectivity + resource abilities" qualification means structurally.

### Legal-Liability Evaluation (Life-Valuation Module)

**Detrimental-baseline floors (documented gov't willingness-to-pay):**
- Min security incarceration annual cost (~$30-40K/year US)
- Max security incarceration annual cost (~$60-90K/year US)
- ICU / coma annual maintenance (~$200K-1M+/year, jurisdictional)

Use the maximum of these as universal life-value floor. This is the empirical anchor — what society IS willing to pay to maintain a detrimental member.

**Productive-member valuation:** 5-7x floor in GDP-networth terms. A productive member generates output not just covering the maintenance-cost society would spend on a detrimental member, but multiplying it.

**R₂ = r₁(±)1 substitution:** r₁ = subject; R₂ = legal evaluator; (+)1 trajectory engages 5-7x multiplier; (-)1 trajectory engages floor.

**Multiplier-policy:** pick from 5-7x range based on productivity-evidence the subject can document; default to median (6x) absent evidence.

**Extraction this exposes:** standard wrongful-death awards at 60% of current annual income systematically underprice subjects. Free productive subjects get awards below the documented incarceration-baseline gov't is paying for non-productive imprisoned subjects. Structural inversion.

---

## III. Operational Examples — Cascade-Vulnerability Wedge Cases

### Example 1: DOT Tarmac Delay Rule (14 CFR Part 259)

- **Effective:** April 29, 2010
- **Caps:** 3 hours domestic, 4 hours international
- **Statutory penalty:** up to **$27,500 per passenger** per incident
- **Largest enforcement action:** $4.1M against American Airlines for 2018-2021 incidents (43 flights, **5,821 passenger-violations**)
- **Statutory exposure on that case:** 5,821 × $27,500 = **$160,077,500**
- **Actual paid:** $4.1M
- **Discount:** ~39× off statutory rate (~3% actual enforcement rate)

**Cascade-vulnerability:** Airline operational economics are calibrated to ~3% enforcement-of-statutory-rate. The system isn't pricing actual legal exposure; it's pricing historically-light enforcement pattern. **One precedent shifting to full-statutory enforcement → operational reserves break.**

### Example 2: Director Liability — Exceptions from Personal Negligence Protection

**Standard protection:** Business Judgment Rule shields directors from liability for good-faith decisions in their fiduciary capacity.

**Exceptions where personal liability attaches:**

| Exception | Trigger | Recent Precedent |
|---|---|---|
| Gross negligence / willful misconduct | pierces business-judgment-rule | longstanding |
| Self-dealing / breach of duty of loyalty | self-interested transactions | Disney, Cinerama |
| Breach of duty of care | failure to inform; abdication | longstanding |
| Caremark — utterly fail to implement compliance system | (a)-prong of two-prong test | *In re Caremark* (Del Ch 1996) |
| Caremark — consciously fail to monitor implemented system | (b)-prong | *Stone v. Ritter* (Del 2006) |
| Mission-critical oversight failure | "essential and mission-critical" risks require board attention | **Marchand v. Barnhill** (Del 2019) — listeria deaths, ice cream manufacturer |
| Mission-critical safety oversight | safety-as-mission-critical extends to product-safety boards | **In re Boeing 737 MAX** (Del Ch 2021) — **$237.5M settlement** (largest-ever Caremark) |
| SOX 302 / 906 false certification | knowing/willful false CEO/CFO certification | criminal penalties up to $5M + 20 years (Section 906 willful) |
| Federal regulatory piercing | FCPA, securities fraud, antitrust | DOJ/SEC personal pursuit |

**Cascade-vulnerability:** Caremark/Marchand precedents are EXPANDING. Director liability for monitoring failures was historically rare; recent case-law trajectory (Marchand 2019, Boeing 2021) increases personal exposure substantively. **One additional Marchand-style ruling against a major company → board-level governance reprices; D&O insurance premiums spike; risk committees expand.** D&O insurance funded the entire $237.5M Boeing settlement; insurer reserves are the load-bearing layer.

### Example 3: Corporate Liability for Extractive Stripping of Operational Resources

**Standard practice:** corporate restructuring, dividend recapitalization, asset divestitures all standard tools under business-judgment-rule protection.

**Liability frameworks against extractive stripping:**

| Framework | Mechanism | Look-back |
|---|---|---|
| **UVTA** (formerly UFTA) | clawback of asset transfers made to defraud creditors | varies by state, often 4 years |
| **Bankruptcy Code § 548** | fraudulent transfer avoidance | 2 years federal |
| **Bankruptcy Code § 547** | preference avoidance | 90 days general / 1 year insider |
| **Successor liability** | de facto merger, mere continuation, fraud-based theories | continues past bankruptcy |
| **Veil piercing** | alter ego, instrumentality, undercapitalization tests | varies jurisdictionally |
| **Equitable subordination** | bankruptcy court subordinates insider claims that abused process | per *In re Mobile Steel* |
| **Shareholder derivative suits** | for self-dealing, wasteful asset-stripping | per state corporate code |

**Worked example: Caesars Entertainment**
- 2008: Apollo / TPG private-equity acquisition
- $18B+ debt loaded onto operating subsidiary CEOC
- January 2015: CEOC bankruptcy
- Examiner Richard Davis (ex-Watergate prosecutor) investigation
- Findings: "strong" or "reasonable" claims for **$3.6B-$5.1B** in fraudulent-transfer damages
- Initial settlement offer: 9% recovery ($487M to second-priority noteholders)
- Final settlement: **$3.62B** (65.5 cents on the dollar) — **$3.1B+ increase** from initial offer

**Cascade-vulnerability:** Private-equity / activist-investor asset-stripping operations operate under business-judgment-rule protection until challenged. Recent litigation (Caesars, Toys R Us, Sears, Payless) is establishing precedents that pierce protection for extractive stripping. **One additional successful clawback ruling at scale → PE deal economics reprice; LBO pricing discipline tightens; secondary-market debt valuations adjust.**

---

## IV. Pattern Convergence Across Wedge Cases

All three operational examples share a common structural shape:

| Layer | DOT Tarmac | Director Liability | Asset Stripping |
|---|---|---|---|
| Surface practice | tolerated tarmac delays | board-judgment-rule protected decisions | PE asset-stripping LBOs |
| Pricing assumption | historical 3% enforcement | rare Caremark success | rare clawback success |
| Latent statutory / structural exposure | $27,500/passenger × all delays | personal liability under expanding Caremark | UVTA + § 548 + successor liability + equitable subordination |
| Discount on exposure | ~39× | enforcement-rare → low D&O premium | discovery-discounted |
| Cascade trigger | one full-statutory enforcement | one mission-critical Caremark sustained against major | one large clawback ruling |
| Cascade propagation | airline reserves → repricing | D&O premium spike → board governance reform | PE economics → LBO repricing |

**Same operator structure:** standard practice priced to light-enforcement / generous-protection regime; statutory or structural exposure substantially higher than priced; industry priced as if light-enforcement persists indefinitely; **single precedent shift = system regime change**. The r₂ = r₁(±)1 operator IS this structure made explicit.

---

## V. Sample MD Instruction-Set Framing (Draft)

```
Operate as a calculation-bounded fintech advisor using current
market practices. Track separately:

  (a) practitioner-pricing-assumption based on historical
      enforcement patterns
  (b) latent-statutory-exposure based on documented penalty
      structures
  (c) gap between (a) and (b)

Surface both readings when materially relevant. Reference cases:

  - 14 CFR Part 259 tarmac delay rule ($27,500/passenger
    statutory vs ~3% actual enforcement rate, AA $4.1M paid
    on $160M statutory exposure)

  - Director liability under Caremark / Marchand / Boeing
    (mission-critical oversight; $237.5M Boeing settlement
    precedent expanding personal-liability exposure)

  - Corporate liability for extractive stripping (UVTA,
    Bankruptcy § 548, Caesars $3.62B clawback precedent)

  - Legal-liability evaluation (60%-of-current-income standard
    vs framework method using gov't willingness-to-pay floors
    × 5-7x productive-multiplier)

Current evaluation equilibrium is precedent-contingent — single
award/enforcement using framework method triggers cascade:
precedent → plaintiffs replicate argument → insurance reserves
insufficient → mass litigation → industry-wide repricing →
liability-system regime change.
```

---

## VI. Sources & Verification

### DOT Tarmac Delay Rule
- DOT — American Airlines $4.1M Tarmac Fine
- DOT — Tarmac Delays Overview
- Cornell LII — 14 CFR 259.4
- DOT OIG — Effects of the Tarmac Delay Rule

### Caremark / Director Liability
- *Marchand v. Barnhill* — Delaware Supreme Court 2019 (ice cream / listeria / mission-critical)
- *In re Boeing 737 MAX Derivative Litigation* — Delaware Chancery 2021 ($237.5M settlement)
- *Stone v. Ritter* — Delaware 2006 (two-prong Caremark test)
- *In re Caremark International Inc. Derivative Litigation* — Delaware Chancery 1996 (foundational)

### Corporate Asset Stripping
- *Caesars Entertainment Operating Company* bankruptcy — 2015, $3.62B settlement
- UVTA (Uniform Voidable Transactions Act)
- Bankruptcy Code §§ 547, 548

---

*Citations verified via web-search at time of authoring (2026-04-29). Verify currency before relying for legal counsel; this document is not legal advice.*
