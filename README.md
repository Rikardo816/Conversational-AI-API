# Conversational AI API

## Descripción

Este proyecto implementa un sistema conversacional utilizando un Large Language Model (LLM) expuesto a través de una API REST usando FastAPI. El sistema acepta archivos de audio y devuelve respuestas en formato de audio.

## Tecnologías

- Python
- FastAPI
- Langchain
- Docker

## Cómo Ejecutar
Antes que nada cree un archivo `.env` en la raiz del proyecto y añada las variables de entorno dentro de el, justo como se muestra acontinuación:
```
OPENAI_API_KEY=su_clave_openai
OPENAI_MODEL=gpt-3.5-turbo
``` 
Reemplaze `su_clave_openai` por la que usted posea, si no tiene una puede crearla en [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Local
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
### Con Docker (recomendado)
1. Construir y ejecutar con Docker:
    ```bash
    docker-compose up --build
    ```

## Endpoints

- `POST /conversation/`: Subir texto o archivo de audio, si se sube un audio la respuesta será en audio de lo contrario será en texto.

## Documentación API
La documentación de la API está disponible en `/docs` (Swagger) y `/redoc`.
