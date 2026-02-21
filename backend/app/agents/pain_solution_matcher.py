from backend.app.memory.solution_registry import build_solution_registry

def match_pain_to_solution(identified_gaps: list[str]):
    registry = build_solution_registry()
    matches = []

    print(f"🔎 Matching against {len(registry)} DataVex solutions")

    for gap in identified_gaps:
        gap_l = gap.lower()

        for entry in registry:
            content = entry.get("content", "").lower()

            if gap_l in content:
                matches.append({
                    "gap": gap,
                    "matched_content": entry["content"][:300],
                    "source": entry.get("source"),
                    "tag": entry.get("tag")
                })
                break  # one strong match per gap is enough

    return matches