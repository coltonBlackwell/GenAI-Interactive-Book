import os
from openai import OpenAI
import pyttsx3


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

animal1 = "cat"
animal2 = "dragon"

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": """You are a FAMILY FRIENDLY AI designed to create clear stories for children. Also, when asked, you provide a short and vivid image generation prompt that represents the story visually."""
        },
        {
            "role": "user",
            "content": (
                f"Create a very short story about a {animal1} and a {animal2} who become friends. "
                "Also give me a separate short, vivid, and descriptive prompt that could be used to create an image of the story."
                "\n\nRespond in this format:\nStory: <story here>\nImagePrompt: <short visual prompt here>"
            )
        },
    ],
    max_tokens=500,
)

response_text = completion.choices[0].message.content

# Split into story and image prompt
lines = response_text.split("ImagePrompt:")
story = lines[0].replace("Story:", "").strip()
image_prompt = lines[1].strip() if len(lines) > 1 else "A cartoon of a cat and a dragon."

print("Story:\n", story)
print("\nImage Prompt:\n", image_prompt)

# Image generation (use DALL·E 3 if you have access)
response = client.images.generate(
    model="dall-e-2",
    prompt=image_prompt,
    size="512x512",
)

image_url = response.data[0].url
print("\nImage URL:\n", image_url)
