# 使用官方 Python 3.11 映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案檔案
COPY . .

# 暴露 FastAPI 預設埠號
EXPOSE 8000

# 啟動指令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
