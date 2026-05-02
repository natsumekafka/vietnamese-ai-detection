# Detecting AI-generated Vietnamese Text

Fine-tuning PhoBERT and mDeBERTa to classify AI-generated vs human-written Vietnamese essays.

## Dataset
- [Vietnamese AI Detection v0](https://www.kaggle.com/datasets/natsumekafka/vietnamese-ai-detection-v0)
- 2,993 train / 374 val / 375 test
- Labels: `ai` (Gemini 2.5 Flash) vs `human` (student essays)

## Models & Results

| Model | Accuracy | F1 (macro) | AUROC |
|-------|----------|------------|-------|
| PhoBERT-base-v2 | 96.8% | 96.8% | 99.84% |
| mDeBERTa-v3-base | 97.3% | 97.3% | 99.87% |

## Model Details

### PhoBERT-base-v2
- Word segmentation: `underthesea`
- Max length: 256 tokens
- Input: `text_seg` (pre-segmented)
- learning_rate: 2e-5
- weight_decay: 0.05
- label_smoothing: 0.1
- Early stopping: patience=2 (stopped at epoch 4)
- ECE (Calibration): 0.040 at T=1.0 
- Confidence: 0% predictions exceed 99% (well-calibrated)

### mDeBERTa-v3-base
- No word segmentation needed (multilingual)
- Max length: 512 tokens
- Input: raw `text`
- Precision: float32 (fp16/bf16 not supported)

## Notebooks
- `notebooks/PhoBert-fine-tuned-v2.ipynb` — PhoBERT Training + Evaluation
- `notebooks/mDeBERTa-fine-tuned.ipynb` — mDeBERTa Training + Evaluation

## Technologies
- **Crawling**: Python, requests, BeautifulSoup
- **AI Generation**: Google Gemini 2.5 Flash API
- **Processing**: pandas, underthesea, scikit-learn
- **Training**: PyTorch, HuggingFace Transformers
- **Models**: PhoBERT-base-v2, mDeBERTa-v3-base
- **Evaluation**: scikit-learn, scipy
- **Infrastructure**: Kaggle (GPU T4 x2), GitHub

## Future Work
- Add training data from GPT, Claude, Llama for better generalization
- Update dataset continuously as new LLM generations emerge
- Explore watermarking-based detection as complement to stylistic analysis
- Investigate topic-dependent detection bias
- Ensemble PhoBERT + mDeBERTa for improved robustness
