import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.scoring import (
    calculate_base_score,
    calculate_signal_score,
    calculate_total_score,
    recommend_pm_archetypes
)
from core.classification import classify_pm_readiness
from core.gap_analysis import analyze_skill_gaps
from core.roadmap import build_transition_roadmap

from data.role_skill_map import ROLE_SKILL_BASE_SCORE
from data.signal_defs import SIGNALS
from data.pm_archetypes import PM_ARCHETYPES
from data.archetype_skill_needs import ARCHETYPE_SKILL_NEEDS

from agents.reasoning_agent import reasoning_agent
from agents.signal_agent import signal_agent
from agents.roadmap_agent import roadmap_agent
from agents.guidance_agent import guidance_agent


print("\n=== PM PATH FINDER V1 (AGENTIC) ===\n")

print("Supported roles:")
for r in ROLE_SKILL_BASE_SCORE:
    print("-", r)

role = input("\nEnter your background role: ").strip().lower()
if role not in ROLE_SKILL_BASE_SCORE:
    print("Role not supported.")
    sys.exit(1)

base_total, base_breakdown = calculate_base_score(role, ROLE_SKILL_BASE_SCORE)

signal_inputs = {}
print("\nAnswer signal questions (yes / partial / no):")
for k, v in SIGNALS.items():
    signal_inputs[k] = input(f"{v}? ").strip().lower()

signal_score = calculate_signal_score(signal_inputs)
total_score = calculate_total_score(base_total, signal_score)
readiness = classify_pm_readiness(total_score)

system_paths = recommend_pm_archetypes(base_breakdown, signal_inputs, PM_ARCHETYPES)

print("\nSystem-recommended PM paths:")
for a, _, _ in system_paths:
    print("-", a)

target = input("\nWhich PM role do YOU want to pursue? ").strip().lower()
risk = "Low" if target in [a[0] for a in system_paths] else "High"

gaps = analyze_skill_gaps(base_breakdown, target, ARCHETYPE_SKILL_NEEDS)
roadmap = build_transition_roadmap(gaps, risk)

# ===== AGENTIC LAYER =====

reasoning_text = reasoning_agent({
    "role": role,
    "base_score": base_total,
    "signal_score": signal_score,
    "total": total_score,
    "readiness": readiness
})

signal_text = signal_agent(signal_inputs)
roadmap_text = roadmap_agent(roadmap)
guidance_text = guidance_agent(risk, target)

# ===== REPORT =====

report = []
report.append("PM PATH FINDER – V1 AGENTIC REPORT\n")
report.append("================================\n\n")

report.append(f"Background: {role}\n")
report.append(f"PM Readiness: {readiness}\n")
report.append(f"Total Score: {total_score}\n")
report.append(f"Target PM Role: {target}\n")
report.append(f"Risk Level: {risk}\n\n")

report.append("REASONING:\n")
report.append(reasoning_text + "\n\n")

report.append("SIGNAL ANALYSIS:\n")
report.append(signal_text + "\n\n")

report.append("TRANSITION ROADMAP:\n")
report.append(roadmap_text + "\n\n")

report.append("GUIDANCE:\n")
report.append(guidance_text + "\n\n")

report.append("DISCLAIMER:\n")
report.append("This is guidance, not a job guarantee.\n")

os.makedirs("outputs", exist_ok=True)
with open("outputs/pm_path_report.txt", "w", encoding="utf-8") as f:
    f.writelines(report)

print("\n=== V1 COMPLETE ===")
print("Agentic report generated at outputs/pm_path_report.txt")
