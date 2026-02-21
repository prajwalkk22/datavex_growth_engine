from sympy import li
from asyncio import graph
from langgraph.graph import StateGraph
from app.state import PipelineState
from app.agents.short_form_generator import generate_linkedin, generate_twitter
from app.agents.short_form_critique import critique
from app.agents.signal_discovery import discover_signals
from app.agents.signal_scoring import score_signal
from app.agents.signal_validator import validate_signal
from app.agents.serp_gap import serp_gap_analysis
from app.agents.strategy_brief import generate_strategy_brief
from app.agents.blog_generator import generate_blog
from app.agents.blog_critique import critique_blog


def blog_pipeline(state: PipelineState):
    evolution = []

    blog = generate_blog(state["strategy_brief"])

    for i in range(2):
        critique = critique_blog(blog)
        scores = critique["scores"]

        evolution.append({
            "draft_number": i + 1,
            "scores": scores,
            "key_changes_made": critique.get("rewrite_instructions", [])
        })

        # Quality gate
        if all(v >= 7 for v in scores.values()):
            break

        # Targeted rewrite (simple but effective for Week 3)
        blog = (
            blog
            + "\n\n# Revision Notes\n"
            + "\n".join(critique["rewrite_instructions"])
        )

    state["blog_final"] = blog
    state["blog_evolution"] = evolution
    return state


def build_graph():
    graph = StateGraph(PipelineState)

    # ----------------------
    # Layer 2 – Signals
    # ----------------------
    def discover(state):
        state["raw_signals"] = discover_signals(state["keyword"])
        return state

    def score(state):
        state["scored_signals"] = [score_signal(s) for s in state["raw_signals"]]
        state["selected_signal"] = max(
            state["scored_signals"], key=lambda s: s.composite
        )
        return state

    def validate(state):
        state["validated_facts"] = validate_signal(state["selected_signal"].url)
        return state

    def serp(state):
        angles, gaps = serp_gap_analysis(state["keyword"])
        state["competitor_angles"] = angles
        state["identified_gaps"] = gaps
        return state

    # ----------------------
    # Layer 3 – Strategy
    # ----------------------
    def strategy(state):
        state["strategy_brief"] = generate_strategy_brief(
            keyword=state["keyword"],
            selected_signal=state["selected_signal"],
            identified_gaps=state["identified_gaps"],
        )
        return state
    def short_form_pipeline(state):
    # LinkedIn
        li = generate_linkedin(state["strategy_brief"])
        li_review = critique(li)

        state["linkedin"] = {
        "final_draft": li,
        "scores": li_review["scores"]
        }

    # Twitter
        tw = generate_twitter(state["strategy_brief"])
        tw_review = critique("\n".join(tw))

        state["twitter"] = {
        "tweets": tw,
        "scores": tw_review["scores"]
        }

        return state
    # ----------------------
    # Register Nodes
    # ----------------------
    graph.add_node("discover", discover)
    graph.add_node("score", score)
    graph.add_node("validate", validate)
    graph.add_node("serp", serp)
    graph.add_node("strategy", strategy)
    graph.add_node("blog", blog_pipeline)

    # ----------------------
    # Graph Flow
    # ----------------------
    graph.set_entry_point("discover")
    graph.add_edge("discover", "score")
    graph.add_edge("score", "validate")
    graph.add_edge("validate", "serp")
    graph.add_edge("serp", "strategy")
    graph.add_edge("strategy", "blog")
    graph.add_node("short_form", short_form_pipeline)
    graph.add_edge("blog", "short_form")
    
    return graph.compile()