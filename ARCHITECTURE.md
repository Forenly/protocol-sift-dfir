# Architecture — Cyber-Physical Protocol SIFT (Forenly)

> **Design principle:** How the agent interacts with the SIFT Workstation over MCP, how the LLM is integrated, and the cyber-physical evidence → robot-security report data flow.

## High-level flow

### Analyst Interaction Flow

1. **Analyst (Natural Language)**: Initiates queries or goals (e.g., "Find hijacked ROS 2 nodes or anomalous joint-limit overrides in this robot memory dump").
2. **AI Agent / LLM Client**:
   * Interprets natural language request.
   * Plans the forensic investigation tool-chain.
   * Exchanges requests/responses over **MCP** with the Protocol SIFT server.
   * Runs an iterative reasoning loop over tool outputs.
   * Emits structured, safety-cited Robot Incident Reports (RIR).
3. **Protocol SIFT MCP Server**:
   * Runs locally on the **SANS SIFT Workstation**.
   * Exposes 200+ DFIR tools (Volatility, Plaso, Sleuth Kit, bulk_extractor, YARA, etc.) as clean MCP tools with schemas.
   * Executes tools directly against the evidence store.
4. **Evidence Store**:
   * Contains robotic operating system (ROS) memory dumps, filesystem images, SLAM sensor history, navigation database logs, and kernel traces.
   * Read by SIFT forensic tools to populate results for the agent.


## Components

| Component | Role |
|---|---|
| **AI Agent / LLM client** | Receives the analyst's natural-language request, plans a tool-chain, calls MCP tools, reasons over each tool's output, decides next step, and synthesizes the final safety-compliant report. |
| **Protocol SIFT MCP Server** | Runs on the SIFT Workstation; wraps SIFT's IR tools as MCP-callable tools. The interoperability layer between the model and the forensic tooling. |
| **SIFT toolset** | The 200+ DFIR tools (memory, disk, timeline, file-carving, malware-triage) executed against the compromised robotic firmware/software environments. |
| **Evidence store** | Compromised robot filesystem images + memory captures mounted/available to the workstation. |

## Reasoning loop

1. **Intake** — analyst describes the goal ("find hijacked navigation nodes or motion control overrides in this memory capture").
2. **Plan** — agent maps the goal to candidate SIFT tools (e.g. Volatility for memory triage, Plaso for filesystem timeline analysis).
3. **Execute** — agent invokes tools via MCP; captures stdout/artifacts.
4. **Reason** — agent interprets output, correlates findings, decides whether to dig deeper or pivot.
5. **Report** — agent emits a structured, safety-cited Robot Incident Report (RIR).

_(Diagram and component detail to be refined as the implementation lands.)_

