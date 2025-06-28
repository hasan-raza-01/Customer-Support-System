FROM python:3.10-slim-bullseye
RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y gcc build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install --upgrade pip uv 
# RUN uv pip install --system -e .
RUN uv pip install -e .
EXPOSE 8000  
CMD ["uv", "run", "app.py"]
