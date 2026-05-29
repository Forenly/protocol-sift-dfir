# Architecture — Protocol SIFT (Forenly)

> Required at repo root: how the agent interacts with the SIFT Workstation, how the LLM is integrated, and the evidence → report data flow.

## High-level flow

### Analyst Interaction Flow

1. **Analyst (Natural Language)**: Initiates queries or goals (e.g., "Find persistence mechanisms on this image").
2. **AI Agent / LLM Client**:
   * Interprets natural language request.
   * Plans the forensic investigation tool-chain.
   * Exchanges requests/responses over **MCP** with the Protocol SIFT server.
   * Runs an iterative reasoning loop over tool outputs.
   * Emits structured, cited forensic reports.
3. **Protocol SIFT MCP Server**:
   * Runs locally on the **SANS SIFT Workstation**.
   * Exposes 200+ DFIR tools (Volatility, Plaso, Sleuth Kit, bulk_extractor, YARA, etc.) as clean MCP tools with schemas.
   * Executes tools directly against the evidence store.
4. **Evidence Store**:
   * Contains disk images, memory captures, and registry hives.
   * Read by SIFT forensic tools to populate results for the agent.


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
