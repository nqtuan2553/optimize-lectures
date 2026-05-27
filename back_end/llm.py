from google import genai
from config import GOOGLE_API_KEY

class LLMClient:
    def __init__(self, model_name="gemini-2.5-flash"):
        if GOOGLE_API_KEY:
            try:
                self.client = genai.Client(api_key=GOOGLE_API_KEY)
            except Exception as e:
                print(f"Lỗi cấu hình API Client: {e}")
                self.client = None
        else:
            print("LỖI: Không có API Key.")
            self.client = None
        
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        if not self.client:
            return "Lỗi: Chưa cấu hình API Key hoặc Client khởi tạo thất bại."
            
        try:
            # SDK mới: client.models.generate_content
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Đã xảy ra lỗi khi gọi API của LLM: {e}")
            return f"Lỗi: Không thể tạo nội dung. {e}"