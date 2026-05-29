# Architecture — Protocol SIFT (Forenly)

> Required at repo root: how the agent interacts with the SIFT Workstation, how the LLM is integrated, and the evidence → report data flow.

## High-level flow

```
   Analyst (natural language)
            │
            ▼
   ┌──────────────────┐        ┌──────────────────────────────┐
   │   AI Agent /     │  MCP   │  Protocol SIFT MCP Server     │
   │   LLM client     │◄──────►│  (on SANS SIFT Workstation)   │
   │ (tool selection, │        │  exposes 200+ IR tools        │
   │  reasoning loop) │        │  as MCP tools                 │
   └──────────────────┘        └──────────────┬───────────────┘
            ▲                                  │ exec
            │ structured report                ▼
            │                    ┌──────────────────────────────┐
            │                    │  SIFT toolset                 │
            │                    │  (Volatility, Plaso, Sleuth   │
            │                    │   Kit, bulk_extractor, YARA…) │
            │                    └──────────────┬───────────────┘
            │                                   │ reads
            │                                   ▼
            │                    ┌──────────────────────────────┐
            └────────────────────│  Evidence: disk images,       │
              reasoning over      │  memory captures, artifacts   │
              tool output         └──────────────────────────────┘
```

## Components

| Component | Role |
|---|---|
| **AI Agent / LLM client** | Receives the analyst's natural-language request, plans a tool-chain, calls MCP tools, reasons over each tool's output, decides next step, and synthesizes the final report. |
| **Protocol SIFT MCP Server** | Runs on the SIFT Workstation; wraps SIFT's IR tools as MCP-callable tools (name, args schema, output). The interoperability layer between the model and the forensic tooling. |
| **SIFT toolset** | The 200+ DFIR tools (memory, disk, timeline, file-carving, malware-triage). Executed against the evidence under analysis. |
| **Evidence store** | Disk images + memory captures (e.g. the hackathon starter case data) mounted/available to the workstation. |

## Reasoning loop

1. **Intake** — analyst describes the goal ("find persistence on this memory image").
2. **Plan** — agent maps the goal to candidate SIFT tools.
3. **Execute** — agent invokes tools via MCP; captures stdout/artifacts.
4. **Reason** — agent interprets output, correlates findings, decides whether to dig deeper or pivot.
5. **Report** — agent emits a structured, evidence-cited incident report.

_(Diagram and component detail to be refined as the implementation lands.)_
