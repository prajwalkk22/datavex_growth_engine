import sys
import os

# add backend/ to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.graph import build_graph


def test_week1_pipeline():
    graph = build_graph()
    result = graph.invoke({"keyword": "AI in RevOps"})

    assert "selected_signal" in result
    assert "competitor_angles" in result
    assert "identified_gaps" in result
    assert result["selected_signal"]["composite"] > 0