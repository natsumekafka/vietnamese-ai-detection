from fastapi.testclient import TestClient
from app.main import app
from app.api import get_ai_service

# Khởi tạo TestClient
client = TestClient(app)

# Tạo một class Mock (giả lập) AI Service để không phải tải model thật (tránh nặng máy và tốn thời gian khi test)
class MockAIService:
    def __init__(self):
        self.is_ready = True
        self.device = "cpu"

    def predict(self, text: str):
        # Trả về kết quả giả định (Mock data)
        return {
            "human_prob": 95.5,
            "ai_prob": 4.5,
            "is_human": True
        }

# Hàm thay thế dependency get_ai_service bằng MockAIService
def override_get_ai_service():
    return MockAIService()

# Ghi đè dependency của ứng dụng FastAPI
app.dependency_overrides[get_ai_service] = override_get_ai_service

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_detect_text_too_short():
    short_text = "Đoạn văn này quá ngắn, không đủ một trăm từ để phân tích chính xác."
    response = client.post(
        "/v1/detect",
        json={"content": short_text}
    )
    assert response.status_code == 422
    assert "tối thiểu 100 từ" in response.text

def test_detect_text_too_long():
    # Tạo văn bản dài hơn 2000 từ
    long_text = "từ " * 2001
    response = client.post(
        "/v1/detect",
        json={"content": long_text}
    )
    assert response.status_code == 422
    assert "tối đa 2000 từ" in response.text

def test_detect_valid_text():
    # Tạo đoạn văn hợp lệ có khoảng hơn 100 từ và dưới 2000 từ
    # (Mỗi câu dưới đây có 8 từ, lặp 15 lần => 120 từ)
    valid_text = "Đây là một câu văn hợp lệ để test. " * 15
    
    response = client.post(
        "/v1/detect",
        json={"content": valid_text}
    )
    
    # Kiểm tra mã trả về có phải là 200 OK không
    assert response.status_code == 200
    
    # Kiểm tra nội dung JSON trả về
    data = response.json()
    assert "is_human" in data
    assert "human_prob" in data
    assert "ai_prob" in data
    assert data["message"] == "Phân tích thành công"
    
    # Do chúng ta dùng MockAIService, kết quả trả về sẽ giống hệt dữ liệu mock
    assert data["human_prob"] == 95.5
    assert data["ai_prob"] == 4.5
    assert data["is_human"] == True
