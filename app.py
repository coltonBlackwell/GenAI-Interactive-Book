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
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Create fun children's stories with an Introduction, Problem, Solution, and a Happy ending (However never explicitly saying this!). Also provide a Story Title at the beginning. Then provide an image prompt in format: Story: <text>\nImagePrompt: <description>"
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
        
        if "ImagePrompt:" in response_text:
            story, image_prompt = response_text.split("ImagePrompt:", 1)
            story = story.replace("Story:", "").strip()
            image_prompt = image_prompt.strip()
        else:
            story = response_text.strip()
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
            model="dall-e-2",
            prompt=f"Children's book illustration of {image_prompt}. Colorful, cartoon style, happy mood.",
            size="512x512",
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