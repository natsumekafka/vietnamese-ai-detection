from fastapi import APIRouter, HTTPException, Depends
from .schemas import DetectionRequest, DetectionResponse
from .services.ai_service import AIInferenceService

router = APIRouter()

# Hàm lấy model instance đã được load trong main.py
def get_ai_service():
    from .main import ai_service
    return ai_service

@router.post("/detect", response_model=DetectionResponse)
async def detect_ai_text(request: DetectionRequest, service: AIInferenceService = Depends(get_ai_service)):
    if not service.is_ready:
        raise HTTPException(
            status_code=503,
            detail="Model chưa được tải hoặc chưa sẵn sàng. Vui lòng kiểm tra lại quá trình khởi động."
        )
    
    try:
        # Gọi hàm dự đoán
        result = service.predict(request.content)
        
        return DetectionResponse(
            is_human=result["is_human"],
            human_prob=result["human_prob"],
            ai_prob=result["ai_prob"],
            message="Phân tích thành công"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi trong quá trình phân tích: {str(e)}")
