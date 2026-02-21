from backend.app.graph import build_graph
from unittest.mock import patch

def test_pipeline_full_success():
    graph = build_graph()

    with patch("app.agents.authority_review.authority_review") as mock_review:
        mock_review.return_value = {"approved": True}

        result = graph.invoke({
            "keyword": "AI in RevOps"
        })

    assert result.get("authority_approved") is True
    assert "blog_final" in result
    assert "social_assets" in result
    assert "linkedin" in result["social_assets"]