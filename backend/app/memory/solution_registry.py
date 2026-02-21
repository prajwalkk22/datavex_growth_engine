from backend.app.memory.datavex_loader import load_datavex_memory

def build_solution_registry():
    raw_memory = load_datavex_memory()

    registry = []

    for item in raw_memory:
        content = item["content"].lower()

        if "real-time" in content or "execution" in content:
            registry.append({
                "pain": "Lack of real-time RevOps execution",
                "solution": "Event-driven execution layer",
                "evidence": item["content"],
                "confidence": 0.9
            })

        if "pipeline" in content and "forecast" in content:
            registry.append({
                "pain": "Inaccurate forecasting",
                "solution": "Signal-based pipeline intelligence",
                "evidence": item["content"],
                "confidence": 0.85
            })

    return registry