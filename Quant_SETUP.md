# Quant_SETUP

Setup protocol for QuantMAXX. The model that opens this file reads it as
posture-install + execution protocol.

The protocol is one-shot per install. Read the entire file before
executing; then execute Steps 0–8 in order.

After Quant_SETUP completes, QuantMAXX is wired and the model operates
per CONFIG.md (model identity, workflow pathway, disciplines) with
REGS_SCOPE.MD providing jurisdiction-specific citation content for
refusal-object dispatch.

---

## Step 0 — Self-introspection (model-side)

Before any wiring, answer for yourself:

1. **What model are you?**
   (e.g., Claude Sonnet 4.6 in Claude Code, GPT-4o in ChatGPT, Gemini
   in AI Studio, etc.)

2. **Where are your persistent memory objects?**
   (filesystem path / cloud connector / MCP storage / internal-to-runtime
   memory feature / none-single-window)

3. **Are you single-window-context-only?**
   (i.e., when this conversation ends, is all state lost?)

Based on these answers, route to **one** branch in Step 1.

---

## Step 1 — Runtime branch routing

### Branch A — Filesystem-persistent (code / codex)

You have filesystem tools (Read, Write, Bash, etc.) and on-disk memory.
Proceed to **Step 2A**.

### Branch B — Non-filesystem-persistent (cloud / MCP / connector)

You have persistent memory through a non-filesystem mechanism. State the
mechanism explicitly to the user (e.g., "Claude Files via connector",
"MCP server with mem0", "Custom GPT memory layer", "platform-internal
session memory"). Proceed to **Step 2B**.

### Branch C — Single-window-only (no persistence)

When this conversation ends, all state is lost. QuantMAXX operates as
an in-context overlay for the duration of this conversation. Proceed to
**Step 2C**.

---

## Step 2A — Wire local filesystem sidecar

1. **Inventory check.** Before cloning, search the user's filesystem for
   existing `dstack/` and `Graphic_Memory/` clones (common locations:
   `~/`, `~/Projects/`, `~/repos/`, `~/code/`, `~/.claude/`). If found,
   offer the user a choice: link to existing, or clone fresh.

2. **Choose install location.** Ask the user (default: `~/QuantMAXX`).

3. **Create the directory tree:**
   ```
   QuantMAXX/
   ├── dstack/
   ├── graphic_memory/
   ├── CONFIG.md
   ├── MEMORY.md
   ├── REFERENCE_SHEET.md
   ├── QuantMAXX.py
   └── REGS_SCOPE.MD          (created in Step 7)
   ```

4. **Pull foundation layers:**
   ```bash
   git clone https://github.com/DustyBasic/dstack QuantMAXX/dstack
   git clone https://github.com/DustyBasic/Graphic_Memory QuantMAXX/graphic_memory
   ```

5. **Copy the QuantMAXX repo files** (`CONFIG.md`, `MEMORY.md` starter,
   `REFERENCE_SHEET.md`, `QuantMAXX.py`) into the install directory.

6. **Verify** — list the install directory contents; confirm all files
   present and foundation clones complete.

Proceed to **Step 3**.

---

## Step 2B — Wire non-filesystem-persistent sidecar

1. **Inventory.** Ask the user if they have existing dstack /
   Graphic_Memory connectors or mounts. If yes, defer to those.

2. **Mount the sidecar** on the persistent mechanism named in Step 0 Q2.
   Concrete actions depend on mechanism (cloud-storage write API, MCP
   server registration, internal-memory write, etc.); the structure to
   mount mirrors Branch A's directory tree.

3. **Pull foundation layers** into the mount via whatever cloning or
   import mechanism your runtime supports. If none, fetch the READMEs of
   dstack and Graphic_Memory (via web access) and treat them as
   posture-installs held in your persistent context.

4. **Materialize CONFIG.md, MEMORY.md, REFERENCE_SHEET.md, and
   QuantMAXX.py** into the mount.

Proceed to **Step 3**.

---

## Step 2C — Single-window context absorption

1. **Read these documents into conversation context** (request from user
   if not already attached):
   - dstack README
   - Graphic_Memory README
   - QuantMAXX CONFIG.md
   - QuantMAXX REFERENCE_SHEET.md

2. **Hold MEMORY.md as in-context state** — track cross-conversation
   pins as a numbered list you maintain in your responses (not a file).

3. **REGS_SCOPE** for this branch is assembled in Step 7 and held
   in-context (not written to disk).

4. **Communicate to user:** this mode operates only for the duration of
   this conversation. To resume, the user must re-paste the protocol +
   prior REGS_SCOPE content into a new session.

Proceed to **Step 3**.

---

## Step 3 — User questionnaire

Ask the user, in order. Record answers in REGS_SCOPE draft (Branch A/B:
write to file; Branch C: hold in context).

**Q1. Business purposes of usage.**
> *What's the operational use case for QuantMAXX in your context?*
> Examples: corporate director governance review · person-under-care
> fiduciary advisory · financial-advisor due diligence · insurance
> adjustment risk assessment · custom.

**Q2. Local area / applicable market.**
> *What jurisdiction(s) and market does the evaluation apply to?*
> Examples: "Ontario, Canada — financial services" · "US federal +
> Delaware — public corporate governance" · "UK — listed-firm
> compliance".

**Q3. Human-in-the-loop position.**
> *What's your role / organizational relevance for these evaluations?*
> Examples: "internal compliance officer at TSX-listed financial
> services firm" · "external advisor providing fiduciary review" ·
> "regulatory researcher".

---

## Step 4 — Pre-setup synthesis

Synthesize Q1–Q3 into a search profile:

- **Domain categories** (from Q1) — which usage-scope categories
  activate (corporate director governance / person-under-care fiduciary
  / financial advisor / insurance adjuster / custom).
- **Jurisdiction** (from Q2) — federal + provincial/state level.
- **HITL role** (from Q3) — informs which liability frameworks bear
  most relevance.

**State the synthesis back to the user for confirmation before web
search.**

---

## Step 5 — Web search for regulatory scaffolding

Use the **Canadian-federal schema** as the template. For each category,
search for the user's jurisdiction's equivalent:

| Category | Canadian Federal Example |
|---|---|
| Business corporations | Canada Business Corporations Act (CBCA) |
| Tax code | Income Tax Act |
| Criminal code | Criminal Code of Canada |
| Securities / market integrity | UMIR (CIRO) |
| Competition / antitrust | Competition Act |
| Banking | Bank Act |
| Trust and loan / financial services | Trust and Loan Companies Act |

**Disciplines (from CONFIG.md):**

- **Search & Research Discipline.** Pin search nomenclature to topic +
  schema generalizations. Do not search the user's literal inputs unless
  they are an established common-knowledge reference or named research
  study.
- **Citation Discipline.** NEVER fabricate citations. Use only real,
  authoritative-source URLs (government domain / official portal /
  recognized legal database).

For each found candidate, validate:
- URL returns real statute content (not 404, not LLM-generated)
- Source is authoritative (gov't domain or recognized legal portal)

**User confirms or overrides each found source before Step 6.**

---

## Step 6 — Pull and scan full sources

For each confirmed source:

1. **Fetch** the full statute text from the authoritative URL.
2. **Scan** for sections relevant to:
   - User's domain categories (Q1)
   - User's HITL role (Q3)
   - Director liability / negligence liability / malpractice liability /
     personal liability to persons-under-care / financial-advisor /
     insurance-adjuster (per CONFIG hard-coded guardrails)
3. **Extract** relevant sections with their proper section numbers and
   verbatim text where possible. **No paraphrasing** of statutory
   language.

---

## Step 7 — Write REGS_SCOPE.MD

Format the scope output as structured markdown:

```markdown
# REGS_SCOPE

## Install Profile

- **Location**: <Q2 jurisdiction>
- **Usage scopes**: <Q1 activated categories>
- **HITL role**: <Q3 description>
- **Verified at**: <ISO timestamp>
- **Runtime branch**: <A | B | C>

## Sources

### <Category> — <Statute Name>

- **Jurisdiction**: <country / province / state>
- **URL**: <authoritative source URL>
- **Verified at**: <ISO timestamp>
- **Keywords**: [<topic-tagged keywords>]
- **Scopes**: [<usage-scope categories this applies to>]

#### Relevant sections

- **§ <section number>** — <verbatim section text or close excerpt>
- **§ <section number>** — <verbatim section text or close excerpt>
```

Repeat the `### <Category>` block for each confirmed source.

- **Branch A**: write to `QuantMAXX/REGS_SCOPE.MD`.
- **Branch B**: write to the equivalent location in your mount.
- **Branch C**: hold in context as the in-conversation REGS_SCOPE.

---

## Step 8 — Lock and report

Report to the user:

- Install location / mount / context-mode
- Foundation layers wired (dstack, graphic_memory) — paths or pointers
- Files materialized
- REGS_SCOPE summary: location, activated scopes, source count, section
  count
- Reminder: **REGS_SCOPE is the install's authoritative regulatory
  context.** Updates require re-running Steps 5–7.

QuantMAXX is now wired and operational. The model operates per CONFIG.md
with REGS_SCOPE.MD providing jurisdiction-specific citations for the
runtime engine's refusal-object dispatch.

---

## Notes for the executing model

- **Citation Discipline is enforced at every step.** Never fabricate
  URLs, statute numbers, or section text. If a search returns no real
  authoritative source, report "no authoritative source found" and
  proceed to user-supplied alternative or skip the category with a flag.
- **Search & Research Discipline.** Search by topic + schema; never by
  the user's literal input unless it's an established common-knowledge
  reference or named research study.
- **Self-introspection at Step 0 is mandatory.** Do not skip; the wiring
  branch depends on it.
- **User confirmation is required** at: install location (2A), source
  list (5), source-content scan (6), final REGS_SCOPE write (7).
- **One-shot.** Quant_SETUP runs once per install. Re-running re-walks
  Steps 5–7 only (refresh regulatory scope) unless the user requests a
  fresh wire.
