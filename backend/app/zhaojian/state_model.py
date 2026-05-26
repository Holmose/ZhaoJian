from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime

DOMAINS = ["relationship", "business", "content", "personal", "strategy", "unknown"]

@dataclass
class ZhaoJianQuery:
    question: str
    domain: str = "unknown"
    goal: str = ""
    event_time: Optional[str] = None
    location: Optional[str] = None

@dataclass
class RealityModel:
    facts: List[str] = field(default_factory=list)
    timeline: List[str] = field(default_factory=list)
    people: List[str] = field(default_factory=list)
    known_variables: List[str] = field(default_factory=list)
    unknown_variables: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)

@dataclass
class SymbolicModel:
    bagua: Dict[str, Any] = field(default_factory=dict)
    wuxing: Dict[str, Any] = field(default_factory=dict)
    iching: Dict[str, Any] = field(default_factory=dict)
    bazi: Dict[str, Any] = field(default_factory=dict)
    qimen: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulationModel:
    agents: List[Dict[str, Any]] = field(default_factory=list)
    rounds: List[Dict[str, Any]] = field(default_factory=list)
    consensus: List[str] = field(default_factory=list)
    disagreements: List[str] = field(default_factory=list)

@dataclass
class FutureBranch:
    name: str
    probability: float
    trigger_conditions: List[str]
    risks: List[str]
    outcome: str

@dataclass
class ZhaoJianState:
    report_id: str
    timestamp: str
    query: ZhaoJianQuery
    reality: RealityModel = field(default_factory=RealityModel)
    symbolic: SymbolicModel = field(default_factory=SymbolicModel)
    simulation: SimulationModel = field(default_factory=SimulationModel)
    causal: Dict[str, Any] = field(default_factory=dict)
    future: Dict[str, Any] = field(default_factory=dict)
    strategy: Dict[str, Any] = field(default_factory=dict)
    confidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def new_state(question: str, domain: str = "unknown", goal: str = "", event_time: str | None = None, location: str | None = None) -> ZhaoJianState:
    ts = datetime.now().isoformat(timespec="seconds")
    rid = "zhaojian_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    return ZhaoJianState(report_id=rid, timestamp=ts, query=ZhaoJianQuery(question=question, domain=domain, goal=goal, event_time=event_time, location=location))
