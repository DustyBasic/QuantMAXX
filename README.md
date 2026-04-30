# QuantMAXX

**Calculation-bounded fintech & business-risk framework. Vertex-aware. Forward-trend apprehensive. Regulatory-ecosystem monitoring.**

A model setup and reference framework for financial quantization and business risk assessment. Bounds AI-assisted financial reasoning to actual calculation rather than loose narrative, and embeds awareness of the gap between current pricing assumptions and latent statutory exposure.

---

## Motivation

Most quantitative finance tooling treats current market practice as ground truth — existing prices, historical enforcement patterns, and incumbent regulatory equilibria absorbed as baseline. This produces models that work well in continuity and fail badly at regime transitions.

Reality: regulatory ecosystems shift, enforcement intensities cycle, legal precedents emerge, pricing assumptions get repriced. The brittle exposures that matter aren't the ones that have already broken — they're the ones that haven't broken yet.

QuantMAXX tracks both layers explicitly.

---

## Architecture

**Surface layer** — current market practice, established equations, conventional pricing.

**Vertex-aware layer** — every model evaluation is read across operator / client / 3rd-party party-positions and near-term / long-term temporal projections. Same data, different vertices, different signals; surfaces capture-over-care patterns the static-current frame misses.

**Forward-projection layer** — temporal extrapolation that distinguishes current static state from forward-trajectory. Compensation evaluation, ROI projection, and risk modeling all operate in temporal forward-space rather than static current.

**Regulatory-ecosystem layer** — tracks documented statutory exposure separately from observed enforcement patterns. Surfaces brittle equilibria where the gap is large. Co-opts risk evaluations with awareness of legal-practice exposures that may shift in the near future.

**Cascade-failure operator** — the r₂ = r₁(±)1 special operations layer substitutes into standard risk equations to produce regime-shift-aware versions. See [`REFERENCE_SHEET.md`](REFERENCE_SHEET.md) Section II.

---

## Foundation Layers

QuantMAXX inherits two upstream layers that condition the model's operating posture and persistence behavior before any QuantMAXX-specific work begins. The installer pulls them fresh from canonical sources at setup time; they are not bundled in this repository.

- **[dstack](https://github.com/DustyBasic/dstack)** — three-skill cognitive-discipline scaffolding: `fractal_mem_cache` (3-tier substrate caching), `grounded_interface` (continuity-first engagement, translation-loss aware), `et_tu_brute` (bias-pattern catching and vocabulary-drift detection). Establishes the disciplined posture QuantMAXX builds on top of.

- **[Graphic_Memory](https://github.com/DustyBasic/Graphic_Memory)** — cross-session observation ledger: SQLite-backed capture of evaluations and findings, 3-stage retrieval (surface → relevance → fetch), session-lifecycle hooks. Carries QuantMAXX's evaluation history forward across sessions for re-walk and pattern recognition.

Re-use of foundation-layer content within a QuantMAXX install is governed by the Foundation Layer Grant declared in [`CONFIG.md`](CONFIG.md). Extraction or redistribution outside QuantMAXX usage requires separate permission from DustyBasic.

---

## Components

| Module | Coverage |
|---|---|
| Equation library | Options, Portfolio, Risk, Performance Ratios, Fixed Income, Rates, Microstructure, Volatility, Bankruptcy, Systemic Risk |
| Special operations | r₂ = r₁(±)1 substitutions, Compensation Evaluation Principles, Legal-Liability Life-Valuation Module |
| Operational examples | Documented cascade-vulnerability wedge cases with verified citations |
| Runtime engine | Observer-interrupt decorator, cross-session SQLite ledger, brittle-point + harm detection, structured refusal-object dispatch |
| Setup protocol | `Quant_SETUP.md` posture-install + execution; runtime-aware (filesystem / cloud-persistent / single-window branches) |
| Hard-coded guardrails | Stripping-prescription refusal with regional citations; fiduciary-harm disallow per structural r2-r1 test |

Full detail in [`REFERENCE_SHEET.md`](REFERENCE_SHEET.md), [`CONFIG.md`](CONFIG.md), and [`QuantMAXX.py`](QuantMAXX.py).

---

## Audience

- Compliance and risk teams needing model-bounded calculation rather than LLM-narrative
- Auditors evaluating exposure under current vs alternate enforcement regimes
- Researchers studying systemic risk and regulatory regime transitions
- Educators teaching fintech with rigorous foundations
- Operators building businesses that want to understand their forward-vulnerability profile

---

## Status

**v0.1** — reference architecture, runtime engine, and setup protocol. Regulatory-scoping pre-seed bundle deferred (installer pulls live).

Roadmap:
- **v0.1** — Reference architecture + runtime engine + Quant_SETUP (current)
- **v0.2** — Express-layer formatting + MCP server wrapper for cross-LLM access
- **v1.0** — Full feature set with framework-overlay layer

---

## Install

QuantMAXX is installed by a model running through `Quant_SETUP.md` — a posture-install + execution protocol the model reads and executes. Two invocation pathways:

### Pathway 1 — Open Quant_SETUP inside your model

Best when you don't have a local clone yet.

1. In your model session (Claude Code, Claude.ai, ChatGPT, Gemini, Cursor, etc.), instruct the model:
   > *Open https://github.com/DustyBasic/QuantMAXX/blob/main/Quant_SETUP.md and execute the install protocol.*
2. The model self-introspects its runtime, pulls the QuantMAXX repo + foundation layers, and runs you through the questionnaire + regulatory scoping.
3. On completion, REGS_SCOPE.MD is written to your install location (or held in-context for single-window models).

### Pathway 2 — Clone the repo, then import Quant_SETUP

Best when you already have a local development environment.

1. Clone the repo:
   ```bash
   git clone https://github.com/DustyBasic/QuantMAXX
   cd QuantMAXX
   ```
2. In your model session, point the model at the local file:
   > *Read `Quant_SETUP.md` and run the install protocol.*
3. The model self-introspects, wires the sidecar in place, and runs the questionnaire + regulatory scoping.

### What the install creates

```
QuantMAXX/                    (configurable install location)
├── dstack/                   (cloned from github.com/DustyBasic/dstack)
├── graphic_memory/           (cloned from github.com/DustyBasic/Graphic_Memory)
├── CONFIG.md                 (model identity + workflow + disciplines)
├── MEMORY.md                 (auto-loaded memory pin index, grows with use)
├── REFERENCE_SHEET.md        (equation library + special operations)
├── QuantMAXX.py              (runtime engine)
└── REGS_SCOPE.MD             (per-install jurisdiction + scope profile)
```

### Single-window-only models

Free-tier models without filesystem access or persistent memory operate in **context-absorption mode**: the install is held in conversation context for the session's duration; nothing is written to disk. To resume in a new session, re-paste the protocol and any prior REGS_SCOPE content.

---

## License

**CC0 1.0 Universal** — public domain dedication. Use freely; no attribution required.

See `LICENSE` (when scaffolded).

---

## Documents

- [`Quant_SETUP.md`](Quant_SETUP.md) — install protocol; the model reads and executes this to wire QuantMAXX into your runtime
- [`CONFIG.md`](CONFIG.md) — declared toolkit defaults (foundation preloads, model identity, workflow pathway, operating assumption, search/citation disciplines, brittle-point flagging)
- [`REFERENCE_SHEET.md`](REFERENCE_SHEET.md) — equation library, special operations, operational examples, sample MD instruction-set framing
- [`QuantMAXX.py`](QuantMAXX.py) — runtime engine (observer-interrupt + SQLite ledger + harm/brittle detection + refusal-object dispatch)

---

## Disclaimers

Reference material and computational tooling. **Not financial advice. Not legal advice.** Verify currency of cited regulations before relying on them. Citations were verified at time of authoring; regulatory state evolves.
