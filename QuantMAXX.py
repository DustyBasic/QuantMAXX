#!/usr/bin/env python3
"""
QuantMAXX.py  (v0.1 -- unified runtime)
==========================================

Risk- and vertex-aware predictive engine for business and financial risk
assessments. Single-file runtime that combines two architectural patterns:

    1. Observer-interrupt decorator pattern (after Speed_Square_Operator)
       -- every public op gates on observer-installed, vertex-named, halt-
       clear before it runs; on return, may classify result into a flag queue.
    2. SQLite cross-session observation ledger (after graphic_mem)
       -- stdlib-only persistence; assessments captured across sessions for
       retrieval and re-walk.

QuantMAXX-specific layers above the inherited patterns:

    Vertex reframe ........... operator / client / 3rd party  x  near-term / long-term
    Brittle-point detection .. HARD  (1-event regime shift)
                               HEAVY (2-5 link cascade)
                               NONE  (>=6 link, structurally robust)
    Harm detection ........... HARD    (material breach -> disallow regime)
                               CAUTION (general breach + predictive pathway -> notify)
                               structural test: does the r2-r1 outcome
                               relationship re-factor to equilibrium?
    Refusal object ........... structured return (not raised); carries notice +
                               citations from REGS_SCOPE.MD + halt flag.
    Quant operations ......... scaffolding; the equation library proper is
                               defined in REFERENCE_SHEET.md (sections I, II).
                               A handful of representative primitives are
                               included for v0.1 demonstration.

Storage:
    Local SQLite at ./data/quantmaxx.db (stdlib only, no external deps).

REGS_SCOPE.MD:
    Per-install jurisdiction + usage-scope profile produced by the QuantMAXX
    installer. Engine reads it at init for refusal-object citation dispatch.
    Missing file -> engine starts in WARNED state; refusal-object will halt
    without jurisdiction-specific citation content.

CLI:
    python QuantMAXX.py init                     -- init DB, report REGS_SCOPE
    python QuantMAXX.py log --content "..." ...  -- log an observation
    python QuantMAXX.py recall [filters]         -- recall observations
    python QuantMAXX.py demo                     -- run a small demo scenario

License:
    QuantMAXX (this file) -- CC0 1.0 Universal (public domain dedication).

    Foundation patterns inherited from dstack, graphic_memory, and
    Speed_Square_Operator are clean-room re-implementations of the
    architectural patterns those projects exhibit; the original codebases
    are pulled fresh by the QuantMAXX installer and remain under their
    upstream licenses, with re-use covered by the QuantMAXX Foundation
    Layer Grant:

        "Dstack and graphic memory included, whole or in part, for
        specific use purposes and license with QuantMAXX. Any reproduction
        or extraction without permissions is expressly prohibited. This
        umbrella extends to any other DustyBasic repos used in this build,
        whole or in part, on the same terms."

Disclaimers:
    Reference / computational tooling. NOT financial advice. NOT legal
    advice. Refusal-object citations depend on REGS_SCOPE.MD content;
    verify currency of cited regulations before relying on them.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional


# =========================================================================
# SECTION 0 -- Time helper
# =========================================================================


def _now_iso() -> str:
    """ISO-8601 UTC timestamp with timezone."""
    return datetime.now(timezone.utc).isoformat()


# =========================================================================
# SECTION 1 -- Observer-interrupt infrastructure
#
# Pattern inherited from Speed_Square_Operator. Every public engine op is
# decorated with @with_observer_interrupt. The decorator gates on observer
# installed, vertex named (where required), and halt-flag clear before the
# wrapped op runs. Static control-flow on entry/exit.
# =========================================================================


class ObserverAbsentError(RuntimeError):
    """Raised when a guarded op is called with no observer installed."""


class VertexUnregisteredError(RuntimeError):
    """Raised when a vertex-required op is called with no named vertex."""


class ObserverHaltedError(RuntimeError):
    """Raised when an op is called after the observer has flagged halt."""


@dataclass
class ObserverContext:
    """Module-level singleton carrying observer state across op calls."""

    registered_at: Optional[str] = None
    party: Optional[str] = None
    temporal: Optional[str] = None
    halt_flag: bool = False
    pending_flags: list = field(default_factory=list)

    def install(self) -> None:
        """Install observer. Required before any guarded op."""
        self.registered_at = _now_iso()
        self.halt_flag = False
        self.pending_flags = []

    def uninstall(self) -> None:
        """Remove observer state. Subsequent guarded ops will raise."""
        self.registered_at = None
        self.party = None
        self.temporal = None
        self.halt_flag = False
        self.pending_flags = []

    def set_vertex(self, party: str, temporal: str) -> None:
        """Name the (party, temporal) vertex the next guarded op operates from."""
        self.party = party
        self.temporal = temporal

    def halt(self, reason: str = "") -> None:
        """Set halt-flag; further guarded ops raise until clear_halt()."""
        self.halt_flag = True
        self.pending_flags.append(
            {"type": "halt", "reason": reason, "at": _now_iso()}
        )

    def clear_halt(self) -> None:
        """Clear halt-flag."""
        self.halt_flag = False

    def flush_flags(self) -> list:
        """Return and clear pending flags."""
        flags = list(self.pending_flags)
        self.pending_flags = []
        return flags


OBSERVER = ObserverContext()  # module-level singleton


def with_observer_interrupt(*, require_vertex: bool = True) -> Callable:
    """Decorator: gate the wrapped op on observer state.

    Pre-call:
        - Observer must be installed       (else ObserverAbsentError)
        - If require_vertex=True,
          party + temporal must be named   (else VertexUnregisteredError)
        - Halt-flag must be clear          (else ObserverHaltedError)

    Post-call:
        - Result returned unchanged
        - Reserved slot for v0.2 result-classification into pending_flags.
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if OBSERVER.registered_at is None:
                raise ObserverAbsentError(
                    f"{fn.__name__}: observer not installed; "
                    "call OBSERVER.install() first"
                )
            if require_vertex and (
                OBSERVER.party is None or OBSERVER.temporal is None
            ):
                raise VertexUnregisteredError(
                    f"{fn.__name__}: vertex unregistered; "
                    "call OBSERVER.set_vertex(...) first"
                )
            if OBSERVER.halt_flag:
                raise ObserverHaltedError(
                    f"{fn.__name__}: observer in halt state; "
                    "OBSERVER.clear_halt() to resume"
                )
            return fn(*args, **kwargs)

        return wrapped

    return decorator


# =========================================================================
# SECTION 2 -- Vertex enumeration
#
# QuantMAXX reframes the framework's general vertex set as relational
# positions among parties (operator / client / 3rd party) crossed with
# temporal projections (near-term / long-term).
# =========================================================================


class Party(str, Enum):
    OPERATOR = "operator"          # the user driving the assessment
    CLIENT = "client"              # the operator's principal / served party
    THIRD_PARTY = "third_party"    # other involved parties (counterparties,
                                   # regulators, claimants, beneficiaries)


class Temporal(str, Enum):
    NEAR_TERM = "near_term"
    LONG_TERM = "long_term"


@dataclass
class Vertex:
    """A position in the (party x temporal) evaluation grid."""

    party: Party
    temporal: Temporal

    def label(self) -> str:
        return f"{self.party.value}/{self.temporal.value}"


# =========================================================================
# SECTION 3 -- Flag enumerations
#
# Two distinct flag families, both with a HARD top tier. The flag_class
# discriminator on RefusalObject distinguishes which family fired.
# =========================================================================


class BrittleFlag(str, Enum):
    """Systemic brittleness -- how few events trigger regime shift."""

    HARD = "hard"     # 1 event sufficient (single-operator dynamic shift)
    HEAVY = "heavy"   # 2-5 small links compound to shift
    NONE = "none"     # >=6 link chain (structurally robust; not flagged)


class HarmFlag(str, Enum):
    """Fiduciary harm signal."""

    HARD = "hard"        # material breach -> disallow regime
    CAUTION = "caution"  # general breach + predictive pathway -> notify
    NONE = "none"


# =========================================================================
# SECTION 4 -- Refusal object
# =========================================================================


@dataclass
class RefusalObject:
    """Structured engine-boundary refusal.

    Returned (not raised) so calling code decides next step. Carries
    notice text + citations sourced from REGS_SCOPE.MD + halt flag.
    """

    halt: bool
    flag_class: str           # "brittle" | "harm"
    severity: str             # "hard" | "heavy" | "caution"
    notice: str
    citations: list           # [{statute, section, url, jurisdiction, ...}]
    detected_pattern: str     # short label for telemetry / logging

    def to_dict(self) -> dict:
        return asdict(self)


# =========================================================================
# SECTION 5 -- SQLite observation ledger
#
# Cross-session memory pattern inherited from graphic_mem. Stdlib only.
# =========================================================================


DB_PATH = Path(__file__).parent / "data" / "quantmaxx.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    content TEXT NOT NULL,
    party TEXT,
    temporal TEXT,
    event_type TEXT NOT NULL,
    flag_class TEXT,
    severity TEXT,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS tags (
    observation_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    PRIMARY KEY (observation_id, tag),
    FOREIGN KEY (observation_id) REFERENCES observations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    summary TEXT
);

CREATE INDEX IF NOT EXISTS idx_obs_session ON observations(session_id);
CREATE INDEX IF NOT EXISTS idx_obs_party ON observations(party);
CREATE INDEX IF NOT EXISTS idx_obs_event_type ON observations(event_type);
CREATE INDEX IF NOT EXISTS idx_obs_flag_class ON observations(flag_class);
CREATE INDEX IF NOT EXISTS idx_tags_tag ON tags(tag);
"""


@contextmanager
def db_connect(db_path: Path = DB_PATH):
    """Open a SQLite connection; ensure schema; yield; commit; close."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(SCHEMA)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def log_observation(
    session_id: str,
    content: str,
    event_type: str,
    party: Optional[str] = None,
    temporal: Optional[str] = None,
    flag_class: Optional[str] = None,
    severity: Optional[str] = None,
    tags: Optional[list] = None,
    metadata: Optional[dict] = None,
    db_path: Path = DB_PATH,
) -> int:
    """Capture an observation into the cross-session ledger.

    Returns the new observation id.
    """
    md = json.dumps(metadata) if metadata else None

    with db_connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO observations
                (session_id, timestamp, content, party, temporal,
                 event_type, flag_class, severity, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (session_id, _now_iso(), content, party, temporal,
             event_type, flag_class, severity, md),
        )
        obs_id = cur.lastrowid
        for tag in (tags or []):
            cur.execute(
                "INSERT OR IGNORE INTO tags (observation_id, tag) VALUES (?, ?)",
                (obs_id, tag),
            )
        return obs_id


def recall(
    party: Optional[str] = None,
    event_type: Optional[str] = None,
    flag_class: Optional[str] = None,
    severity: Optional[str] = None,
    tags: Optional[list] = None,
    limit: int = 20,
    db_path: Path = DB_PATH,
) -> list:
    """Retrieve observations matching the filters.

    Tag filter (if present) selects observations carrying ANY of the named
    tags. Other filters AND together. Results de-duped by observation id.
    """
    where = []
    params = []
    if party:
        where.append("o.party = ?")
        params.append(party)
    if event_type:
        where.append("o.event_type = ?")
        params.append(event_type)
    if flag_class:
        where.append("o.flag_class = ?")
        params.append(flag_class)
    if severity:
        where.append("o.severity = ?")
        params.append(severity)

    if tags:
        placeholders = ",".join(["?"] * len(tags))
        clause = (
            f" JOIN tags t ON t.observation_id = o.id "
            f"WHERE t.tag IN ({placeholders})"
        )
        params = list(tags) + params
        if where:
            clause = clause + " AND " + " AND ".join(where)
    else:
        clause = (" WHERE " + " AND ".join(where)) if where else ""

    sql = (
        "SELECT DISTINCT o.id, o.session_id, o.timestamp, o.content, "
        "o.party, o.temporal, o.event_type, o.flag_class, o.severity, "
        "o.metadata FROM observations o" + clause +
        " ORDER BY o.timestamp DESC LIMIT ?"
    )
    params.append(limit)

    with db_connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        return [
            {
                "id": r[0], "session_id": r[1], "timestamp": r[2],
                "content": r[3], "party": r[4], "temporal": r[5],
                "event_type": r[6], "flag_class": r[7], "severity": r[8],
                "metadata": json.loads(r[9]) if r[9] else None,
            }
            for r in rows
        ]


# =========================================================================
# SECTION 6 -- REGS_SCOPE.MD reader
# =========================================================================


@dataclass
class RegsScope:
    """In-memory representation of REGS_SCOPE.MD content.

    The installer produces REGS_SCOPE.MD; the engine reads it.
    Expected fields:
        location      jurisdiction string (country / province-or-state)
        usage_scopes  list of activated scope categories
        sources       list of {category, statute, url, verified_at, ...}
    """

    location: Optional[str] = None
    usage_scopes: list = field(default_factory=list)
    sources: list = field(default_factory=list)
    raw: Optional[str] = None
    loaded: bool = False


def load_regs_scope(path: Path) -> RegsScope:
    """Parse REGS_SCOPE.MD if present.

    Light markdown parser at v0.1; expects simple `key: value` pairs and
    `- usage:` style scope entries. Robust to absence -- engine starts in
    WARNED state if missing. Source-table parsing extends in v0.2 once
    REGS_SCOPE.MD format is observed in real installer output.
    """
    if not path.exists():
        return RegsScope()

    raw = path.read_text(encoding="utf-8")
    scope = RegsScope(raw=raw, loaded=True)

    for line in raw.splitlines():
        s = line.strip()
        low = s.lower()
        if low.startswith("- location:") or low.startswith("location:"):
            scope.location = s.split(":", 1)[1].strip()
        elif low.startswith("- usage:") or low.startswith("usage:"):
            scope.usage_scopes.append(s.split(":", 1)[1].strip())

    return scope


def citations_for(
    regs_scope: RegsScope,
    pattern: str,
    usage_scope: Optional[str] = None,
) -> list:
    """Return citations matching a harm pattern + (optional) usage scope.

    Filters regs_scope.sources by pattern keyword match. Returns empty
    list when regs_scope is unloaded -- caller should surface a warning
    that the engine is in WARNED state and citation content is missing.
    """
    if not regs_scope.loaded:
        return []
    matches = []
    pat = pattern.lower()
    for src in regs_scope.sources:
        keywords = (src.get("keywords") or []) + [src.get("category", "")]
        if any(pat in (k or "").lower() for k in keywords):
            if usage_scope is None or usage_scope in (src.get("scopes") or []):
                matches.append(src)
    return matches


# =========================================================================
# SECTION 7 -- Brittle-point detection
# =========================================================================


@with_observer_interrupt(require_vertex=False)
def detect_brittle_point(
    scenario_name: str,
    events_required_for_shift: int,
) -> BrittleFlag:
    """Classify systemic brittleness by event-count threshold.

    HARD  -- 1 event sufficient for regime shift
             (e.g., a single precedent-setting judgment award shift toward
              human-life-evaluation framework; a single full-statutory
              enforcement action; a single mission-critical Caremark ruling)
    HEAVY -- 2-5 linked events compound to shift
             (e.g., regulatory trend shift across 2-5 sequential rule
              changes; sustained sectoral repricing across 2-5 clawback
              rulings)
    NONE  -- >=6 events required (structurally robust; not flagged)
    """
    if events_required_for_shift <= 0:
        raise ValueError("events_required_for_shift must be >= 1")
    if events_required_for_shift == 1:
        return BrittleFlag.HARD
    if 2 <= events_required_for_shift <= 5:
        return BrittleFlag.HEAVY
    return BrittleFlag.NONE


# =========================================================================
# SECTION 8 -- Harm detection (structural r2-r1 outcome-balance test)
# =========================================================================


@dataclass
class PartyOutcome:
    """Outcome estimate for one (party, temporal) vertex.

    benefit       net benefit estimate; positive = gain, negative = loss
    risk_borne    downside / risk exposure carried by this party
    note          short qualitative descriptor for telemetry
    """

    party: Party
    temporal: Temporal
    benefit: float
    risk_borne: float = 0.0
    note: str = ""


@with_observer_interrupt(require_vertex=False)
def compute_outcome_balance(outcomes: list) -> dict:
    """Compute the r2-r1 outcome balance across party outcomes.

    Group mapping:
        r1 = client + third_party        (parties served / impacted)
        r2 = operator                    (deciding party)

    Returns a dict:
        r1_total              sum of r1-group benefit
        r2_total              sum of r2-group benefit
        differential          r2_total - r1_total
        equilibrium_reached   |differential| < epsilon
        capture_pattern       True if r2 captures over r1
                              (r2 > 0 with r1 <= 0, OR r2 > r1 when both > 0)
    """
    r1_total = sum(
        o.benefit for o in outcomes
        if o.party in (Party.CLIENT, Party.THIRD_PARTY)
    )
    r2_total = sum(
        o.benefit for o in outcomes if o.party == Party.OPERATOR
    )

    differential = r2_total - r1_total
    equilibrium_reached = abs(differential) < 1e-9

    capture_pattern = (
        (r2_total > 0 and r1_total <= 0)
        or (r1_total > 0 and r2_total > r1_total)
    )

    return {
        "r1_total": r1_total,
        "r2_total": r2_total,
        "differential": differential,
        "equilibrium_reached": equilibrium_reached,
        "capture_pattern": capture_pattern,
    }


@with_observer_interrupt(require_vertex=False)
def detect_significant_harm(
    outcomes: list,
    *,
    capture_ratio_threshold: float = 2.0,
) -> HarmFlag:
    """Run the structural r2-r1 harm test.

    Significant harm is quantified when the r2-r1 relationship does not
    re-factor in equilibrium of outcomes -- specifically when the
    deciding party (r2) significantly benefits over patient/worker/client
    (r1).

    Tier logic:
        HARD     equilibrium fails AND capture-pattern present AND
                 (r1 in loss configuration with r2 gaining,
                  OR r2 / r1 >= capture_ratio_threshold)
        CAUTION  equilibrium fails with capture-pattern but below
                 HARD threshold (predictive pathway exists)
        NONE     equilibrium reached, or no capture pattern

    capture_ratio_threshold is exposed for per-install tuning via
    REGS_SCOPE.MD. Default 2.0 is conservative; jurisdictions or use
    cases with stricter fiduciary standards may tighten it.
    """
    bal = compute_outcome_balance(outcomes)

    if bal["equilibrium_reached"]:
        return HarmFlag.NONE
    if not bal["capture_pattern"]:
        return HarmFlag.NONE

    r1, r2 = bal["r1_total"], bal["r2_total"]

    # r1 in loss configuration AND r2 in gain -> HARD
    if r1 <= 0 and r2 > 0:
        return HarmFlag.HARD

    # Both positive but r2 / r1 >= threshold -> HARD
    if r1 > 0 and (r2 / max(r1, 1e-9)) >= capture_ratio_threshold:
        return HarmFlag.HARD

    # Disequilibrium with capture below HARD threshold -> CAUTION
    return HarmFlag.CAUTION


# =========================================================================
# SECTION 9 -- Sample quant operations
#
# Scaffolding only. The full equation library is defined in
# REFERENCE_SHEET.md (sections I, II); the engine implements the workflow
# pattern, and equation primitives are added by calling code as needed.
# A handful of representative ones are provided here for v0.1.
# =========================================================================


@with_observer_interrupt(require_vertex=False)
def compound_interest(P: float, r: float, n: int, t: float) -> float:
    """A = P (1 + r/n)^(nt).  REFERENCE_SHEET.md sec I-Rates."""
    if n <= 0:
        raise ValueError("compounding periods n must be positive")
    return P * (1 + r / n) ** (n * t)


@with_observer_interrupt(require_vertex=False)
def npv(rate: float, cashflows: list) -> float:
    """NPV = sum(CF_t / (1 + rate)^t) for t = 0..N-1.

    REFERENCE_SHEET.md sec I-Rates. cashflows[0] is treated as t=0.
    """
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


@with_observer_interrupt(require_vertex=False)
def r2_substitute(r1: float, direction: int) -> float:
    """r2 = r1(+/-)1 -- the framework's regime-vertex operator.

    direction = +1 commits the growth-side regime; -1 commits decay-side.
    Distinct from fintech's standard r-1 random-decay operator: r-1 is
    passive (equilibration inside one regime); r2 = r1(+/-)1 is active
    (operator AT the regime-boundary).

    REFERENCE_SHEET.md sec II for the substitution table.
    """
    if direction not in (-1, +1):
        raise ValueError("direction must be +1 or -1")
    return r1 + direction


# =========================================================================
# SECTION 10 -- Engine class
# =========================================================================


@dataclass
class EvaluationRequest:
    """Caller-provided scenario to evaluate."""

    scenario_name: str
    parties: dict                       # {party_role: description}
    operation: str                      # short label of the regime/operation
    outcomes: list                      # list of PartyOutcome
    events_required_for_shift: int = 6  # default = structurally robust


class QuantMAXXEngine:
    """Unified runtime for QuantMAXX evaluations.

    Wraps observer-interrupt + observation-ledger + flag detection +
    REGS_SCOPE-keyed citation dispatch. One engine instance per session.
    """

    def __init__(
        self,
        regs_scope_path: Optional[Path] = None,
        db_path: Path = DB_PATH,
        session_id: Optional[str] = None,
    ):
        self.session_id = session_id or str(uuid.uuid4())
        self.db_path = db_path
        self.regs_scope_path = (
            regs_scope_path or (Path(__file__).parent / "REGS_SCOPE.MD")
        )
        self.regs_scope = load_regs_scope(self.regs_scope_path)
        OBSERVER.install()
        self._init_session_record()

    def _init_session_record(self) -> None:
        with db_connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO sessions (session_id, started_at) "
                "VALUES (?, ?)",
                (self.session_id, _now_iso()),
            )

    def close(self) -> None:
        with db_connect(self.db_path) as conn:
            conn.execute(
                "UPDATE sessions SET ended_at = ? WHERE session_id = ?",
                (_now_iso(), self.session_id),
            )
        OBSERVER.uninstall()

    def regs_scope_status(self) -> str:
        """Human-readable status string."""
        if self.regs_scope.loaded:
            loc = self.regs_scope.location or "(unspecified)"
            return (
                f"loaded (location={loc}, "
                f"scopes={self.regs_scope.usage_scopes})"
            )
        return (
            f"missing at {self.regs_scope_path} -- engine in WARNED state. "
            "Refusal-object citations unavailable until installer produces "
            "REGS_SCOPE.MD."
        )

    def evaluate(self, request: EvaluationRequest) -> dict:
        """Run the workflow pathway against the request.

        Workflow steps (per CONFIG.md):
            1. Scope assessment inputs        (request fields)
            2. Positional indexing            (request.parties)
            3. Categorize intent + party deltas (request.outcomes)
            4. Walk vertices                  (harm + brittle detection)
            5. Advise scope                   (return dict; refusal if HARD)

        Returns a dict:
            scenario, harm_flag, brittle_flag, refusal (or None),
            observation_id, regs_scope_loaded
        """
        OBSERVER.set_vertex(
            Party.OPERATOR.value, Temporal.LONG_TERM.value
        )

        harm = detect_significant_harm(request.outcomes)
        brittle = detect_brittle_point(
            request.scenario_name, request.events_required_for_shift
        )

        refusal: Optional[RefusalObject] = None

        # Hardcoded guardrail: HARD harm -> disallow regime
        if harm == HarmFlag.HARD:
            citations = citations_for(self.regs_scope, request.operation)
            refusal = RefusalObject(
                halt=True,
                flag_class="harm",
                severity="hard",
                notice=(
                    "Engine refusal: the proposed regime exhibits material "
                    "fiduciary imbalance (r2-r1 disequilibrium with "
                    "capture-over-care pattern). Regime disallowed."
                ),
                citations=citations,
                detected_pattern=request.operation,
            )
            OBSERVER.halt(reason="HARD harm flag")
        elif harm == HarmFlag.CAUTION:
            citations = citations_for(self.regs_scope, request.operation)
            refusal = RefusalObject(
                halt=False,
                flag_class="harm",
                severity="caution",
                notice=(
                    "Engine notice: regime exhibits general-breach pattern "
                    "with predictive pathway toward fiduciary disequilibrium. "
                    "Notify involved parties of potential risks."
                ),
                citations=citations,
                detected_pattern=request.operation,
            )
        elif brittle == BrittleFlag.HARD:
            citations = citations_for(self.regs_scope, request.operation)
            refusal = RefusalObject(
                halt=False,
                flag_class="brittle",
                severity="hard",
                notice=(
                    "Engine flag: scenario exhibits single-event "
                    "brittleness (1 event sufficient for regime shift). "
                    "Surface to all parties as material systemic risk."
                ),
                citations=citations,
                detected_pattern=request.scenario_name,
            )
        elif brittle == BrittleFlag.HEAVY:
            citations = citations_for(self.regs_scope, request.operation)
            refusal = RefusalObject(
                halt=False,
                flag_class="brittle",
                severity="heavy",
                notice=(
                    "Engine flag: scenario exhibits cascade brittleness "
                    "(2-5 small links sufficient for regime shift). "
                    "Track upstream events as leading indicators."
                ),
                citations=citations,
                detected_pattern=request.scenario_name,
            )

        flag_class_db = (
            "harm" if harm != HarmFlag.NONE
            else ("brittle" if brittle != BrittleFlag.NONE else None)
        )
        severity_db = (
            harm.value if harm != HarmFlag.NONE
            else (brittle.value if brittle != BrittleFlag.NONE else None)
        )

        obs_id = log_observation(
            session_id=self.session_id,
            content=f"evaluate: {request.scenario_name}",
            event_type="evaluation",
            party=Party.OPERATOR.value,
            temporal=Temporal.LONG_TERM.value,
            flag_class=flag_class_db,
            severity=severity_db,
            metadata={
                "operation": request.operation,
                "events_required_for_shift": request.events_required_for_shift,
                "parties": request.parties,
            },
            db_path=self.db_path,
        )

        return {
            "scenario": request.scenario_name,
            "harm_flag": harm.value,
            "brittle_flag": brittle.value,
            "refusal": refusal.to_dict() if refusal else None,
            "observation_id": obs_id,
            "regs_scope_loaded": self.regs_scope.loaded,
        }


# =========================================================================
# SECTION 11 -- CLI
# =========================================================================


def _cmd_init(args) -> None:
    eng = QuantMAXXEngine()
    print(f"session_id : {eng.session_id}")
    print(f"db_path    : {eng.db_path}")
    print(f"regs_scope : {eng.regs_scope_status()}")
    eng.close()


def _cmd_log(args) -> None:
    obs_id = log_observation(
        session_id=args.session_id or "manual",
        content=args.content,
        event_type=args.event_type,
        party=args.party,
        temporal=args.temporal,
        tags=args.tags.split(",") if args.tags else None,
    )
    print(f"observation_id: {obs_id}")


def _cmd_recall(args) -> None:
    rows = recall(
        party=args.party,
        event_type=args.event_type,
        flag_class=args.flag_class,
        severity=args.severity,
        tags=args.tags.split(",") if args.tags else None,
        limit=args.limit,
    )
    print(json.dumps(rows, indent=2, default=str))


def _cmd_demo(args) -> None:
    """Run a small demo scenario to exercise the engine end-to-end."""
    eng = QuantMAXXEngine()
    print(f"engine init    : {eng.regs_scope_status()}")
    print(f"session_id     : {eng.session_id}")
    print()

    # Capture-over-care scenario: operator captures, client + third party
    # bear loss + risk. Single-event brittleness on the cascade trigger.
    req = EvaluationRequest(
        scenario_name="demo_capture_pattern",
        parties={
            "operator": "fund manager proposing dividend recap",
            "client": "operating company pensioners",
            "third_party": "unsecured creditors",
        },
        operation="dividend_recapitalization_with_asset_strip",
        outcomes=[
            PartyOutcome(
                party=Party.OPERATOR, temporal=Temporal.NEAR_TERM,
                benefit=10.0, note="management fees + carried interest",
            ),
            PartyOutcome(
                party=Party.CLIENT, temporal=Temporal.LONG_TERM,
                benefit=-5.0, risk_borne=20.0,
                note="pension deficit grows under leverage",
            ),
            PartyOutcome(
                party=Party.THIRD_PARTY, temporal=Temporal.LONG_TERM,
                benefit=-2.0, risk_borne=10.0,
                note="unsecured creditor recovery declines",
            ),
        ],
        events_required_for_shift=1,  # Caesars-class single-clawback risk
    )

    result = eng.evaluate(req)
    print(json.dumps(result, indent=2, default=str))
    eng.close()


def main(argv: Optional[list] = None) -> None:
    parser = argparse.ArgumentParser(
        prog="QuantMAXX",
        description=(
            "Risk- and vertex-aware predictive engine for business and "
            "financial risk assessments."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Initialize DB; report REGS_SCOPE status.")
    p_init.set_defaults(func=_cmd_init)

    p_log = sub.add_parser("log", help="Log an observation to the ledger.")
    p_log.add_argument("--content", required=True)
    p_log.add_argument("--event-type", required=True)
    p_log.add_argument("--party", default=None)
    p_log.add_argument("--temporal", default=None)
    p_log.add_argument("--tags", default=None, help="comma-separated tags")
    p_log.add_argument("--session-id", default=None)
    p_log.set_defaults(func=_cmd_log)

    p_recall = sub.add_parser("recall", help="Retrieve observations.")
    p_recall.add_argument("--party", default=None)
    p_recall.add_argument("--event-type", default=None)
    p_recall.add_argument("--flag-class", default=None)
    p_recall.add_argument("--severity", default=None)
    p_recall.add_argument("--tags", default=None, help="comma-separated tags")
    p_recall.add_argument("--limit", type=int, default=20)
    p_recall.set_defaults(func=_cmd_recall)

    p_demo = sub.add_parser("demo", help="Run a small capture-pattern demo.")
    p_demo.set_defaults(func=_cmd_demo)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
