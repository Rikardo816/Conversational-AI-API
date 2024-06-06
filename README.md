# Conversational AI API

## Descripción

Este proyecto implementa un sistema conversacional utilizando un Large Language Model (LLM) expuesto a través de una API REST usando FastAPI. El sistema acepta archivos de audio y devuelve respuestas en formato de audio.

## Tecnologías

- Python
- FastAPI
- Langchain
- Docker

## Cómo Ejecutar

1. Clonar el repositorio.
2. Crear un entorno virtual e instalar las dependencias:
    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
3. Ejecutar la aplicación:
    ```bash
    uvicorn app.main:app --reload
    ```
4. Construir y ejecutar con Docker:
    ```bash
    docker-compose up --build
    ```

## Endpoints

- `POST /upload-audio/`: Subir un archivo de audio y obtener una respuesta en audio.
- `POST /converse/`: Enviar texto y recibir una respuesta en texto.

## Documentación API

La documentación de la API está disponible en `/docs` (Swagger) y `/redoc`.
