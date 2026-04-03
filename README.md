# Mortenson Pre-Task Planning (PTP) Agent

An AI-driven system designed to standardize and elevate pre-task planning across global campuses. This demo showcases Google's agentic AI capabilities integrated with Mortenson's corporate identity.

## 🚀 Overview

The PTP Agent serves as a bridge between program-level knowledge and site-level execution. It synthesizes schedule data (Primavera P6), safety records (IRIS), and technical specifications to generate high-fidelity, task-specific execution plans ("Smart PTPs").

This project consists of:
1.  **A Modular Agent Backend** built with the **Google ADK** (Agent Development Kit), designed to be deployable into Vertex AI Agent Engine.
2.  **A Clean Web UI** reflecting Mortenson's corporate branding, featuring a crisp light mode.

## 🏗️ Architecture

-   **Backend**: FastAPI proxy that communicates with the Google ADK Agent. It handles Server-Sent Events (SSE) to stream responses and tool execution traces to the frontend.
-   **Frontend**: A static web application (HTML/CSS/JS) served via a minimal FastAPI server.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI, Google ADK, `google-genai` SDK.
-   **Frontend**: Vanilla HTML5, CSS3, JavaScript.
-   **Fonts**: Adobe Typekit (`urw-din`).

## ⚙️ Setup & Installation

### Prerequisites

-   Python 3.10+
-   `uv` for package management
-   Google Cloud Credentials (ADC) with access to Vertex AI.

### Backend Setup

1.  Navigate to the `ptp-agent` directory:
    ```bash
    cd ptp-agent
    ```
2.  Create a `.env` file based on the environment variables needed (see below).
3.  Run the backend server:
    ```bash
    uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Run the frontend server (defaults to port 3000):
    ```bash
    uv run uvicorn main:app --port 3000 --reload
    ```
3.  Open your browser and navigate to `http://localhost:3000`.

## 🔒 Environment Variables

Create a `.env` file in the `ptp-agent` directory with the following variables:

```env
GCP_PROJECT_ID=your-gcp-project-id
GCP_LOCATION=us-central1
USE_VERTEX_AI=true
```

## 🌟 Key Features

-   **Interactive Test Prompts**: Quick-click pills to test common scenarios (e.g., listing high-risk tasks).
-   **Spontaneous Agent Verification**: A dedicated "Ask For Verification" button that triggers the agent to proactively ask a critical safety double-check question without echoing any user prompts, simulating an agent-initiated interaction.
-   **Tool Tracing**: Visual indicators in the chat when the agent invokes specific tools (like querying schedule or safety records).
-   **Crisp Light Mode**: Styled according to Mortenson's corporate guidelines with official standard Adobe Typekit fonts and dynamic SVG logos.
