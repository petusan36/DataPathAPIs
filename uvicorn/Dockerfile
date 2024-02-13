# Step 1: Use official lightweight Python image as base OS.
FROM python:3.9
LABEL authors="Pedro Turriago Sanchez"

# Step 2. Copy local code to the container image.
WORKDIR /app

COPY . .

# Step 3. Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPOINT ["top", "-b"]
CMD ["uvicorn", "main:appCollections", "--host", "0.0.0.0", "--port", "8080"]