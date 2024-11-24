FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglu1-mesa \
    libxrender1 \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*


RUN python -m pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .