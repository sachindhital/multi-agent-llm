# llm/agents/image_prompt_agent.py

import os
from dotenv import load_dotenv
from openai import OpenAI

class ImagePromptAgent:
    def __init__(self, model="gpt-4"):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_prompts(self, blog_content, num_prompts=4):
        system_message = {
            "role": "system",
            "content": (
                "You are an assistant that creates vivid, creative DALL·E 3 image prompts "
                "based on blog content. Each prompt should describe a unique and visually rich scene "
                "that matches the themes, settings, or events described in the blog."
            )
        }

        user_message = {
            "role": "user",
            "content": (
                f"Based on the following blog content, generate {num_prompts} unique and creative prompts "
                f"for images that could visually represent different parts of the article:\n\n"
                f"{blog_content}"
            )
        }

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[system_message, user_message],
            temperature=0.8
        )

        output = response.choices[0].message.content.strip()
        prompts = [line.strip("- ").strip() for line in output.splitlines() if line.strip()]
        return prompts
