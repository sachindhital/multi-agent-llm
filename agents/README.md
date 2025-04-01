📂 Project Structure

llm/
├── agents/
├── app/
├── core/
├── .env
├── requirements.txt
└── blog_api.py



# 🧠 Multi-Agent Blog Generator

This project generates blog articles using LLM agents (Planner, Writer, Editor) and automatically creates DALL·E 3 images for each post.

## 🧩 Features

- 🧠 Blog planning, writing, editing with CrewAI agents
- 🎨 Image prompts generated from content
- 🖼️ DALL·E 3 image generation (via OpenAI API)
- 🌐 Flask frontend + FastAPI backend
- 📦 Modular code structure with `.env` for secrets

## 💻 Local Setup

```bash
git clone https://github.com/your-username/multi-agent-llm.git
cd multi-agent-llm
python -m venv llm
source llm/bin/activate  # or .\llm\Scripts\activate (Windows)
pip install -r requirements.txt


