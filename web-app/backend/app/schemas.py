from pydantic import BaseModel, Field, field_validator

class DetectionRequest(BaseModel):
    content: str = Field(..., description="Văn bản cần kiểm tra AI (tối thiểu 100 từ).")

    @field_validator('content')
    @classmethod
    def validate_word_count(cls, v: str):
        words = [w for w in v.split() if w.strip()]
        if len(words) < 100:
            raise ValueError(f"Văn bản quá ngắn (chỉ có {len(words)} từ). Vui lòng nhập tối thiểu 100 từ để hệ thống phân tích chính xác.")
        if len(words) > 2000:
            raise ValueError(f"Văn bản quá dài (có {len(words)} từ). Vui lòng nhập tối đa 2000 từ để tránh quá tải hệ thống.")
        return v

class DetectionResponse(BaseModel):
    is_human: bool
    human_prob: float
    ai_prob: float
    message: str = "Success"
