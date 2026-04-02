import json

def get_upcoming_high_risk_tasks() -> str:
    """
    Scans the Primavera P6 schedule for the next 3-4 weeks and returns high-risk tasks.
    Returns:
        A JSON string containing the tasks.
    """
    tasks = [
        {"task_id": "T-101", "name": "Medium Voltage Cabling in Electrical Yard", "risk_level": "High", "scheduled_start": "2026-04-10"},
        {"task_id": "T-102", "name": "Generator Fuel Line Installation", "risk_level": "High", "scheduled_start": "2026-04-15"},
        {"task_id": "T-105", "name": "Switchgear Rigging and Hoisting", "risk_level": "Critical", "scheduled_start": "2026-04-20"}
    ]
    return json.dumps(tasks, indent=2)

def query_iris_safety_records(task_name: str) -> str:
    """
    Retrieves past incident reports and lessons learned from the Google IRIS and R2 L2 databases for a specific scope of work.
    
    Args:
        task_name: The name or category of the task.
        
    Returns:
        Safety records and hazard trends related to the task.
    """
    task_name_lower = task_name.lower()
    
    records = []
    if "medium voltage" in task_name_lower or "cabling" in task_name_lower:
        records = [
            {"incident_id": "INC-8891", "description": "LOTO failure on secondary feeder resulted in near-miss arc flash.", "date": "2024-11-05"},
            {"incident_id": "INC-7022", "description": "Improper rigging of MV cable spool caused strain injury.", "date": "2025-02-12"},
            {"lesson_learned": "R2 L2 Bulletin 442 - Always double-verify line-side zero energy states using independent proximity testers before making MV terminations."}
        ]
    elif "generator" in task_name_lower or "fuel" in task_name_lower:
        records = [
            {"incident_id": "INC-5510", "description": "Secondary containment breach during pipe pressure test.", "date": "2023-09-01"},
            {"lesson_learned": "R2 L2 Bulletin 310 - Ensure secondary containment flanges are torqued to spec prior to dynamic flow tests."}
        ]
    else:
        records = [{"info": "No critical incidents found for this exact scope, but standard site PPE and generic hot-work rules apply."}]
        
    return json.dumps(records, indent=2)

def generate_ptp_deliverable(task_name: str, gc_standard: str) -> dict:
    """
    Generates a structured execution plan (Smart PTP) incorporating safety holds, training, and QA/QC checklists.
    
    Args:
        task_name: The task being planned.
        gc_standard: The safety standard toggle (e.g., "Google Standard", "GC Standard", "Combined Best Practice").
        
    Returns:
        A dictionary containing the structured PTP.
    """
    checklist = []
    if gc_standard == "Google Standard":
        checklist = ["Google Appendix A (LOTO) completed", "Google Quality Audit G-12 passed", "Review YARN Engineering Bulletin"]
    elif gc_standard == "GC Standard":
        checklist = ["GC Daily JHA completed", "GC Equipment Inspection Log filled", "Subcontractor Toolbox Talk verified"]
    else:
        checklist = ["Combined: Google Appendix A + GC Daily JHA", "Combined: Google Quality + GC Equipment Log", "Review YARN Engineering Bulletin"]

    ptp = {
        "title": f"Pre-Task Plan: {task_name}",
        "standard_applied": gc_standard,
        "visual_logic": "https://www.mortenson.com/images/visual_logic_placeholder.png",
        "just_in_time_training": [
            {"title": "5-Minute Toolbox Talk: Arc Flash Boundaries", "url": "#video-1"},
            {"title": "Micro-learning: Proper Lockout/Tagout (LOTO)", "url": "#video-2"}
        ],
        "qa_qc_checklist": checklist,
        "detailed_execution_plan": [
            "Step 1: Conduct site walkthrough and identify unmapped energetic sources.",
            "Step 2: Apply LOTO according to approved Method of Procedure (MOP).",
            "Step 3: Verification of Zero Energy State (Safety Hold Point).",
            "Step 4: Execute primary operations as per standard.",
            "Step 5: Post-Task Housekeeping and Evaluation."
        ],
        "regulatory_compliance_pack": ["OSHA 1910.269", "NFPA 70E"]
    }
    
    return ptp

def submit_crew_feedback(task_name: str, new_hazards: list[str]) -> str:
    """
    Mocks submitting a crew's self-assessment and feedback back into the global database.
    
    Args:
        task_name: The task completed.
        new_hazards: List of newly identified hazards.
    """
    if new_hazards:
        return f"SUCCESS: Flagged {len(new_hazards)} new hazards for {task_name}. Updated R2 L2 database and flagged 'Engineering Bulletin Opportunity' to Google design team."
    return "SUCCESS: Post-task evaluation recorded. No new hazards identified."
