from langgraph.graph import StateGraph
from backend.app.state import PipelineState
from backend.app.approval import approval_and_publish
# Signal + Strategy
from backend.app.agents.signal_discovery import discover_signals
from backend.app.agents.signal_scoring import score_signal
from backend.app.agents.signal_validator import validate_signal
from backend.app.agents.serp_gap import serp_gap_analysis
from backend.app.agents.strategy_brief import generate_strategy_brief

# Blog
from backend.app.agents.blog_generator import generate_blog
from backend.app.agents.blog_critique import critique_blog

# Verification
from backend.app.agents.pain_solution_matcher import match_pain_to_solution
from backend.app.agents.authority_review import authority_review

# Short form
from backend.app.agents.short_form_generator import generate_linkedin, generate_twitter
from backend.app.agents.short_form_critique import critique
from backend.app.agents.social_publisher import publish_social_assets


# ======================================================
# BLOG PIPELINE (with authority gate)
# ======================================================
def blog_pipeline(state: PipelineState):
    evolution = []

    blog = generate_blog(state["strategy_brief"])

    for i in range(2):
        review = critique_blog(blog)
        scores = review["scores"]

        evolution.append({
            "draft_number": i + 1,
            "scores": scores,
            "key_changes_made": review.get("rewrite_instructions", [])
        })

        if all(v >= 7 for v in scores.values()):
            break

        blog += (
            "\n\n# Revision Notes\n"
            + "\n".join(review["rewrite_instructions"])
        )

    # ✅ Final canonical artifact
    state["blog_final"] = blog
    state["blog_evolution"] = evolution

    # 🔒 AUTHORITY REVIEW (AI HARD GATE)
    decision = authority_review(blog)

    if not decision["approved"]:
        state["halt"] = True
        state["halt_reason"] = "Authority rejected blog"
        state["authority_approved"] = False
        return state

    state["authority_approved"] = True

    # 🔴 HUMAN-IN-THE-LOOP DISTRIBUTION
    approval_and_publish(state["blog_final"])

    return state
# ======================================================
# SHORT FORM + SOCIAL ASSETS (POST-APPROVAL ONLY)
# ======================================================
def short_form_pipeline(state: PipelineState):
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

    # Final publish-ready assets
    state["social_assets"] = publish_social_assets(
        blog=state["blog_final"],
        strategy=state["strategy_brief"]
    )

    return state


# ======================================================
# GRAPH BUILDER
# ======================================================
def build_graph():
    graph = StateGraph(PipelineState)

    # -------- Layer 2: Signals --------
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

    # -------- NEW: Pain → Solution Gate --------
    def verify_solution(state):
        matches = match_pain_to_solution(state["identified_gaps"])

        if not matches:
            state["halt"] = True
            state["halt_reason"] = "No verified DataVex solution for this pain"
            return state

        state["verified_solutions"] = matches
        return state

    # -------- Strategy --------
    def strategy(state):
        state["strategy_brief"] = generate_strategy_brief(
            keyword=state["keyword"],
            selected_signal=state["selected_signal"],
            identified_gaps=state["identified_gaps"],
        )
        return state

    # -------- Register Nodes --------
    graph.add_node("discover", discover)
    graph.add_node("score", score)
    graph.add_node("validate", validate)
    graph.add_node("serp", serp)
    graph.add_node("verify_solution", verify_solution)
    graph.add_node("strategy", strategy)
    graph.add_node("blog", blog_pipeline)
    graph.add_node("short_form", short_form_pipeline)

    # -------- Graph Flow --------
    graph.set_entry_point("discover")
    graph.add_edge("discover", "score")
    graph.add_edge("score", "validate")
    graph.add_edge("validate", "serp")
    graph.add_edge("serp", "verify_solution")
    graph.add_edge("verify_solution", "strategy")
    graph.add_edge("strategy", "blog")
    graph.add_edge("blog", "short_form")

    return graph.compile()