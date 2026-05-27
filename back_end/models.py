import json
from typing import Dict, Any, List, TypedDict

class SkillTree:
    def __init__(self, abilities: Dict[str, Any]):
        self.abilities = abilities

    def __str__(self) -> str:
        return json.dumps(self.abilities, ensure_ascii=False, indent=2)

class LessonPlan:
    def __init__(self, topic: str, knowledge_points: str, exercises: List[Dict[str, Any]]):
        self.topic = topic
        self.knowledge_points = knowledge_points
        self.exercises = exercises

    def __str__(self) -> str:
        exercise_str = ""
        for i, ex in enumerate(self.exercises):
            exercise_str += f"\n--- Bài tập {i+1} ---\n"
            exercise_str += f"Câu hỏi: {ex.get('question', 'Chưa có')}\n"
            exercise_str += f"Giải pháp: {ex.get('solution', 'Chưa có')}\n"
            exercise_str += f"Các lỗi sai thường gặp: {ex.get('common_mistakes', 'Chưa có')}\n"

        return f"""
=======================================================
{self.topic}
=======================================================

PHẦN 1: GIẢI THÍCH KIẾN THỨC
---------------------------------
{self.knowledge_points}

PHẦN 2: BÀI TẬP VẬN DỤNG
---------------------------------
{exercise_str}
=======================================================
"""

class LessonPlanState(TypedDict):
    lesson_plan: LessonPlan
    evaluation_feedback: Dict[str, Any]
    student_scores: List[int]
    skill_tree: SkillTree
    iterations: int
    max_iterations: int
    questions: List[str]
    learning_style: str
    preferences: Dict[str, Any]
    learning_speed: str