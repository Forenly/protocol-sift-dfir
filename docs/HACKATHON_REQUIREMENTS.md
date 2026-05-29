# Protocol SIFT Hackathon — Requirements (source of truth)

> Compiled from the official Devpost page ("FIND EVIL!"). Use when planning deliverables. Fields marked _TBD_ are not yet published on the page captured.

## Sponsor / Admin
- **Initiative:** Protocol SIFT (SANS / teamdfir)
- **Theme:** FIND EVIL! — AI-assisted DFIR
- **Participants:** 3,761 registered

## The concept
Protocol SIFT integrates AI agents with the **SANS SIFT Workstation** (200+ IR tools) through the **Model Context Protocol (MCP)**. Analyst types in natural language → AI selects tools, executes them, reasons about output, produces structured reports. Mission: turn the POC into a production-grade capability.

## Dates
| Date | Event |
|---|---|
| _TBD_ | Submission period opens |
| _TBD_ | Submission deadline |

## Tools & technologies
- **SANS SIFT Workstation** — OVA: <https://sans.org/tools/sift-workstation> (run in a VM).
- **Protocol SIFT POC install** (run on SIFT):
  ```bash
  curl -fsSL https://raw.githubusercontent.com/teamdfir/protocol-sift/main/install.sh | bash
  ```
- **Starter case data** — sample disk images + memory captures: <https://sansorg.egnyte.com/fl/HhH7crTYT4JK>
- **Protocol SIFT NotebookLM notebook** — chief resource for what/how to build.

## Example / quality bar
- **AppliedIR/Valhuntir** — Valhuntir CLI, AI-augmented IR platform, by Steve Anson (SANS author): <https://github.com/AppliedIR/Valhuntir>. Meet or exceed this level of quality.

## Inspiration / reading
- SANS blog: *Protocol SIFT: An Experimental Research Initiative for AI-Assisted DFIR* (sans.org)
- Rob T. Lee Substack: *Introducing Protocol SIFT: Meeting AI Threat Speed with Defensive AI Orchestration*
- Anthropic **GTG-1002** threat-intel report — the offensive op validating why Protocol SIFT matters.

## What to submit
1. **Text description** — features + functionality.
2. **Demo video <3 min**, public — shows it working, how AI is used, problem + value; no unlicensed material.
3. **Public open-source repo** with OSS license.
4. **README** with setup + run instructions, dependencies, example configs/datasets.
5. **Architecture diagram at repo root**.

## Open questions to confirm on the Devpost page
- [ ] Exact submission window + deadline.
- [ ] Prize structure / tracks (if any).
- [ ] Judging criteria.
- [ ] Eligibility / excluded regions.
