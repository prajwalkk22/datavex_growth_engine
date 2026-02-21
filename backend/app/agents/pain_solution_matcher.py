from app.memory.solution_registry import build_solution_registry

def match_pain_to_solution(identified_gaps: list[str]):
    registry = build_solution_registry()
    matches = []

    for gap in identified_gaps:
        for entry in registry:
            if gap.lower() in entry["pain"].lower():
                matches.append(entry)

    print(f"🔎 Matching against {len(datavex_memory)} DataVex solutions")
    return matches