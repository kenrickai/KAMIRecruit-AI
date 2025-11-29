# agents/orchestrator.py

from dataclasses import dataclass

from agents.candidate_guidance_agent import CandidateGuidanceAgent
from agents.task_recommender_agent import TaskRecommenderAgent
from agents.ngo_onboarding_agent import NGOOnboardingAgent
from router.agent_router import route_message


@dataclass
class OrchestratorResult:
    route: str
    reason: str
    agent_name: str
    reply: str


class Orchestrator:
    """
    Simple multi-agent orchestrator:
    - Uses router.route_message(...) to decide which agent to call.
    - Delegates to one of the Gemini-powered / heuristic agents.
    """

    def __init__(self) -> None:
        self.candidate_agent = CandidateGuidanceAgent()
        self.task_agent = TaskRecommenderAgent()
        self.ngo_agent = NGOOnboardingAgent()

    def handle(self, user_id: int, message: str) -> OrchestratorResult:
        decision = route_message(message)

        # Map router targets to agents
        if decision.target == "candidate":
            agent_name = "candidate_guidance"
            reply = self.candidate_agent.chat(user_id, message)

        elif decision.target in ("projects", "skills"):
            # Project/skills → task recommender
            agent_name = "task_recommender"
            reply = self.task_agent.suggest(user_id, message)

        elif decision.target == "resume":
            # Resume-related → ask user to upload PDF
            agent_name = "candidate_guidance"
            reply = (
                "You mentioned resume/CV. "
                "Please upload your resume to /process_resume so I can extract your skills."
            )

        else:
            # generic fallback → candidate guidance
            agent_name = "candidate_guidance"
            reply = self.candidate_agent.chat(user_id, message)

        return OrchestratorResult(
            route=decision.target,
            reason=decision.reason,
            agent_name=agent_name,
            reply=reply,
        )
