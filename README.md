# Window Manufacturing Chatbot

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)
![LangChain](https://img.shields.io/badge/LangChain-008080?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai)

Window Manufacturing Chatbot is a web-based application designed to assist users with questions related to window manufacturing. Leveraging the power of Large Language Models (LLMs) via OpenAI, the chatbot provides detailed and accurate information about different types of windows, manufacturing processes, installation, maintenance, and more. The application ensures a smooth conversational context to handle follow-up questions effectively.

## 🌐 Architecture

The application architecture includes:

- **FastAPI**: Serves as the web framework for building the API.
- **Redis Queue and Pub/Sub**: Used for managing tasks and message brokering.
- **Sockets**: For real-time communication between the client and server.
- **Docker**: Containerizes the application for easy deployment.
- **LangChain**: Manages conversational context and dialogue flow.
- **OpenAI LLM**: Provides the intelligence behind the chatbot’s responses.

This architecture facilitates a robust and scalable chatbot application, capable of handling multiple user interactions and maintaining context throughout the conversation.

## 🚀 Getting Started

To start using the Window Manufacturing Chatbot, follow these steps:

### 🛠️ Prerequisites

Before you start, ensure you have the following installed:

- Docker
- Git

### 🛠️ Installation

#### Step 1: Clone the Repository

Clone the Window Manufacturing Chatbot repository to your local machine:

```bash
git clone https://github.com/RamishUrRehman007/WindowManufacturingBot.git
