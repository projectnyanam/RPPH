# Gunakan image Python resmi yang ringan
FROM python:3.10-slim

# Tentukan working directory di dalam kontainer
WORKDIR /code

# Salin file requirements.txt terlebih dahulu untuk memanfaatkan cache Docker
COPY ./requirements.txt /code/requirements.txt

# Instal semua library yang dibutuhkan
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Salin seluruh kode aplikasi (main.py, dll) ke dalam kontainer
COPY . .

# Hugging Face Spaces secara default menjalankan aplikasi pada port 7860
# Jalankan Uvicorn server untuk FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
