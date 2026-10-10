<div align="center">

<img src="./assets/electric-defense-banner.svg" width="100%" alt="Electric Defense: Dilli Dinesh cybersecurity project dossiers"/>

# PROJECT DOSSIERS // ELECTRIC DEFENSE

**Three different problems. Three different detection workflows. One standard: evidence over hype.**

[← Profile](https://github.com/Dinesh-757) · [Portfolio](https://dinesh-757.github.io/) · [Contact](https://www.linkedin.com/in/dilli-dinesh)

</div>

> **Reading guide:** These dossiers summarize project repositories. They do not certify production readiness, model accuracy, or an independently verified live deployment. For a technical assessment, run the documented setup and tests in a controlled environment and examine the real output.

| Operation | Problem | First thing to inspect |
| :-- | :-- | :-- |
| **01 · CyberShield AI** | Combining security signals into an analyst-facing operations platform | [Architecture & setup](https://github.com/Dinesh-757/CyberShield-AI#readme) |
| **02 · CodeGuard AI** | Finding risky changes and instructions in a local development workspace | [Tests & limitations](https://github.com/Dinesh-757/CodeGuard-AI#tests) |
| **03 · Memforensix** | Investigating process/network artifacts in memory images | [Real data vs. demo fallback](https://github.com/Dinesh-757/Memforensix#important-about-the-forensics-in-this-demo) |

<img src="./assets/electric-conduit.svg" width="100%" alt="" />

## 01 — CyberShield AI | Security operations platform

<a href="https://github.com/Dinesh-757/CyberShield-AI"><img src="./assets/operation-cybershield.svg" width="100%" alt="CyberShield AI project artwork" /></a>

**The problem:** Network, endpoint, application, and intelligence signals are often scattered. Analysts need a single workflow to inspect events, prioritize suspicious activity and record responses.

**The implementation described by the repository:** A React / TypeScript dashboard and FastAPI services for network intrusion detection, ransomware behavior monitoring, log analytics, controlled vulnerability scanning, intelligence feeds, incident management and PDF reporting. Database persistence, role-based permissions and WebSocket event delivery connect the experience.

**Where to look in the code:** FastAPI routes, real-time event handling, model-inference paths, alert persistence, incident workflows, and authentication boundaries.

**How to evaluate it:**
1. Follow the repository's environment-specific setup instructions in an isolated lab.
2. Exercise network and file events that are authorized for that lab.
3. Check whether alerts are tied to observable evidence and appear in the dashboard.
4. Review authorization and logging before exposing any endpoint to another network.

**Evidence boundary:** The listed modules reflect repository documentation, not a benchmark or an independently verified production deployment. Development credentials, if present, must be changed before any shared deployment.

**[View CyberShield AI source →](https://github.com/Dinesh-757/CyberShield-AI)**

<img src="./assets/electric-conduit.svg" width="100%" alt="" />

## 02 — CodeGuard AI | Local coding-workspace security

<a href="https://github.com/Dinesh-757/CodeGuard-AI"><img src="./assets/operation-codeguard.svg" width="100%" alt="CodeGuard AI project artwork" /></a>

**The problem:** AI-assisted development creates new places for malicious instructions, overbroad tool permissions, exposed secrets, and unsafe configurations to appear. A transparent local scanner can help developers review those risks.

**The implementation described by the repository:** An administrator approves a specific workspace, Watchdog observes file changes, deterministic rule modules inspect supported content, and an authenticated React interface displays persisted findings over WebSockets. The system documents bounded scans, role enforcement, event history, and PDF assessment reports.

**Where to look in the code:** Workspace-scope safeguards, scanners and rule IDs, debouncing/hash logic, audit records, security headers, WebSocket authentication, and human review workflow.

**How to evaluate it:**
1. Use the isolated test scripts and the documented approval flow.
2. Add an intentionally benign fixture containing a scanner-recognizable pattern.
3. Compare the file event, finding rule, redacted evidence and analyst review history.
4. Check pause/resume/stop behavior and inspect false-positive limitations.

**Evidence boundary:** It does not identify which AI assistant wrote a file, execute scanned code, or block execution. Its README marks full Windows automation, Docker/PostgreSQL and interactive browser validation as work still to confirm.

**[View CodeGuard AI source and tests →](https://github.com/Dinesh-757/CodeGuard-AI)**

<img src="./assets/electric-conduit.svg" width="100%" alt="" />

## 03 — MEMFORENSIX | Memory forensics workbench

<a href="https://github.com/Dinesh-757/Memforensix"><img src="./assets/operation-memforensix.svg" width="100%" alt="Memforensix project artwork" /></a>

**The problem:** A memory capture can expose process trees, suspicious connections, and indicators that are unavailable in ordinary application logs. Analysts need a structured workflow to inspect those artifacts.

**The implementation described by the repository:** Volatility 3 plugins for memory analysis, YARA-based indicator scanning, an IsolationForest anomaly-analysis stage, and progress/reporting through FastAPI, Celery/Redis and a React dashboard.

**Where to look in the code:** Capture-format parsing, Volatility plugin execution, YARA rules, synthetic data fallback, analysis-job state, exported reports and authorization.

**How to evaluate it:**
1. Use the documented synthetic sample to understand the UI and workflow — **not** as genuine forensic evidence.
2. For real forensic work, use a valid memory image acquired in an authorized environment.
3. Confirm which outputs come from Volatility parsing versus fallback fixtures.
4. Investigate indicator quality and anomalous findings rather than treating model outputs as automatic proof.

**Evidence boundary:** The demo includes a **synthetic placeholder** and a deterministic fallback dataset when memory parsing fails. Real plugin output requires an actual supported OS memory image. That distinction must remain explicit in demos and reports.

**[View MEMFORENSIX source and data caveats →](https://github.com/Dinesh-757/Memforensix)**

<img src="./assets/electric-conduit.svg" width="100%" alt="" />

## What I optimize for

- **Real evidence:** command outputs, test runs, code paths and captured screenshots rather than invented performance numbers.
- **Reproducibility:** explicit setup, test commands, expected inputs and known prerequisites.
- **Threat modeling:** least privilege, authorized scanning boundaries and transparent data handling.
- **Honest limitations:** distinguishing a real detection path from mock data, missing coverage, or unverified deployments.

<div align="center">

<img src="./assets/electric-defense-footer.svg" width="100%" alt="Stay curious. Defend relentlessly." />

[Return to profile](https://github.com/Dinesh-757) · [View portfolio](https://dinesh-757.github.io/) · [Connect on LinkedIn](https://www.linkedin.com/in/dilli-dinesh)

</div>
