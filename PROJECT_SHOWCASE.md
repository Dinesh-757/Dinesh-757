# PROJECT DOSSIERS // DILLI DINESH

> A closer look at security projects, their actual scope, and how to evaluate them. Features described below are drawn from the project repositories; they are not claims of independent production validation.

## 01 — CyberShield AI | Security operations platform

**Source:** [CyberShield-AI](https://github.com/Dinesh-757/CyberShield-AI)

A multi-module security operations platform built around a React dashboard and a FastAPI backend. The repository describes network intrusion detection, ransomware behavior monitoring, log analytics, a controlled vulnerability scanner, threat-intelligence correlation, incident management, reports, RBAC and live events.

**Investigate:** How captured events move through detection services to analyst-facing incidents, and how authorization is applied to security actions.

**Technical trail:** React · TypeScript · FastAPI · Scapy · scikit-learn · SQLAlchemy · WebSockets

**Verification note:** Read the setup and tests in the repository. A documented feature is not automatically evidence that every environment or model has been independently validated.

## 02 — CodeGuard AI | Local coding-workspace security

**Source:** [CodeGuard-AI](https://github.com/Dinesh-757/CodeGuard-AI)

A workspace-scoped security scanner that watches real filesystem changes and inspects code and configuration for exposed secrets, risky AI instructions, MCP permissions, dependency indicators, and potentially dangerous patterns. Findings are stored and streamed to a React dashboard.

**Investigate:** File integrity and change detection, scoped monitoring, reproducible rule findings, analyst review, and the difference between heuristics and confirmed vulnerabilities.

**Technical trail:** Python · FastAPI · React · Watchdog · SQLite · WebSockets · JWT

**Verification note:** The project's own README marks full Windows automated tests, Docker/PostgreSQL validation, and interactive browser testing as remaining work. It does not claim to attribute code to an AI assistant or automatically block attacks.

## 03 — MEMFORENSIX | Memory forensics workbench

**Source:** [Memforensix](https://github.com/Dinesh-757/Memforensix)

A full-stack analysis pipeline using Volatility 3, YARA scanning, and IsolationForest-based anomaly detection. Its architecture includes a React UI, FastAPI, Celery workers, Redis, and PostgreSQL.

**Investigate:** Process trees, network artifacts, malware-indicator rules, asynchronous analysis, and the boundary between synthetic demo data and real memory evidence.

**Technical trail:** Volatility 3 · YARA · scikit-learn · FastAPI · Celery · Docker

**Verification note:** The included demo memory sample is synthetic, and the repository explicitly documents a fallback dataset when a true memory image cannot be parsed. Real forensic output requires a valid OS memory image.

---

## Engineering priorities

- **Evidence over decoration:** screenshots, test outputs, and limitations should be attached to their source repositories when available.
- **Scope over hype:** clearly distinguish implemented paths, demonstrations, pending tests and proposed improvements.
- **Defensive by design:** security scanning belongs in authorized and isolated environments.
- **Reproducibility:** installation commands, configuration, and tests are more useful than unsupported performance claims.

[Back to profile](https://github.com/Dinesh-757) · [LinkedIn](https://www.linkedin.com/in/dilli-dinesh) · [TryHackMe](https://tryhackme.com/p/Dinesh20)
