import subprocess  # For FFmpeg
from langchain_community.llms import Ollama  # Offline LLM
import requests  # For Suno API (online)

# Your custom Mistral persona
llm = Ollama(model="persona")  # Assumes running on Pi

def generate_suno_prompt(user_input):
    query = f"Generate Suno prompt for music: {user_input}. Style: neoSHADE - positive, Jung/Peterson arcs, real stories. Include lyrics snippet, genre (reggae/rock/jazz/etc.), tempo, mood. Suggest video concepts."
    return llm(query)

def call_suno_api(prompt):
    api_key = "YOUR_TTAPI_OR_SUNOAPI_KEY"  # Get from provider
    url = "https://api.ttapi.io/suno/v1/music"  # Example from TTAPI
    payload = {
        "prompt": prompt,
        "mv": "chirp-v4-5+",  # Model
        "custom": True  # Use lyrics if in prompt
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        audio_url = response.json().get("audio_url")  # Download MP3
        with open("output.mp3", "wb") as f:
            f.write(requests.get(audio_url).content)
        return "output.mp3"
    else:
        return None

def create_video(audio_file, image_path="background.jpg", lyrics="Sample lyrics"):  # Use your album art
    # Simple FFmpeg: Audio + static image + lyrics overlay
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", image_path, 
        "-i", audio_file, "-vf", f"drawtext=text='{lyrics}':fontcolor=white:fontsize=24:x=(w-tw)/2:y=h-60",
        "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "output.mp4"
    ]
    subprocess.run(cmd)
    return "output.mp4"

# Example Usage for Legacy Household
user_input = "Create music on family resilience, real story arc about overcoming loss."
prompt = generate_suno_prompt(user_input)
print("Generated Prompt:", prompt)

audio = call_suno_api(prompt)
if audio:
    video = create_video(audio, image_path="album_art.jpg", lyrics="Excerpt from lyrics...")
    print("Generated Music/Video:", video)
    # Store in vault: Move to /path/to/legacy_folder

# Run: python3 music_legacy_generator.py
