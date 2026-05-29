# Forenly · Protocol SIFT — "FIND EVIL!" Hackathon

> Forenly AI Systems' entry for the **Protocol SIFT** hackathon (SANS / teamdfir) — *AI-assisted Digital Forensics & Incident Response.* Theme: **FIND EVIL!**

## What is Protocol SIFT

Protocol SIFT integrates AI agents with the **SANS SIFT Workstation** — 200+ incident-response tools on a single platform — through the **Model Context Protocol (MCP)**. An analyst types what they need in natural language; the AI selects tools, executes them, reasons about the output, and produces structured reports.

The hackathon mission: sharpen this proof of concept into a production-grade capability.

## What we're building

_TBD — one-paragraph concept._ An agentic DFIR workflow on top of the Protocol SIFT MCP layer: natural-language triage of disk images and memory captures, autonomous tool-chaining across SIFT's IR toolset, and structured, analyst-ready incident reports with evidence citations.

> Cross-leverage: shares the agentic-security investigation pattern with our Splunk Agentic Ops (Security track) and UiPath Maestro (cybersecurity) work — alarm/case → reasoned tool-chain → root cause + remediation playbook.

## Architecture

See [`ARCHITECTURE.md`](./ARCHITECTURE.md) — how the agent talks to the SIFT Workstation over MCP, how the LLM selects/executes tools and reasons over output, and the evidence → report data flow.

## Setup / prerequisites

1. **SANS SIFT Workstation** — download the OVA from <https://sans.org/tools/sift-workstation> and run it in a VM (VirtualBox / VMware).
2. **Protocol SIFT POC** — once SIFT is up:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/teamdfir/protocol-sift/main/install.sh | bash
   ```
3. **Starter case data** — sample disk images + memory captures: <https://sansorg.egnyte.com/fl/HhH7crTYT4JK>
4. Configure an MCP-capable AI client against the installed Protocol SIFT server.

_(Our run instructions, dependencies, and example configs/datasets to be filled in as the project is built.)_

## Resources

- **SANS blog:** *Protocol SIFT: An Experimental Research Initiative for AI-Assisted DFIR* (sans.org)
- **Rob T. Lee's Substack:** *Introducing Protocol SIFT: Meeting AI Threat Speed with Defensive AI Orchestration*
- **Anthropic GTG-1002 threat report** — the offensive operation that validates why Protocol SIFT matters
- **Quality bar / example submission:** [AppliedIR/Valhuntir](https://github.com/AppliedIR/Valhuntir) — Valhuntir CLI, AI-augmented IR platform (by Steve Anson, SANS author)
- **Protocol SIFT NotebookLM notebook** — primary Q&A resource for what/how to build

## Submission checklist

- [ ] Text description (features + functionality)
- [ ] Demo video <3 min, public — shows it working, how AI is used, problem + value; no unlicensed material
- [ ] **Public open-source repo** with OSS license ✅ (Apache-2.0)
- [ ] README with setup + run instructions, dependencies, example configs/datasets
- [ ] **Architecture diagram at repo root**

## Status

🚧 Pre-kickoff. Concept not yet locked. 3,761 participants registered. See [`docs/HACKATHON_REQUIREMENTS.md`](./docs/HACKATHON_REQUIREMENTS.md).
