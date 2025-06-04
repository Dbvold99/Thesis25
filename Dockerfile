# Base image from VALIS
FROM cdgatenbee/valis-wsi AS base

FROM base AS dev

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev zlib1g-dev libgl1 \
    cmake g++ pkg-config libglib2.0-dev libxml2-dev \
    git \
    default-jdk \
    libvips-dev \
    librsvg2-dev \
 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY config.yaml ./
COPY get_config.py ./
COPY src/ src/

RUN pip install --upgrade pip && pip install --no-cache-dir -e .

FROM base AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    librsvg2-dev \
 && rm -rf /var/lib/apt/lists/*

COPY --from=dev /usr/local /usr/local

COPY config.yaml ./
COPY get_config.py ./
COPY src/ src/

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-m"]