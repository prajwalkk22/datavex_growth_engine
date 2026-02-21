from app.graph import build_graph


def test_week3_blog_generation():
    graph = build_graph()
    result = graph.invoke({"keyword": "AI in RevOps"})

    assert "blog_final" in result
    assert len(result["blog_final"]) > 500
    assert len(result["blog_evolution"]) >= 1