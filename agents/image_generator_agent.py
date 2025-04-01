# llm/agents/image_generator_agent.py

import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

class ImageGeneratorAgent:
    def __init__(self, model="dall-e-3", size="1024x1024", quality="standard"):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file.")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.size = size
        self.quality = quality

    def generate_images(self, prompts, download=False, output_dir="generated_images"):
        urls = []
        if download:
            os.makedirs(output_dir, exist_ok=True)

        for i, prompt in enumerate(prompts, 1):
            print(f"🎨 Generating image for prompt {i}: {prompt}")
            response = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=self.size,
                quality=self.quality,
                n=1
            )
            image_url = response.data[0].url
            urls.append(image_url)

            if download:
                img_data = requests.get(image_url).content
                file_path = os.path.join(output_dir, f"image_{i}.png")
                with open(file_path, 'wb') as f:
                    f.write(img_data)
                print(f"✅ Saved to {file_path}")
            else:
                print(f"🖼️ URL: {image_url}")

        return urls
