import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        items = data.get("items", ["cat"])
        
        if not items:
            items = ["cat"]
        
        # Generate story with GPT-3.5-turbo
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Create a fun children's story with the following structure but WITHOUT section headers:
                    1. Begin with a title (plain text, no asterisks or formatting)
                    2. A natural introduction
                    3. A problem that arises
                    4. How it gets solved
                    5. A happy ending
                    
                    Write in one cohesive narrative flow without labeling sections.
                    Then provide an image prompt in format: Story: <text>\nImagePrompt: <description>"""
                },
                {
                    "role": "user",
                    "content": f"Create a story about: {', '.join(items)}"
                }
            ],
            max_tokens=500,
            temperature=0.7
        )

        response_text = completion.choices[0].message.content
        
        # Clean up the story text
        if "ImagePrompt:" in response_text:
            story, image_prompt = response_text.split("ImagePrompt:", 1)
            story = story.replace("Story:", "").strip()
            
            # Remove any remaining markdown formatting
            story = story.replace("**", "")
            
            # Ensure title is clean (remove any special formatting)
            if "\n" in story:
                first_line = story.split("\n")[0]
                story = first_line + "\n\n" + "\n".join(story.split("\n")[1:])
            
            image_prompt = image_prompt.strip()
        else:
            story = response_text.strip().replace("**", "")
            image_prompt = f"A colorful cartoon of {', '.join(items)} playing together"
        
        # Generate TTS audio
        audio_response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=story[:4096]
        )

        audio_path = "static/story.mp3"
        with open(audio_path, "wb") as f:
            f.write(audio_response.content)

        # Generate image with DALL-E 2
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"Children's book illustration of {image_prompt}. Colorful, cartoon style, happy mood.",
            size="1024x1024",
            quality="standard",
            n=1
        )

        return jsonify({
            "story": story,
            "image_url": image_response.data[0].url,
            "audio_url": f"/{audio_path}"
        })

    except Exception as e:
        print(f"Error generating story: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)