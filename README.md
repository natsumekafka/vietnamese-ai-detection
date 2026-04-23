# Detecting AI-generated Vietnamese Text

Fine-tuning PhoBERT and mDeBERTa to classify AI-generated vs human-written Vietnamese essays.

## Dataset
- [Vietnamese AI Detection v0](https://www.kaggle.com/datasets/natsumekafka/vietnamese-ai-detection-v0)
- 2,993 train / 374 val / 375 test
- Labels: `ai` (Gemini 2.5 Flash) vs `human` (student essays)

## Models & Results

| Model | Accuracy | F1 (macro) | AUROC |
|-------|----------|------------|-------|
| PhoBERT-base-v2 | 97.6% | 97.65% | ? |
| mDeBERTa-v3-base | 97.3% | 97.33% | 99.87% |

## Model Details

### PhoBERT-base-v2
- Word segmentation: `underthesea`
- Max length: 256 tokens
- Input: `text_seg` (pre-segmented)

### mDeBERTa-v3-base
- No word segmentation needed (multilingual)
- Max length: 512 tokens
- Input: raw `text`
- Precision: float32 (fp16/bf16 not supported)

## Notebooks
- `notebooks/PhoBert-fine-tuned.ipynb` — PhoBERT Training + Evaluation
- `notebooks/mDeBERTa-fine-tuned.ipynb` — mDeBERTa Training + Evaluation

## Out-of-distribution Analysis

| AI Source | Accuracy |
|-----------|----------|
| Gemini 2.5 Flash (in-distribution) | ~100% |
| Gemini 3 Fast | 80% |
| Gemini 3.1 Pro | 40-50% |
| ChatGPT | 0% |

> Model thực chất là **Gemini 2.5 Flash detector** — generalizes kém với các LLM khác do giới hạn của dataset.

## Key Findings
- Model học pattern của Gemini 2.5 Flash, không generalize tốt sang LLM khác họ
- Model lớn hơn (Pro) tạo văn bản khó detect hơn model nhỏ (Flash, Fast)

## Future Work
- Thêm data từ GPT, Claude, Llama để model generalize tốt hơn
- Cập nhật dataset theo từng thế hệ LLM mới