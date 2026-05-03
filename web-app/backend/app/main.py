from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .api import router as v1_router
from .services.ai_service import AIInferenceService

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo instance của service với đường dẫn mới
ai_service = AIInferenceService(model_dir="model/phobert-finetuned-v2")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi chạy khi startup
    logger.info("Bắt đầu khởi động hệ thống...")
    success = ai_service.load_model()
    if not success:
        logger.warning("CẢNH BÁO: Không thể load model. API phân tích sẽ trả về lỗi 503 cho đến khi model được cập nhật.")
    yield
    # Dọn dẹp khi shutdown
    logger.info("Đang tắt hệ thống...")

app = FastAPI(
    title="Vietnamese AI Text Detection API",
    description="API phát hiện văn bản tiếng Việt do AI tạo ra sử dụng PhoBERT v2.",
    version="1.0.0",
    lifespan=lifespan
)

# Cấu hình CORS để frontend React có thể gọi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Có thể đổi thành cụ thể (VD: ["http://localhost:5173"]) khi lên production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn router
app.include_router(v1_router, prefix="/v1", tags=["Detection"])

@app.get("/")
def health_check():
    return {
        "status": "online",
        "model_ready": ai_service.is_ready,
        "device": str(ai_service.device)
    }
