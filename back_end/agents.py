import re
import json
from typing import Dict, Any, List, Tuple
from models import LessonPlan, LessonPlanState
from llm import LLMClient

class EvaluatorAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def _parse_evaluation(self, text: str) -> Tuple[Dict[str, Any], int, str, str]:
        try:
            # Parsing reason, overall score, and suggestion using the defined markers
            reason_match = re.search(r"<\|reason_start\|>(.*?)<\|reason_end\|>", text, re.DOTALL)
            score_match = re.search(r"<\|score_start\|>(.*?)<\|score_end\|>", text, re.DOTALL)
            suggest_match = re.search(r"<\|suggest_start\|>(.*?)<\|suggest_end\|>", text, re.DOTALL)

            reason = reason_match.group(1).strip() if reason_match else "Không có lý do."
            overall_score = int(score_match.group(1)) if score_match else 0
            suggestion = suggest_match.group(1).strip() if suggest_match else "Không có đề xuất tối ưu."

            # The probability score is now the overall score as per the updated prompt format
            probability_score = overall_score

            return {"feedback": suggestion, "reason": reason, "probability_score": probability_score}, overall_score, reason, suggestion
        except Exception as e:
            print(f"Lỗi phân tích đánh giá: {e}. Văn bản nhận được: '{text}'")
            # Return a default structure in case of parsing errors
            return {"feedback": {"error": f"Lỗi định dạng phản hồi từ LLM: {e}"}, "reason": "Lỗi phân tích lý do.", "probability_score": 0, "suggestion": "Lỗi phân tích đề xuất."}, 0, "Lỗi phân tích lý do.", "Lỗi phân tích đề xuất."

    def evaluate(self, state: LessonPlanState) -> Dict[str, Any]:
        lesson_plan = state['lesson_plan']
        student_scores = state['student_scores']
        skill_tree = state['skill_tree']
        evaluation_feedbacks = []
        student_scores_str = f"Student Scores on Skill-Tree Abilities: {student_scores}"
        questions = state['questions']
        learning_style = state.get('learning_style', 'Không rõ')
        preferences = state.get('preferences', {})
        learning_speed = state.get('learning_speed', 'Không rõ')
        learning_info_str = f"Preferences: {json.dumps(preferences, ensure_ascii=False)}\nLearning Style: {learning_style}\nLearning Speed: {learning_speed}" #
        for question in questions:
            eval_task = f"""# Nhiệm vụ:
            Dựa vào trình độ năng lực (thể hiện qua Skill-Tree và điểm số cụ thể), sở thích và tốc độ học của học sinh, đánh giá thiết kế bài giảng đã nhận. Phân tích điểm mạnh, điểm yếu của phần giải thích kiến thức và lời giải bài tập trong bài giảng dựa trên trình độ năng lực, sở thích, phong cách học và tốc độ học của học sinh.
            Ước lượng xác suất học sinh giải đúng câu hỏi sau khi học bài giảng: {question} (một số từ 0 đến 100). Giải thích lý do cho ước lượng này.
            Đề xuất các cách tối ưu hóa phần giải thích kiến thức và lời giải bài tập để nâng cao hiệu quả học tập cho học sinh dựa trên trình độ năng lực, sở thích, phong cách học và tốc độ học của học sinh và cải thiện điểm đánh giá tổng thể của thiết kế bài giảng.
            Định dạng đầu ra:

            <|reason_start|>
            [Lý do chi tiết cho điểm đánh giá và ước lượng xác suất giải đúng bài tập.]
            <|reason_end|>

            <|score_start|>
            ['chỉ duy nhất một số từ 0 đến 100' là điểm đánh giá tổng thể thiết kế bài giảng]
            <|score_end|>

            <|suggest_start|>
            [Các đề xuất cụ thể để tối ưu hóa thiết kế bài giảng, tập trung vào phần giải thích kiến thức và lời giải bài tập.]
            <|suggest_end|>\n\n"""

            prompt = f"""Role: Bạn là một chuyên gia đánh giá nội dung giáo dục và thiết kế giảng dạy khách quan và giàu kinh nghiệm.
            Hồ sơ học sinh: (Skill-Tree):\n{skill_tree}\n{student_scores_str}\n{learning_info_str}\n\n
            Thiết kế bài giảng cần đánh giá:\n{lesson_plan}\n\n
            {eval_task}\n\n
            Constraints: Đánh giá một cách độc lập và khách quan. Phản hồi phải chi tiết, mang tính xây dựng và trực tiếp liên quan đến trình độ năng lực, sở thích, phong cách học và tốc độ học của học sinh.\n
            Workflow & Output Format: Đưa ra nhận định cuối cùng của bạn theo định dạng CHÍNH XÁC đã mô tả trong phần Nhiệm vụ."""

            response_text = self.llm_client.generate(prompt)
            evaluation_feedback, score, reason, suggestion = self._parse_evaluation(response_text)
            # print("evaluation_feedback")
            # print(evaluation_feedback)
            evaluation_feedbacks.append(evaluation_feedback)

        return {"evaluation_feedback": evaluation_feedbacks, "lesson_plan": lesson_plan}

class AnalystAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def _parse_analysis(self, text: str) -> str:
        return text.strip()

    def analyze_and_enrich(self, state: LessonPlanState) -> Dict[str, Any]:
        lesson_plan = state['lesson_plan']
        student_scores = state['student_scores']
        skill_tree = state['skill_tree']

        enriched_exercises = []
        student_scores_str = f"Student Scores on Skill-Tree Abilities: {student_scores}"
        for exercise in lesson_plan.exercises:
            prompt = f"""Role: Bạn là một giáo viên dạy môn Lập trình hướng đối tượng với Java nhiều kinh nghiệm.
            Task: Dựa vào câu hỏi bài tập, giải pháp và hồ sơ năng lực (Skill-Tree) cùng điểm số cụ thể của học sinh, hãy xác định 2-3 lỗi sai phổ biến nhất mà một học sinh có trình độ này có thể mắc phải.
            Trình bày các lỗi sai một cách rõ ràng, dễ hiểu. Student Profile (Skill-Tree):\n{skill_tree}\n{student_scores_str}\n\nExercise Question: {exercise.get('question')}\nExercise Solution: {exercise.get('solution')}\n\n
            Output Format: Chỉ trả về phần phân tích các lỗi sai, không thêm bất kỳ lời chào hay giải thích nào khác. Bắt đầu bằng gạch đầu dòng."""

            common_mistakes = self._parse_analysis(self.llm_client.generate(prompt))
            updated_exercise = exercise.copy()
            updated_exercise['common_mistakes'] = common_mistakes
            enriched_exercises.append(updated_exercise)

        return {"lesson_plan": LessonPlan(
            topic=lesson_plan.topic,
            knowledge_points=lesson_plan.knowledge_points,
            exercises=enriched_exercises
        )}

class OptimizerAgent:
    def __init__(self, llm_client: LLMClient): # Reverted to original
        self.llm_client = llm_client

    def _parse_optimized_plan(self, text: str, topic: str) -> LessonPlan:
        try:
            knowledge_match = re.search(r"PHẦN 1: GIẢI THÍCH KIẾN THỨC\s*-+\s*(.*?)\s*PHẦN 2: BÀI TẬP VẬN DỤNG", text, re.DOTALL | re.IGNORECASE)
            exercises_text_match = re.search(r"PHẦN 2: BÀI TẬP VẬN DỤNG\s*-+\s*(.*)", text, re.DOTALL | re.IGNORECASE)

            knowledge_points = knowledge_match.group(1).strip() if knowledge_match else "Không thể trích xuất kiến thức."
            exercises_text = exercises_text_match.group(1).strip() if exercises_text_match else ""

            exercises = []
            exercise_blocks = re.split(r"---\s*Bài tập\s*\d+\s*---", exercises_text)
            for block in exercise_blocks:
                if not block.strip():
                    continue
                question_match = re.search(r"Câu hỏi:\s*(.*?)(?:\nGiải pháp:|\Z)", block, re.DOTALL)
                solution_match = re.search(r"Giải pháp:\s*(.*?)(?:\nCác lỗi sai thường gặp:|\Z)", block, re.DOTALL)
                common_mistakes_match = re.search(r"Các lỗi sai thường gặp:\s*(.*)", block, re.DOTALL)

                if question_match:
                    exercises.append({
                        "question": question_match.group(1).strip(),
                        "solution": solution_match.group(1).strip() if solution_match else "Chưa có giải pháp.",
                        "common_mistakes": common_mistakes_match.group(1).strip() if common_mistakes_match else "Không có lỗi sai."
                    })
            return LessonPlan(topic, knowledge_points, exercises)
        except Exception as e:
            print(f"Lỗi phân tích giáo án tối ưu: {e}")
            return LessonPlan(topic, "Lỗi định dạng phản hồi từ LLM.", [])

    def optimize(self, state: LessonPlanState) -> Dict[str, Any]:
        previous_plan = state['lesson_plan']
        evaluation_feedback_list = state['evaluation_feedback']
        student_scores = state['student_scores']
        skill_tree = state['skill_tree']
        learning_style = state.get('learning_style', 'Không rõ')
        preferences = state.get('preferences', {})
        learning_speed = state.get('learning_speed', 'Không rõ')
        student_scores_str = f"Student Scores on Skill-Tree Abilities: {student_scores}"
        learning_info_str = f"Preferences: {json.dumps(preferences, ensure_ascii=False)}\nLearning Style: {learning_style}\nLearning Speed: {learning_speed}" # 
        token_prompt = len(previous_plan.__str__().split(' ')) + len(student_scores_str.split(' ')) + 300 + len(learning_info_str.split(' '))
        feedback_str = ""
        for i, feedback_item in enumerate(evaluation_feedback_list):
            feedback_str1 = ""
            feedback_str1 += f"--- Feedback for question {i+1} ---\n"
            feedback_str1 += f"Reason: {feedback_item.get('reason', 'N/A')}\n"
            feedback_str1 += f"Probability Score: {feedback_item.get('probability_score', 'N/A')}\n"
            feedback_str1 += f"Suggestion: {feedback_item.get('feedback', 'N/A')}\n\n"
            token_feedback = len(feedback_str1.split(' '))
            if token_prompt + token_feedback > 14500:
                break
            feedback_str += feedback_str1
            token_prompt += token_feedback

        prompt = f"""Role: Bạn là một nhà thiết kế chương trình giảng dạy sáng tạo và giàu kinh nghiệm trong môn Lập trình hướng đối tượng với Java.
        Task: Cải thiện và viết lại một 'thiết kế bài giảng cá nhân hóa' mới dựa trên: phiên bản cũ, các phản hồi đánh giá và hồ sơ của học sinh, bao gồm: 'trình độ năng lực, sở thích, phong cách học và tốc độ học của học sinh'. Mục tiêu là tạo ra một giáo án tốt hơn, khắc phục được các nhược điểm đã chỉ ra và 'phải phù hợp với trình độ năng lực, sở thích, phong cách học và tốc độ học của học sinh'.
        Hood sơ học sinh (Skill-Tree - Cây trình độ năng lực của học sinh):\n{skill_tree}\n{student_scores_str}\n{learning_info_str}\n\n
        Thiết kế bài giảng cũ:\n{previous_plan}\n\n
        Evaluation Feedback (Advantages and Disadvantages):\n{feedback_str}\n\n
        Instruction: Tập trung vào việc cải thiện các điểm bị đánh giá thấp. Giữ lại những điểm mạnh đã được ghi nhận. Tạo ra nội dung mới 'phải phù hợp hơn với học sinh dựa trên trình độ năng lực, sở thích, phong cách học và tốc độ học của học sinh'. Đảm bảo giáo án mới có 2 phần rõ ràng: giải thích kiến thức và bài tập vận dụng (bao gồm 3 bài tập phù hợp với trình độ năng lực, sở thích, phong cách học và tốc độ học của học sinh).\n\n
        Output Format: Trả về thiết kế bài giảng mới theo định dạng CHÍNH XÁC sau:\n\n
        PHẦN 1: GIẢI THÍCH KIẾN THỨC\n---------------------------------\n[Nội dung kiến thức mới]\n\n
        PHẦN 2: BÀI TẬP VẬN DỤNG\n---------------------------------\n--- Bài tập 1 ---\nCâu hỏi: [Câu hỏi bài tập 1]\nGiải pháp: [Các bước giải chi tiết cho bài tập 1]\nCác lỗi sai thường gặp: [Các lỗi thường mắc phải khi gặp câu hỏi bài tập 1]\n\n--- Bài tập 2 ---\nCâu hỏi: [Câu hỏi bài tập 2]\nGiải pháp: [Các bước giải chi tiết cho bài tập 2]\nCác lỗi sai thường gặp: [Các lỗi thường mắc phải khi gặp câu hỏi bài tập 2]\n\n--- Bài tập 3 ---\nCâu hỏi: [Câu hỏi bài tập 3]\nGiải pháp: [Các bước giải chi tiết cho bài tập 3]\nCác lỗi sai thường gặp: [Các lỗi thường mắc phải khi gặp câu hỏi bài tập 3]
        """

        optimized_text = self.llm_client.generate(prompt)
        optimized_plan = self._parse_optimized_plan(optimized_text, previous_plan.topic)

        return {"lesson_plan": optimized_plan, "iterations": state.get("iterations", 0) + 1}

# class EvaluatorAgent:
#     def __init__(self, llm_client: LLMClient):
#         self.llm_client = llm_client

#     def _parse_evaluation(self, text: str) -> Tuple[Dict[str, Any], int, str, str]:
#         try:
#             reason_match = re.search(r"<\|reason_start\|>(.*?)<\|reason_end\|>", text, re.DOTALL)
#             score_match = re.search(r"<\|score_start\|>(.*?)<\|score_end\|>", text, re.DOTALL)
#             suggest_match = re.search(r"<\|suggest_start\|>(.*?)<\|suggest_end\|>", text, re.DOTALL)

#             reason = reason_match.group(1).strip() if reason_match else "Không có lý do."
#             score_str = score_match.group(1).strip() if score_match else "0"
#             try:
#                 overall_score = int(score_str)
#             except:
#                 overall_score = 50

#             suggestion = suggest_match.group(1).strip() if suggest_match else "Không có đề xuất tối ưu."
#             probability_score = overall_score

#             return {"feedback": suggestion, "reason": reason, "probability_score": probability_score}, overall_score, reason, suggestion
#         except Exception as e:
#             print(f"Lỗi phân tích đánh giá: {e}")
#             return {"feedback": "Lỗi", "reason": "Lỗi", "probability_score": 0}, 0, "Lỗi", "Lỗi"

#     def evaluate(self, state: LessonPlanState) -> Dict[str, Any]:
#         lesson_plan = state['lesson_plan']
#         student_scores = state['student_scores']
#         skill_tree = state['skill_tree']
#         evaluation_feedbacks = []
#         student_scores_str = f"Student Scores: {student_scores}"
#         questions = state['questions']
#         learning_info_str = f"Preferences: {json.dumps(state.get('preferences', {}), ensure_ascii=False)}\nLearning Speed: {state.get('learning_speed', 'N/A')}"
        
#         target_questions = questions[:1] if len(questions) > 0 else ["Câu hỏi kiểm tra kiến thức tổng quát"]

#         for question in target_questions:
#             eval_task = f"""# Nhiệm vụ:
#             Dựa vào trình độ năng lực, sở thích và tốc độ học của học sinh, đánh giá thiết kế bài giảng đã nhận.
#             Ước lượng xác suất học sinh giải đúng câu hỏi: {question} (0-100).
#             Định dạng đầu ra:
#             <|reason_start|>[Lý do]<|reason_end|>
#             <|score_start|>[Điểm số 0-100]<|score_end|>
#             <|suggest_start|>[Đề xuất]<|suggest_end|>"""

#             prompt = f"""Role: Chuyên gia đánh giá.
#             Hồ sơ học sinh: (Skill-Tree):\n{skill_tree}\n{student_scores_str}\n{learning_info_str}\n
#             Thiết kế bài giảng:\n{lesson_plan}\n
#             {eval_task}"""

#             response_text = self.llm_client.generate(prompt)
#             evaluation_feedback, score, reason, suggestion = self._parse_evaluation(response_text)
#             evaluation_feedbacks.append(evaluation_feedback)

#         return {"evaluation_feedback": evaluation_feedbacks, "lesson_plan": lesson_plan}

# class AnalystAgent:
#     def __init__(self, llm_client: LLMClient):
#         self.llm_client = llm_client

#     def _parse_analysis(self, text: str) -> str:
#         return text.strip()

#     def analyze_and_enrich(self, state: LessonPlanState) -> Dict[str, Any]:
#         lesson_plan = state['lesson_plan']
#         student_scores = state['student_scores']
#         skill_tree = state['skill_tree']

#         enriched_exercises = []
#         student_scores_str = f"Student Scores: {student_scores}"
        
#         for exercise in lesson_plan.exercises:
#             prompt = f"""Role: Giáo viên Java kinh nghiệm.
#             Task: Xác định 2-3 lỗi sai phổ biến cho câu hỏi này dựa trên Skill-Tree:\n{skill_tree}\n{student_scores_str}\n
#             Exercise Question: {exercise.get('question')}\nSolution: {exercise.get('solution')}\n
#             Output Format: Chỉ trả về text lỗi sai, bắt đầu bằng gạch đầu dòng."""

#             common_mistakes = self._parse_analysis(self.llm_client.generate(prompt))
#             updated_exercise = exercise.copy()
#             updated_exercise['common_mistakes'] = common_mistakes
#             enriched_exercises.append(updated_exercise)

#         return {"lesson_plan": LessonPlan(
#             topic=lesson_plan.topic,
#             knowledge_points=lesson_plan.knowledge_points,
#             exercises=enriched_exercises
#         )}

# class OptimizerAgent:
#     def __init__(self, llm_client: LLMClient):
#         self.llm_client = llm_client

#     def _parse_optimized_plan(self, text: str, topic: str) -> LessonPlan:
#         try:
#             knowledge_match = re.search(r"PHẦN 1:.*?KIẾN THỨC\s*-+\s*(.*?)\s*PHẦN 2", text, re.DOTALL | re.IGNORECASE)
#             exercises_text_match = re.search(r"PHẦN 2:.*?VẬN DỤNG\s*-+\s*(.*)", text, re.DOTALL | re.IGNORECASE)

#             knowledge_points = knowledge_match.group(1).strip() if knowledge_match else text
#             exercises_text = exercises_text_match.group(1).strip() if exercises_text_match else ""

#             exercises = []
#             exercise_blocks = re.split(r"---\s*Bài tập\s*\d+\s*---", exercises_text)
#             for block in exercise_blocks:
#                 if not block.strip(): continue
#                 question_match = re.search(r"Câu hỏi:\s*(.*?)(?:\nGiải pháp:|$)", block, re.DOTALL)
#                 solution_match = re.search(r"Giải pháp:\s*(.*?)(?:\nCác lỗi|$)", block, re.DOTALL)
#                 if question_match:
#                     exercises.append({
#                         "question": question_match.group(1).strip(),
#                         "solution": solution_match.group(1).strip() if solution_match else "Chưa có",
#                         "common_mistakes": ""
#                     })
#             if not exercises:
#                 exercises = [{"question": "Bài tập tự thực hành", "solution": "Tự thực hành", "common_mistakes": ""}]
#             return LessonPlan(topic, knowledge_points, exercises)
#         except Exception as e:
#             print(f"Lỗi parse tối ưu: {e}")
#             return LessonPlan(topic, text, [])

#     def optimize(self, state: LessonPlanState) -> Dict[str, Any]:
#         previous_plan = state['lesson_plan']
#         evaluation_feedback_list = state['evaluation_feedback']
#         feedback_str = json.dumps(evaluation_feedback_list, ensure_ascii=False)
#         learning_info = f"Style: {state.get('learning_style')}, Interest: {state.get('preferences')}"

#         prompt = f"""Role: Nhà thiết kế giáo án Java.
#         Task: Viết lại bài giảng tốt hơn dựa trên phản hồi: {feedback_str}
#         Hồ sơ học sinh: {learning_info}
#         Bài giảng cũ: {previous_plan}
#         Output Format CHÍNH XÁC:
#         CHỦ ĐỀ GIÁO ÁN: {previous_plan.topic}
#         PHẦN 1: GIẢI THÍCH KIẾN THỨC
#         ---------------------------------
#         [Nội dung kiến thức mới]
#         PHẦN 2: BÀI TẬP VẬN DỤNG
#         ---------------------------------
#         --- Bài tập 1 ---
#         Câu hỏi: [Câu hỏi 1]
#         Giải pháp: [Giải pháp 1]
#         --- Bài tập 2 ---
#         Câu hỏi: [Câu hỏi 2]
#         Giải pháp: [Giải pháp 2]
#         """
#         optimized_text = self.llm_client.generate(prompt)
#         optimized_plan = self._parse_optimized_plan(optimized_text, previous_plan.topic)
#         return {"lesson_plan": optimized_plan, "iterations": state.get("iterations", 0) + 1}