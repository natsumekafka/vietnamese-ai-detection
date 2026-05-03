@echo off
title Khoi dong AI Text Detection
echo ==========================================
echo    KHOI DONG HE THONG AI TEXT DETECTION
echo ==========================================

:: Ép thêm Node.js vào PATH tạm thời
set PATH=%PATH%;C:\Program Files\nodejs\

:: Khởi động Backend trong cửa sổ mới
echo [1/2] Dang mo Backend (FastAPI)...
start "AI Backend Server" cmd /k "cd /d d:\detector_web\backend && venv\Scripts\activate.bat && uvicorn app.main:app --reload"

:: Đợi 2 giây cho Backend chạy
timeout /t 2 /nobreak >nul

:: Khởi động Frontend trong cửa sổ mới
echo [2/2] Dang mo Frontend (React)...
start "AI Frontend Server" cmd /k "cd /d d:\detector_web\frontend && npm run dev"

echo.
echo ==========================================
echo TAT CA DA DUOC KHOI DONG!
echo.
echo Vui long mo trinh duyet va truy cap link:
echo http://localhost:5173
echo.
echo De tat ung dung, ban chi can dong 2 cua so den hien ra la duoc.
echo ==========================================
pause
