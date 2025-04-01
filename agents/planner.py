from crewai import Agent

def create_planner(topic: str):
    return Agent(
        role="Content Planner",
        goal=f"Plan engaging and factually accurate content on {topic}",
        backstory=f"You're working on planning a blog article about the topic: {topic}.",
        allow_delegation=False,
        verbose=True
    )
