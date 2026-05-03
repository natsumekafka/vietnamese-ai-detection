# Script để cài đặt PyTorch với CUDA 11.8/12.1 và các thư viện khác
# Dành cho Windows với GPU NVIDIA (VD: RTX 3050 Ti)

Write-Host "Installing PyTorch with CUDA support..." -ForegroundColor Green
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

Write-Host "Installing other requirements..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host "Installation completed!" -ForegroundColor Green
