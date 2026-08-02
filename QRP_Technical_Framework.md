# Technical Framework: The QRP Agentic System

**Concept:** Digital Proposal Engineer (DPE)
**Core Objective:** Convert raw, fragmented RFQs into a high-confidence **Quote Ready Package (QRP)** using a decoupled, 4-layer architecture.

---

## 1. Architecture Layers

### Layer 1: The Reasoning Engine (The Process Brain)
*Standardized logic that is identical for every deployment.*
- **Triage Module:** Logic to identify the "anatomy" of a request (e.g., Technical Specs $\rightarrow$ Commercial Terms $\rightarrow$ Delivery Timeline).
- **Gap Analysis Engine:** A recursive loop that compares extracted requirements against a "Completeness Checklist" to determine what is missing.
- **Synthesis Module:** The ability to correlate current RFQ data with historical "nearest-neighbor" projects to suggest feasibility.
- **Health Scoring Algorithm:** A weighted calculation (e.g., Data Completeness 40% + Historical Match 30% + Technical Feasibility 30%) that determines if a package is "Quote Ready."

### Layer 2: The Org Context (The Knowledge Base)
*The "Company Brain" ingested via RAG and Knowledge Graphs.*
- **Project Archive (The Historian):** Vectorized database of all past projects (BOMs, CAD metadata, final quotes, and "lessons learned" notes).
- **Capability Matrix:** A structured map of the company's technical limits (e.g., "Max build height: 5m," "Material capability: Stainless 316").
- **Vendor Ecosystem:** A directory of approved suppliers, lead times, and part codes.
- **Customer Personas:** Historical preferences of recurring clients (e.g., "Client X always requires ISO-123 certification").

### Layer 3: Policy & Guardrails (The Management)
*The "Employee Handbook" that governs agent behavior.*
- **QRP Definition:** The specific criteria for a "100% Health Score" (e.g., "Must have an attached PDF drawing and a confirmed budget range").
- **Escalation Triggers:** Rules for when the agent must stop and request human input (e.g., "If required material is not in the Capability Matrix $\rightarrow$ Alert Senior Engineer").
- **Risk Heuristics:** Flags for "Danger Zones" (e.g., "Lead time requested is < 4 weeks; flag as High Risk").
- **Communication Style:** The tone and format for chasing clients for missing information.

### Layer 4: The Integration Set (The Hands)
*The API connectors that allow the agent to execute.*
- **Ingestion:** IMAP/SMTP (Email), API (Customer Portals), OCR (PDF/Drawings).
- **Collaboration:** Slack/Teams/WhatsApp for internal coordination.
- **CRM/ERP Sync:** Direct read/write to Twenty CRM or internal ERPs to pull costings and push the final QRP.
- **Output Generator:** Templates to package the QRP into a standardized "Sales-Ready" dossier.

---

## 2. The QRP Workflow Pipeline

**Step 1: Ingestion $\rightarrow$ Triage**
- **Input:** Raw RFQ.
- **Agent Action:** Extract all explicit requirements. Compare against Layer 2 (Capability Matrix).
- **Output:** Initial requirement list + "Missing Info" list.

**Step 2: Historical Correlation**
- **Agent Action:** Query Layer 2 (Project Archive) for similar builds.
- **Output:** "Nearest Neighbor" report: *"This is 85% similar to Project #402 from 2023. Estimated cost was $X, lead time was Y."*

**Step 3: Internal Coordination (The "Ping")**
- **Agent Action:** Reach out to Design/Manufacturing via Layer 4. *"We have a request for [X]; can we accommodate [Y] given our current floor load?"*
- **Output:** Confirmed technical feasibility.

**Step 4: QRP Assembly & Scoring**
- **Agent Action:** Compile the "Dossier" (Requirements + Historical Data + Technical Confirmation + Vendor Codes).
- **Output:** The **QRP** with a **Health Score**.

**Step 5: Handoff**
- **Trigger:** Health Score $\ge$ Threshold (e.g., 80%).
- **Action:** Alert Senior Salesperson: *"RFQ #123 is now Quote Ready. Confidence: 85%. Key risk: Lead time. Package attached."*

---

## 3. The "Plug-and-Play" Onboarding Flow

To deploy this for a new company, the setup is **Configuration, not Coding**:

1. **Connect Hands:** Authorize Email, CRM, and Communication tools.
2. **Seed Knowledge:** Upload 12-24 months of historical project data (PDFs, Excels, CRM logs) to populate the Vector DB.
3. **Define Policies:** Set the "Quote Ready" checklist and escalation triggers.
4. **Test & Calibrate:** Run 5 past RFQs through the system to tune the Health Scoring algorithm.
5. **Go Live:** The agent begins monitoring the inbox.
