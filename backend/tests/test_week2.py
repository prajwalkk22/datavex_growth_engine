from app.graph import build_graph


def test_week2_strategy_brief():
    graph = build_graph()
    result = graph.invoke({"keyword": "AI in RevOps"})

    assert "strategy_brief" in result

    brief = result["strategy_brief"]
    assert brief.chosen_angle
    assert len(brief.rejected_angles) >= 2
    assert brief.estimated_authority_score >= 0