import { UserProfile } from "../types";

export const generateLectureContent = async (profile: UserProfile): Promise<string> => {
  try {
    const response = await fetch('/api/generate-lecture', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(profile),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Lỗi Server: ${response.status}`);
    }

    const data = await response.json();
    return data.result;

  } catch (error: any) {
    console.error("Lỗi kết nối Backend:", error);
    return `Không thể tạo bài giảng.\n\nLỗi: ${error.message}\n\nHãy đảm bảo bạn đã chạy Backend (python server.py) ở cổng 5000.`;
  }
};