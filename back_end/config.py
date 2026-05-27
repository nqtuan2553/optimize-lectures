import os
import re
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("API_KEY")

# --- MOCK DATA (Dữ liệu giả lập thay cho file) ---

MOCK_SKILL_TREE_DATA = {
    "syntax": {
        "name": "Cú pháp và ngữ nghĩa Java",
        "levels": {
            1: "Cài đặt môi trường và chạy được chương trình cơ bản như Hello World.",
            2: "Cú pháp cơ bản, biến, kiểu dữ liệu.",
            3: "Cấu trúc điều khiển, hàm/method.",
            4: "Luồng dữ liệu, file I/O, stream assembly.",
            5: "Thành thạo cú pháp và ngữ nghĩa Java, có thể tối ưu mã nguồn."
        },
        "max_level": 5
    },
    "oopConcepts": {
        "name": "Khái niệm và triển khai OOP",
        "levels": {
            1: "Hiểu khái niệm cơ bản (trừu tượng, đóng gói, thừa kế, ...).",
            2: "Cài đặt được chương trình với lớp, đối tượng cơ bản.",
            3: "Overriding, đa hình, abstract class, interface, tham chiếu this.",
            4: "Ứng dụng nguyên lý OOP trong project nhỏ.",
            5: "Thiết kế và xây dựng hệ thống hoàn chỉnh sử dụng OOP."
        },
        "max_level": 5
    },
    "testing": {
        "name": "Gỡ lỗi & Kiểm thử",
        "levels": {
            1: "Tìm và sửa lỗi cú pháp cơ bản.",
            2: "Phát hiện và sửa được các lỗi logic, xử lý ngoại lệ.",
            3: "Sử dụng được debugger, viết test case bằng JUnit.",
            4: "Integration test, kiểm thử trường hợp biên."
        },
        "max_level": 4
    },
    "modeling": {
        "name": "Mô hình hóa và thiết kế",
        "levels": {
            1: "Đọc/hiểu UML và use case đơn giản.",
            2: "Vẽ được sơ đồ use case, class diagram, sequence diagram,...",
            3: "Áp dụng Design Patterns (Factory, Singleton, Observer); áp dụng nguyên tắc SOLID.",
            4: "Thiết kế hệ thống phức tạp với UML + Design Patterns."
        },
        "max_level": 4
    },
    "abstraction": {
        "name": "Tổng quát hóa và cấu trúc dữ liệu",
        "levels": {
            1: "Generics và Collections cơ bản.",
            2: "Wildcards và ràng buộc.",
            3: "Các lớp wrapper như String, Array,...; các container tổng quát như List, Set,...",
            4: "Thành thạo lập trình tổng quát và cấu trúc dữ liệu, quan hệ giữa generics và thừa kế."
        },
        "max_level": 4
    }
}

# Đường dẫn đến thư mục chứa bài giảng
BASE_DIR = "E:/study/AI1-K67-UET/6.HKII-2024-2025/Business internship/eduplannern/back_end/"
LESSON_PLAN_DIR = os.path.join(BASE_DIR, "lessonplan")
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions")

def load_text_file(filename, default_content=""):
    """Hàm bổ trợ để đọc file an toàn từ thư mục lessonplan"""
    path = os.path.join(LESSON_PLAN_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Lỗi khi đọc file {filename}: {e}")
    return default_content

def get_lesson_template(topic_id):
    """Lấy nội dung bài giảng mẫu dựa trên ID chủ đề (ví dụ: lesson_1)"""
    # Tìm file lesson_1.txt, lesson_2.txt ...
    filename = f"{topic_id}.txt"
    # Nếu không tìm thấy file cụ thể, có thể fallback về file chung
    content = load_text_file(filename)
    if not content:
        content = load_text_file("oop_with_java_lessonplan.txt", "Nội dung bài giảng mặc định.")
    return content

def get_topic_questions(topic_id):
    """Lấy bộ câu hỏi mẫu dựa trên ID chủ đề"""
    # Tìm file questions_lesson_1.txt ... 
    questions = []
    questions_dir = os.path.join(QUESTIONS_FILE, topic_id)
    for filename in os.listdir(questions_dir):
        if re.match(r"question.*\.txt", filename):
            with open(os.path.join(questions_dir, filename), 'r', encoding='utf-8') as f:
                questions.extend(f.read().splitlines())
        
    return questions

TOPIC_TITLES = {
    'class_and_object': 'Bài 1: Giới thiệu về Đối tượng và Lớp',
    'inheritance': 'Bài 2: Tính kế thừa (Inheritance)',
    'polymorphism': 'Bài 3: Tính đa hình (Polymorphism)',
}

def get_topic_title(topic_id):
    return TOPIC_TITLES.get(topic_id, topic_id.replace('_', ' ').title())

# MOCK_INITIAL_LESSON_PLAN = """
# =====================================================
# CHỦ ĐỀ BÀI HỌC: Lập trình hướng đối tượng với Java
# =====================================================

# PHẦN 1: GIẢI THÍCH KIẾN THỨC
# ---------------------------------
# Lập trình hướng đối tượng (OOP) là kỹ thuật lập trình cho phép lập trình viên tạo ra các đối tượng trong code trừu tượng hóa các đối tượng thực tế.
# Các khái niệm cơ bản:
# 1. Lớp (Class): Khuôn mẫu để tạo đối tượng.
# 2. Đối tượng (Object): Thể hiện cụ thể của lớp.
# 3. Các tính chất: Đóng gói, Kế thừa, Đa hình, Trừu tượng.

# PHẦN 2: BÀI TẬP VẬN DỤNG
# ---------------------------------
# --- Bài tập 1 ---
# Câu hỏi: Tạo một class 'HocSinh' với thuộc tính ten và tuoi.
# Giải pháp: public class HocSinh { String ten; int tuoi; }
# Các lỗi sai thường gặp: Chưa khai báo kiểu dữ liệu.

# --- Bài tập 2 ---
# Câu hỏi: Khởi tạo đối tượng HocSinh trong hàm main.
# Giải pháp: HocSinh hs = new HocSinh();
# Các lỗi sai thường gặp: Quên từ khóa new.
# """

# MOCK_QUESTIONS = [
#     "Làm thế nào để đảm bảo tính đóng gói cho thuộc tính của lớp?",
#     "Tại sao cần sử dụng Constructor?",
#     "Sự khác biệt giữa Overloading và Overriding là gì?"
# ]