FROM python:3.10-alpine

WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port for the FastAPI
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "quake_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
