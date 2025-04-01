from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Agent, Task, Crew
import os
from utils import get_openai_api_key
import markdown
# Set up API key
openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

app = FastAPI(title="Blog Generator API")

class TopicRequest(BaseModel):
    topic: str

@app.post("/generate_blog")
def generate_blog(request: TopicRequest):
    try:
        # Create agents
        planner = Agent(
            role="Content Planner",
            goal=f"Plan engaging and factually accurate content on {request.topic}",
            backstory=f"You're working on planning a blog article about the topic: {request.topic}.",
            allow_delegation=False,
            verbose=True
        )

        writer = Agent(
            role="Content Writer",
            goal=f"Write insightful and factually accurate opinion piece about the topic: {request.topic}",
            backstory=f"You're working on a writing a new opinion piece about the topic: {request.topic}.",
            allow_delegation=False,
            verbose=True
        )

        editor = Agent(
            role="Editor",
            goal="Edit a given blog post to align with the writing style of the organization.",
            backstory="You are an editor who receives a blog post from the Content Writer.",
            allow_delegation=False,
            verbose=True
        )

        # Create tasks
        plan = Task(
            description=(
                "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
                "2. Identify the target audience, their interests, and pain points.\n"
                "3. Develop a detailed content outline including intro, key points, and call to action.\n"
                "4. Include SEO keywords and relevant sources."
            ),
            expected_output="A comprehensive content plan document including outline, audience analysis, and keywords.",
            agent=planner,
        )

        write = Task(
            description=(
                "1. Use the content plan to craft a compelling blog post.\n"
                "2. Incorporate SEO keywords naturally.\n"
                "3. Properly name sections/subtitles.\n"
                "4. Ensure good structure and brand voice."
            ),
            expected_output="A well-written blog post in markdown format.",
            agent=writer,
        )

        edit = Task(
            description="Proofread the blog post for grammar and tone alignment.",
            expected_output="A polished blog post ready for publishing.",
            agent=editor
        )

        # Run the crew
        crew = Crew(agents=[planner, writer, editor], tasks=[plan, write, edit], verbose=2)
        result = crew.kickoff(inputs={"topic": request.topic})

        return {"topic": request.topic, "blog": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---- Flask Frontend ----
from flask import Flask, render_template, request as flask_request
import requests

flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET', 'POST'])
def home():
    blog = None
    if flask_request.method == 'POST':
        topic = flask_request.form['topic']
        response = requests.post("http://localhost:8000/generate_blog", json={"topic": topic})
    if response.status_code == 200:
        markdown_blog = response.json()['blog']
        blog = markdown.markdown(markdown_blog)  # ✅ Convert to HTML
    else:
        blog = f"<p style='color:red'>Error: {response.text}</p>"
    return render_template('index.html', blog=blog)

if __name__ == '__main__':
    flask_app.run(debug=True, port=5000)
