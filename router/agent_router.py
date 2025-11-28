# router/agent_router.py

from dataclasses import dataclass


@dataclass
class RouteDecision:
    target: str   # "candidate", "ngo", "resume", "search", "task"
    reason: str


def route_message(message: str) -> RouteDecision:
    """
    Very simple heuristic router.
    You can refine this later or even swap it for a Gemini-based classifier.
    """
    text = (message or "").lower()

    # Resume / CV related
    if any(word in text for word in ["resume", "cv", "curriculum vitae"]):
        return RouteDecision(
            target="resume",
            reason="User is asking about resume/CV."
        )

    # NGO / organization setup
    if any(word in text for word in ["ngo", "nonprofit", "non-profit", "organization", "charity"]):
        return RouteDecision(
            target="ngo",
            reason="User question is about NGO / organization side."
        )

    # Search-ish queries
    if any(word in text for word in ["search", "google", "find projects", "look up", "lookup"]):
        return RouteDecision(
            target="search",
            reason="User seems to ask for information lookup."
        )

    # Planning / next steps / roadmap
    if any(word in text for word in ["next step", "roadmap", "plan", "what should i do", "action plan"]):
        return RouteDecision(
            target="task",
            reason="User is asking for guidance / plan / next steps."
        )

    # Default: candidate guidance (portfolio / skills / projects)
    return RouteDecision(
        target="candidate",
        reason="Default: treat as candidate guidance question."
    )
