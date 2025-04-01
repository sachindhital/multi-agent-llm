def generate_blog(topic: str, breakdown: str = "") -> dict:
    from llm.agents.planner import create_planner
    from llm.agents.writer import create_writer
    from llm.agents.editor import create_editor
    from llm.agents.image_prompt_agent import ImagePromptAgent
    from llm.agents.image_generator_agent import ImageGeneratorAgent
    from crewai import Task, Crew

    # Add the trend breakdown context
    context = f"\nTrend Context:\n{breakdown}" if breakdown else ""

    planner = create_planner(topic + context)
    writer = create_writer(topic + context)
    editor = create_editor()

    # Define tasks
    plan = Task(
        description=(
            f"Create a content plan for the topic: {topic}. "
            "Include audience analysis, SEO keywords, and structure." + context
        ),
        expected_output="A detailed blog plan document.",
        agent=planner
    )

    write = Task(
        description=(
            f"Write the blog post based on the planner's work for: {topic}. "
            "Incorporate the trend insights if provided." + context
        ),
        expected_output="A full markdown blog article.",
        agent=writer
    )

    edit = Task(
        description="Proofread the blog for tone, grammar, and flow.",
        expected_output="Final version of the blog, ready to publish.",
        agent=editor
    )

    # Run the crew
    crew = Crew(agents=[planner, writer, editor], tasks=[plan, write, edit], verbose=2)
    blog_content = crew.kickoff(inputs={"topic": topic})

    # Generate image prompts
    image_prompt_agent = ImagePromptAgent()
    image_prompts = image_prompt_agent.generate_prompts(blog_content)

    # Generate image URLs
    image_generator_agent = ImageGeneratorAgent()
    image_urls = image_generator_agent.generate_images(image_prompts)

    # Final structured response
    return {
        "topic": topic,
        "blog": blog_content,
        "image_prompts": image_prompts,
        "image_urls": image_urls
    }
