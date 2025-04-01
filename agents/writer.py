from crewai import Agent

def create_writer(topic: str):
    return Agent(
        role="Content Writer",
        goal=f"Write insightful opinion piece about {topic}",
        backstory=f"You write based on the planner's outline for topic: {topic}.",
        allow_delegation=False,
        verbose=True
    )
