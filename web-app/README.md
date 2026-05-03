# Vietnamese AI Text Detection (Web App)

A Full-stack application (FastAPI + React) powered by Artificial Intelligence (Fine-tuned **PhoBERT v2** model) to detect and classify whether a Vietnamese text is **Human-written** or **AI-generated**.

This system is designed with Production standards, ensuring smooth inference on GPUs (with automatic NVIDIA CUDA detection) and providing a modern Glassmorphism user interface.

---

## Key Features
- **Smart AI Core (PhoBERT v2):** Utilizes a Transformer-based Deep Learning model specifically fine-tuned for Vietnamese grammar and syntax.
- **Auto GPU Optimization:** Automatically detects and offloads inference to the GPU (e.g., RTX 3050 Ti) for lightning-fast responses (< 0.2 seconds).
- **Natural Language Pre-processing:** Integrates Vietnamese word segmentation using the `underthesea` library before feeding data to the model.
- **Modern Interface (Glassmorphism):** Clean, intuitive UI with smart error handling and confidence score visualization via progress bars.
- **Strict API Security:** Multi-layer validation using Pydantic. Inputs must contain **between 100 and 2000 words** to ensure sufficient context for complexity analysis (Perplexity & Burstiness) while preventing system overload.
- **1-Click Experience:** Start the entire Backend and Frontend server cluster with a single click (Windows).

---

## Tech Stack
### Backend
- **Framework:** FastAPI, Uvicorn
- **AI / Deep Learning:** PyTorch, HuggingFace Transformers, Safetensors
- **NLP Processing:** Underthesea
- **Data Validation:** Pydantic
- **Testing:** Pytest, HTTPX

### Frontend
- **Core:** React 18, Vite
- **Styling:** Tailwind CSS, PostCSS
- **Icons:** Lucide React

---

## Directory Structure
```text
vietnamese-ai-detection/web-app/
├── Start-App.bat             # 1-click script to start the whole system (Windows)
├── README.md                 # Documentation
├── backend/                  # FastAPI source code
│   ├── app/
│   │   ├── main.py           # App initialization, CORS & Lifespan config
│   │   ├── api.py            # Route handlers (/v1/detect)
│   │   ├── schemas.py        # Pydantic models (Validations)
│   │   └── services/
│   │       └── ai_service.py # Model Loading & AI Inference
│   ├── model/
│   │   └── phobert-finetuned-v2/ # Directory for Kaggle model weights
│   ├── tests/                # Unit tests (pytest)
│   ├── requirements.txt      # Python dependencies
│   └── install.ps1           # Auto-install script (Installs PyTorch CUDA)
└── frontend/                 # React source code
    ├── src/
    │   ├── App.jsx           # Main UI logic
    │   ├── index.css         # Global CSS (Tailwind directives)
    │   └── components/
    │       └── DetectionResult.jsx # Result display component
    ├── package.json          # Node.js dependencies
    ├── tailwind.config.js    # UI configuration
    └── vite.config.js        # Build tool configuration
```

---

## Installation & Usage

### Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/) (LTS recommended)
- *(Optional)* NVIDIA Graphics Card for CUDA acceleration (will fallback to CPU if unavailable).

### Step 1: Load Model Weights
Due to size limits, the AI model weights are not included directly in the repository. You need to download them from the training pipeline:
1. Download your fine-tuned PhoBERT model folder (e.g., from Kaggle/Colab).
2. Place the files (`model.safetensors`, `config.json`, `vocab.txt`, `bpe.codes`) into the following path:
   `backend/model/phobert-finetuned-v2/`

### Step 2: 1-Click Start (Windows)
You don't need to remember complicated configuration commands. In the project root directory, simply double-click the file:
**`Start-App.bat`**

The system will automatically set environment variables, open 2 background windows running FastAPI and React, and the app will be available at: **http://localhost:5173**

---

### Step 2 (Advanced): Manual Start via CMD

**Start Backend:**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn app.main:app --reload
```
*Backend will run at: `http://127.0.0.1:8000`*

**Start Frontend:**
```cmd
cd frontend
npm install
npm run dev
```
*Frontend will run at: `http://localhost:5173`*

---

## API Reference

### AI Text Detection
- **Endpoint:** `POST /v1/detect`
- **Content-Type:** `application/json`

**Request Body:**
```json
{
  "content": "Một cuộc sống ý nghĩa là khi ta biết trân trọng từng khoảnh khắc, biết yêu thương gia đình..." 
}
```
*(Note: The `content` string must contain **between 100 and 2000 words**. Otherwise, the API will throw an `HTTP 422 Unprocessable Entity` error).*

**Response (Success):**
```json
{
  "is_human": true,
  "human_prob": 98.45,
  "ai_prob": 1.55,
  "message": "Phân tích thành công"
}
```

---

## Testing

To run the backend unit tests using pytest:

```cmd
cd backend
venv\Scripts\activate.bat
pytest tests/test_api.py -v
```
This runs automated tests to ensure API logic (word limits, payload structure) functions correctly without needing to load the heavy AI model.

---

## Engineering Notes
- **Word Limits vs Context Window:** The system blocks inputs under 100 words and over 2000 words at the API level. This prevents Out of Distribution (OOD) noise and system overload. For valid long texts, they will be seamlessly truncated (`truncation=True, max_length=256`) by the HuggingFace Tokenizer.
- **Probabilities & Confidence:** The `human_prob` and `ai_prob` parameters directly reflect the **Softmax** activation function applied to the model's output logits.
