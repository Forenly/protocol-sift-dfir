# Cyber-Physical & Robotic Forensics: Datasets & SIFT Tool Mapping

This document details how standard tools included in the **SANS SIFT Workstation** are fully equipped to perform digital forensics on autonomous robots, edge controllers, and OT systems, using publicly available and findable datasets.

## 1. Mapping SIFT Tools to Robotics (ROS 2 / Linux) Forensics

Because over 90% of advanced commercial and industrial robots (Autonomous Mobile Robots, manipulator arms, inspection rovers) run on **Linux** (typically Ubuntu) and **ROS 2** (Robot Operating System), standard Linux-capable SIFT tools are natively appropriate for this work.

| SIFT Tool | Standard DFIR Use | Cyber-Physical / Robotics DFIR Mapping |
| :--- | :--- | :--- |
| **Volatility 3** | Linux Memory Triage | • Identify active ROS 2 nodes (processes running as ROS 2 executors).<br>• Detect memory-injected payloads overriding safety controls (using `linux_malfind`).<br>• Analyze network sockets (`linux_netstat`) to locate unauthorized outbound control sessions. |
| **Plaso (log2timeline)** | Timeline Analysis | • Correlate system-level events (udev device connections, kernel logs) with robotic sensor anomalies.<br>• Parse ROS 2 SQLite/MCAP databases (`rosbag2`) and application-level log files to build a timeline of hijacked motion commands. |
| **The Sleuth Kit (TSK)** | File System Analysis | • Verify the cryptographic integrity of robotic control binaries.<br>• Detect modification of configuration files (e.g., safety distance thresholds, navigation coordinates). |
| **YARA** | Pattern Matching | • Scan robot filesystems and memory for known IoT/Linux malware families (e.g., Mirai, Gafgyt, Mozi) targeting embedded architectures (ARM, x86_64). |

---

## 2. Publicly Available & Findable Datasets

Our implementation is designed to consume standard forensic formats. The following findable datasets are fully appropriate for validating this workflow:

### A. SIFT Hackathon Starter Case Data
* **Source:** Official SANS/teamdfir Starter Case (https://sansorg.egnyte.com/fl/HhH7crTYT4JK)
* **Format:** RAW/DD Disk Images, LiME Memory Captures.
* **Appropriateness:** Since this case data simulates a compromised Linux server environment, the OS artifacts (process lists, network sockets, system logs) map perfectly to a Linux-based ROS 2 edge controller or autonomous patrol robot runtime.

### B. ROS 2 Security & SROS2 Datasets
* **Source:** Open-Source SROS2 (Secure ROS 2) working group datasets and MCAP logs available on GitHub.
* **Format:** SQLite / MCAP `rosbag2` logs.
* **Appropriateness:** Contains diagnostic records, node communication topology, and lifecycle state changes. Allows the AI agent to parse spatial navigation maps and command inputs to trace how a robot's physical perception was manipulated.

### C. IoT & Linux Malware Corpus
* **Source:** Public repositories like VX-Underground, MalwareMustDie, or standard SANS DFIR whitepapers.
* **Format:** Infected RAM dumps and ext4 disk images.
* **Appropriateness:** Provides real samples of Linux backdoors and botnets. SIFT's Volatility profiles and YARA rules are natively capable of detecting these on Linux-based robots.

---

## 3. Evidence-to-Report Data Flow

The AI Forensics Agent orchestrates the following flow autonomously via MCP:

```
[Robotic Evidence (RAM/Disk)]
            ↓
    [SANS SIFT Tools via MCP]
  (Volatility, Plaso, Sleuth Kit)
            ↓
  [AI Agent Reasoning & Correlation]
            ↓
[Robot Incident Report (RIR)]
```

By grounding our project in standard Linux/ROS 2 forensic artifacts and publicly available datasets, we ensure a practical, high-impact, and fully testable submission that aligns perfectly with the SIFT ecosystem.
