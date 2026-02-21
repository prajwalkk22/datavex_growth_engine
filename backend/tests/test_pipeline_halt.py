from app.graph import build_graph

def test_pipeline_halts_without_solution():
    graph = build_graph()

    result = graph.invoke({
        "keyword": "random unknown enterprise concept"
    })

    assert result.get("halt") is True
    assert "halt_reason" in result