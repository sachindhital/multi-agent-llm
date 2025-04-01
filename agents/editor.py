from crewai import Agent

def create_editor():
    return Agent(
        role="Editor",
        goal="Edit the blog post to match journalistic standards.",
        backstory="You're the final reviewer for clarity, grammar, and tone.",
        allow_delegation=False,
        verbose=True
    )
