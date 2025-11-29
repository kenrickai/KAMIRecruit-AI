from dataclasses import dataclass


@dataclass
class RouteDecision:
    target: str   # "candidate" | "resume" | "projects" | "skills" | "generic"
    reason: str


def route_message(message: str) -> RouteDecision:
    """
    Very simple heuristic router based on keywords.
    You can later replace this with an LLM / classifier.
    """
    text = message.lower()

    if "resume" in text or "cv" in text:
        return RouteDecision(target="resume", reason="User mentioned resume/CV.")
    if "project" in text or "volunteer" in text:
        return RouteDecision(target="projects", reason="User asking about projects.")
    if "skill" in text or "improve" in text or "upskill" in text:
        return RouteDecision(target="skills", reason="User asking about skills.")
    if "job" in text or "career" in text:
        return RouteDecision(target="candidate", reason="Career-related question.")

    return RouteDecision(target="generic", reason="No specific keyword matched.")
