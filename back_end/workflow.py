from langgraph.graph import StateGraph, END
from models import LessonPlanState
from llm import LLMClient
from agents import EvaluatorAgent, AnalystAgent, OptimizerAgent

# Setup Client & Agents
llm_client = LLMClient()
evaluator_agent = EvaluatorAgent(llm_client)
analyst_agent = AnalystAgent(llm_client)
optimizer_agent = OptimizerAgent(llm_client)

def should_continue_optimization(state: LessonPlanState):
    return "continue" if state.get("iterations", 0) < state.get("max_iterations", 0) else "end"

# Config Graph
workflow = StateGraph(LessonPlanState)
workflow.add_node("analyst", analyst_agent.analyze_and_enrich)
workflow.add_node("evaluator", evaluator_agent.evaluate)
workflow.add_node("optimizer", optimizer_agent.optimize)

workflow.set_entry_point("evaluator")
workflow.add_edge("evaluator", "analyst")
workflow.add_edge("analyst", "optimizer")
workflow.add_conditional_edges(
    "optimizer",
    should_continue_optimization,
    {
        "continue": "evaluator",
        "end": END
    }
)

class EduPlanner:
    def __init__(self, llm_client: LLMClient):
        self.final_lesson_plan = None
        self.best_score = -1

    def run_optimization_loop(self, initial_state: LessonPlanState):
        app = workflow.compile()
        try:
            for s in app.stream(initial_state):
                for key, value in s.items():
                    if 'lesson_plan' in value and value['lesson_plan']:
                        self.final_lesson_plan = value['lesson_plan']
        except Exception as e:
            print(f"Graph Error: {e}")
        return self.final_lesson_plan