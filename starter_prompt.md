i want to build a demo with this spec to show case Google agentic AI capabilities to Mortenson. I am working with their Senior Operating Group Safety Director and this is the spec she sent me: https://docs.google.com/document/d/1YEY39Efri87YS7iOV7oIbCAd8UiIyeKGYppt7ZuQevc/edit?tab=t.0

important notes:
- mock up data if you need
- mock up services if you need and make it easy to swap for real services later.
- use Google ADK for agent building, make it modular so it can be deployed into Vertex AI Agent Engine and invoked by various clients
- build a simple web UI using pure HTML/CSS/JS. use the brand/logo/theme from Mortenson.com


Spec text:
Blueprint: Google Data Center Pre-Task Planning (PTP) Agent
1. Executive Summary
The Google Data Center PTP Agent is an AI-driven system designed to standardize and elevate pre-task planning across global campuses. By synthesizing schedule data (P6), safety records (IRIS), technical specifications, and contractual requirements, the agent generates high-fidelity, task-specific execution plans. It serves as a bridge between program-level knowledge and site-level execution.
2. System Architecture & Data Integration
The agent utilizes a Retrieval-Augmented Generation (RAG) architecture to ensure all generated plans are grounded in factual, project-specific data.
Data Input Layer (The "Intelligence" Feed)
Schedule Integration: Real-time API connection to Primavera P6 to identify upcoming high-risk activities (Tack/Flow schedules).
Safety & Lessons Learned: * Google IRIS: Past incident reports for similar scopes of work.
Boots on the Ground: Real-time hazard/kudo trends.
R2 L2 Program: Global lessons learned repository.
Technical & Regulatory:
Project Documents: Specs, Drawings, Engineering Bulletins (MARCUS/YARN).
Standards: ASTM, ASI, Federal/State OSHA, EPA, and DNR.
Google Specifics: Appendix A (LOTO), Appendix B, etc.
Contractual Layer: Analysis of GC and Subcontractor-specific "Scope of Work" (SOW) documents to ensure alignment between contracted tasks and field plans.
3. Functional Modules
A. Schedule-Driven Foreseeability
The agent scans the P6 schedule 3–4 weeks out. It flags tasks that historically have higher incident rates or complex engineering requirements, automatically prompting the team to begin a "High-Risk Review" PTP.
B. The "Smart PTP" Generator
When a crew selects a task (e.g., "Medium Voltage Cabling in Electrical Yard"), the agent generates a plan containing:
Visual Logic: Integrated screenshots of relevant specs and snips from IRIS incident reports showing "what went wrong" in the past.
Just-in-Time Training: 5-minute toolbox talk modules and micro-learning videos tied to that specific task.
Change Management: A "What-If" logic engine to help crews handle field variations or rework without losing safety oversight.
C. GC-Specific Customization (The "Toggle" Feature)
Recognizing that different GCs have unique Safety Management Systems (SMS):
Tenant Profiles: GCs can upload their specific safety programs.
Feature Toggles: Users can toggle between "Google Standard," "GC Standard," or "Combined Best Practice" requirements.
Quality QA/QC: Automated checklists pulled from both Google Quality requirements and GC-specific benchmarks.
4. Output Deliverables
The agent will output structured, mobile-friendly documents including:
Detailed Execution Plan: Step-by-step instructions with integrated safety/quality holds.
Visual Hazard Maps: Pictures of specs vs. pictures of previous failures.
Regulatory Compliance Pack: Relevant OSHA/EPA citations for the specific task.
Crew Self-Assessment: A digital "Post-Task" evaluation to feed back into the learning loop.
5. Learning & Feedback Loop
Self-Correction: If a crew identifies a new hazard during the self-assessment, the agent "tags" that data and updates the global R2 L2 database.
Pattern Recognition: If multiple sites report the same design-related rework, the agent flags an "Engineering Bulletin Opportunity" to the Google design team.
