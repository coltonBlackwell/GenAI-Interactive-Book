# AI Storytime Generator 🧸

A web app that generates children's stories using AI, featuring colorful illustrations and audio narration.

## Features

- 🎨 **Interactive Story Creation**: Combine animals and objects to generate unique stories
- 🖼️ **AI-Generated Illustrations**: Colorful images accompany each story
- 🔊 **Audio Narration**: Stories are read aloud with text-to-speech
- 🎮 **Child-Friendly Interface**: Large buttons, playful design, and fun animations

## How It Works

1. Select 1 or more animals/characters
2. Select 1 or more objects
3. Click "Create My Story"
4. Enjoy your custom story with image and audio!

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python with Flask
- **AI Services**: OpenAI (GPT-4o-mini for stories, DALL-E 3 for images, TTS for audio)
- **Styling**: Custom playful CSS with animations

## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key
- Flask

### File Structure

ai-storytime-generator/\
├── static/\
│   ├── styles.css\
│   └── story.mp3 (generated)\
├── templates/\
│   └── index.html\
├── app.py\
├── requirements.txt\
└── README.md

### Example Story prompts
Try these fun combinations:

- 🦁 Lion + 🧸 Teddy Bear
- 🦒 Giraffe + 🚲 Bicycle
- 🐧 Penguin + 🏮 Lantern
