import os
import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from underthesea import word_tokenize
import logging

logger = logging.getLogger(__name__)

class AIInferenceService:
    def __init__(self, model_dir: str = "phobert-finetuned"):
        self.model_dir = model_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        self.is_ready = False

    def load_model(self):
        """Load model and tokenizer from the local directory."""
        if not os.path.exists(self.model_dir):
            logger.error(f"Thư mục model không tồn tại: {os.path.abspath(self.model_dir)}")
            logger.error("Vui lòng tải model từ Kaggle và đặt vào thư mục này.")
            return False

        try:
            logger.info(f"Loading tokenizer từ {self.model_dir}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
            
            logger.info(f"Loading model từ {self.model_dir} lên {self.device}...")
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_dir)
            self.model.to(self.device)
            self.model.eval()
            self.is_ready = True
            logger.info("Model loaded successfully!")
            return True
        except Exception as e:
            logger.error(f"Lỗi khi load model: {str(e)}")
            return False

    def predict(self, text: str):
        """Thực hiện dự đoán: trả về xác suất Human và AI."""
        if not self.is_ready:
            raise RuntimeError("Model chưa sẵn sàng. Vui lòng kiểm tra lại quá trình load model.")

        # Bước 1: Word segment bằng underthesea
        try:
            segmented_text = word_tokenize(text, format="text")
        except Exception as e:
            logger.error(f"Lỗi khi word_tokenize: {str(e)}")
            segmented_text = text # Fallback

        # Bước 2: Tokenize với max_length=256, truncation=True
        inputs = self.tokenizer(
            segmented_text,
            max_length=256,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # Chuyển input lên thiết bị (GPU/CPU)
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        # Bước 3: Inference qua model lấy logits
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits

        # Bước 4: Softmax tính xác suất
        probs = F.softmax(logits, dim=1).squeeze().tolist()
        
        # Lớp 0: Human, Lớp 1: AI (theo cấu trúc user mô tả)
        human_prob = float(probs[0])
        ai_prob = float(probs[1])

        return {
            "human_prob": human_prob * 100,
            "ai_prob": ai_prob * 100,
            "is_human": human_prob > ai_prob
        }
