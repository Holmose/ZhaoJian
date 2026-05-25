# TianJi System Architecture V1

## Mission

Build an oriental-philosophy-enhanced multi-agent simulation system for future branching, past reconstruction, and decision strategy.

## Non-goals

- Do not claim deterministic prophecy.
- Do not replace legal, medical, investment, or safety-critical decisions.
- Do not use oriental symbolic systems as standalone proof.

## Core State Object

`TianJiState` is the central data contract. All engines read/write this shape:

```json
{
  "query": {},
  "reality": {},
  "symbolic": {},
  "simulation": {},
  "causal": {},
  "future": {},
  "strategy": {},
  "confidence": {}
}
```

## Module Contracts

### Reality Parser

Input: raw user question.
Output: domain, facts, timeline, people, known variables, unknown variables, constraints.

### Symbolic Engine

Input: raw text + domain.
Output: bagua, wuxing, V4 iching transition, V2 bazi natal pattern, V3 qimen situation model.

### Simulation Adapter

Input: TianJiState dict.
Output: agents, rounds, consensus, disagreements.

V1 uses deterministic local adapter. V4 should replace it with Hermes/MiroFish full simulation manager.

### Report Generator

Input: TianJiState dict.
Output: Markdown + JSON.

## Integration Plan with Hermes/MiroFish

1. Keep TianJi as independent extension module under `backend/app/tianji`.
2. Add API endpoint `/api/tianji/run`.
3. In endpoint, call `TianJiOrchestrator.run`.
4. Replace `LocalSimulationEngine` with real MiroFish simulation manager when full environment is available.
5. Store TianJi report as project artifact.
6. Add frontend page for TianJi runs.

## Future Data Engines

### Bazi Engine V2

Required data:

- Solar/lunar conversion
- Heavenly stems and earthly branches
- Month pillar rules
- Day pillar algorithm
- Hour pillar algorithm
- Ten gods
- Five element strength
- Luck cycles

### Qimen Engine V3

Required data:

- Solar terms
- Yin/Yang Dun
- Ju number
- Nine palaces
- Eight doors
- Nine stars
- Eight gods
- Three wonders and six instruments
- Useful god selection

## Quality Gates

- Every report must include blind spots.
- Every report must include at least 3 future branches.
- Every report must include a Skeptic Agent perspective.
- Every symbolic conclusion must be translated into real-world action language.
