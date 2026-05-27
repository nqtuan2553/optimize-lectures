from models import SkillTree, LessonPlanState, LessonPlan
from config import MOCK_SKILL_TREE_DATA, get_lesson_template, get_topic_questions, get_topic_title
from workflow import EduPlanner, llm_client, optimizer_agent

def parse_lesson_plan_from_text(text: str) -> LessonPlan:
    # Reuse hàm parse của Optimizer để xử lý text ban đầu
    return optimizer_agent._parse_optimized_plan(text, "Java OOP")

def generate_lecture_content(user_data):
    """
    Bridge function: Nhận data Frontend -> Chạy Agent -> Trả về Text
    """
    try:
        # 1. Trích xuất dữ liệu Frontend
        topic = user_data.get('lessonTopic', 'oop_with_java_lessonplan')
        interests = user_data.get('interests', '')
        learning_style = user_data.get('learningStyle', 'visual')
        raw_skills = user_data.get('skillLevels', {})

        print(f"Generating lecture for topic: {topic}, interests: {interests}, style: {learning_style}, skills: {raw_skills}")
        # Map skill level text -> int
        def map_level(val):
            if not val: return 1
            try:
                return int(val.split('_')[1])
            except:
                return 1

        student_scores = [
            map_level(raw_skills.get('syntax')),
            map_level(raw_skills.get('oopConcepts')),
            map_level(raw_skills.get('testing')),
            map_level(raw_skills.get('modeling')),
            map_level(raw_skills.get('abstraction')),
        ]

        # 2. Chuẩn bị State ban đầu
        skill_tree = SkillTree(MOCK_SKILL_TREE_DATA)
        
        # Sửa topic trong text mẫu
        initial_text = get_lesson_template(topic)
        initial_plan = parse_lesson_plan_from_text(initial_text)
        initial_plan.topic = get_topic_title(topic)

        questions = get_topic_questions(topic)

        initial_state = LessonPlanState(
            lesson_plan=initial_plan,
            evaluation_feedback={},
            student_scores=student_scores,
            skill_tree=skill_tree,
            iterations=0,
            max_iterations=2, # Config số vòng lặp
            questions=questions,
            learning_style=learning_style,
            preferences={"interests": interests},
            learning_speed="normal"
        )

        # 3. Chạy Workflow
        planner = EduPlanner(llm_client)
        final_plan = planner.run_optimization_loop(initial_state)

        if final_plan:
            return str(final_plan)
        else:
            return str(initial_plan)

    except Exception as e:
        print(f"Service Error: {e}")
        return f"Lỗi xử lý: {str(e)}"