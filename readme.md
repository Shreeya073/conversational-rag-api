# Conversational RAG API

A FastAPI-based REST API for conversational question answering using **Retrieval-Augmented Generation (RAG)**.

## Features

* Multi-turn conversational queries
* Custom RAG pipeline
* Redis-based chat memory
* LLM integration
* Context-aware responses
* Interview booking with name, email, date, and time
* MySQL database for storing bookings

## Technologies

* Python
* FastAPI
* LLM
* Ollama
* Redis
* MySQL

## Database Setup

```bash
python -m app.core.init_db
```

## Run the API

```bash
uvicorn app.main:app --reload
```
## Run the Console

```bash
python -m app.console  
```
API documentation:

`http://127.0.0.1:8000/docs`

## Demo

## Console Demo

![Console Chat](docs/image.png)