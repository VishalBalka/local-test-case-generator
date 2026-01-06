# 🤖 Local Test Case Generator

A powerful, privacy-focused tool that uses Local LLMs (via Ollama) to automatically generate comprehensive QA test cases from PDF, DOCX, and Text requirements.

## ✨ Features
- **100% Local**: No API keys required. Your data never leaves your machine.
- **Multi-Format Support**: Parses `.pdf`, `.docx`, and `.txt` files.
- **Structured Output**: Generates test cases with IDs, Titles, Steps, and Expected Results.
- **LLM Integration**: Built with LangChain and optimized for `llama3.2`.

---

## 🛠️ Prerequisites

### 1. Install Ollama
Download and install Ollama from [ollama.com](https://ollama.com).

### 2. Pull the Model
Open your terminal and run:
```bash
ollama pull llama3.2:3b