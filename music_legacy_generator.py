#!/usr/bin/env python3
"""
music_legacy_generator.py
BruceAI / NeoLegacy Music Creation Tool
Generates Suno-optimized prompts offline (via Ollama persona model),
optionally calls Suno API for music, creates simple visualizer videos (FFmpeg),
and archives everything securely in the legacy vault.

Purpose: Help legacy households create meaningful, values-aligned music tracks
from personal stories, arcs, and themes — preserving truth, resilience, and love.

Requirements:
- Ollama running locally with 'persona' model (neoSHADE-tuned Mistral)
- FFmpeg installed (sudo apt install ffmpeg)
- Optional: Suno API key (TTAPI.io, SunoAPI.org, AIMLAPI.com, etc.)

License: Same as BruceAI — non-commercial, conscience-aligned use only.
"""

import os
import subprocess
import requests
from datetime import datetime
from langchain_community.llms import Ollama

# ────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────

OLLAMA_MODEL = "persona"                        # Your custom neoSHADE Mistral model
LEGACY_VAULT_PATH = "./legacy_vault"            # Where generated files are stored
DEFAULT_BACKGROUND_IMAGE = "album_art.jpg"      # Fallback image for visualizers

# Suno API (third-party provider — replace with your choice)
SUNO_API_URL = "https://api.ttapi.io/suno/v1/music"   # Example endpoint
SUNO_API_KEY = "YOUR_SUNO_API_KEY_HERE"               # ← FILL THIS IN

# ────────────────────────────────────────────────
# LLM Prompt Generator (fully offline)
# ────────────────────────────────────────────────

llm = Ollama(model=OLLAMA_MODEL)

def generate_suno_prompt(user_input: str) -> str:
    """
    Creates a high-quality Suno prompt aligned with neoSHADE values.
    """
    query = f"""
You are neoSHADE — a values-aligned music creator.
Generate a complete, ready-to-use Suno prompt based on this request:
{user_input}

Core rules:
- Style & tone: positive, transparent, motivational, real-life emotional arcs
- Influences: Carl Jung (shadow integration, individuation), Jordan Peterson (responsibility, meaning), Greek thinkers (virtue, logos, courage)
- Lyrics: 8–16 meaningful lines — resilient, truthful, uplifting, no despair/nihilism
- Structure: Include full lyrics snippet + genre/mode (reggae, rock, slow jam, jazz, acoustic, cinematic, hip-hop, etc.) + tempo/BPM range + mood/vibe + frequency hints + instrumentation ideas
- Video ideas: Suggest 1–2 simple visualizer concepts (e.g., cosmic waves, symbolic shadows, family photos, ocean at dusk)
- Format clearly for direct copy-paste into Suno:
  [Lyrics]
  [Style & Parameters]
  [Video Concepts]

Keep everything aligned with truth, love, legacy, and human conscience.
"""
    response = llm(query).strip()
    return response


# ────────────────────────────────────────────────
# Suno Music Generation (online — optional)
# ────────────────────────────────────────────────

def call_suno_api(prompt: str, timeout=180) -> str | None:
    """
    Calls third-party Suno API to generate audio.
    Returns path to saved MP3 or None if skipped/failed.
    """
    if SUNO_API_KEY == "YOUR_SUNO_API_KEY_HERE" or not SUNO_API_KEY:
        print("Suno API key not configured. Skipping music generation.")
        print("You can copy-paste the generated prompt into Suno manually.")
        return None

    payload = {
        "prompt": prompt,
        "mv": "chirp-v4-5+",           # Use latest high-quality model
        "custom": True,
        "tags": "neoSHADE, legacy, motivational, values-aligned"
    }

    headers = {"Authorization": f"Bearer {SUNO_API_KEY}"}

    try:
        print("Sending request to Suno API...")
        response = requests.post(SUNO_API_URL, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        audio_url = data.get("audio_url") or data.get("url") or data.get("download_url")
        if not audio_url:
            print("Error: No audio URL in response.")
            return None

        filename = f"legacy_track_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        filepath = os.path.join(LEGACY_VAULT_PATH, filename)

        print(f"Downloading audio from: {audio_url}")
        audio_data = requests.get(audio_url).content
        with open(filepath, "wb") as f:
            f.write(audio_data)

        print(f"Music saved: {filepath}")
        return filepath

    except Exception as e:
        print(f"Suno API error: {str(e)}")
        return None


# ────────────────────────────────────────────────
# Simple Video Visualizer (fully offline)
# ────────────────────────────────────────────────

def create_visualizer(audio_path: str, background_image: str = DEFAULT_BACKGROUND_IMAGE, lyrics_text: str = "", output_name: str = None) -> str | None:
    """
    Creates a basic MP4 visualizer: static background + audio + optional lyrics overlay.
    Requires FFmpeg installed.
    """
    if not os.path.isfile(audio_path):
        print(f"Audio file not found: {audio_path}")
        return None

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if output_name:
        output_path = os.path.join(LEGACY_VAULT_PATH, output_name)
    else:
        base = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = os.path.join(LEGACY_VAULT_PATH, f"{base}_visualizer_{timestamp}.mp4")

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", background_image,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage", "-preset", "slow",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest"
    ]

    if lyrics_text:
        safe_lyrics = lyrics_text.replace("'", "'\\''").replace('"', '\\"')
        vf = f"drawtext=text='{safe_lyrics}':fontcolor=white:fontsize=28:borderw=2:x=(w-tw)/2:y=h-th-60:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        cmd.extend(["-vf", vf])

    cmd.append(output_path)

    try:
        print("Running FFmpeg to create visualizer...")
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Visualizer saved: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e.stderr.decode()}")
        return None
    except Exception as e:
        print(f"Error creating video: {e}")
        return None


# ────────────────────────────────────────────────
# Archive & Logging
# ────────────────────────────────────────────────

def log_generation(user_input: str, prompt: str, audio_path: str | None, video_path: str | None):
    log_file = os.path.join(LEGACY_VAULT_PATH, "generation_log.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    entry = f"""
[{timestamp}]
Input: {user_input}
Prompt:\n{prompt}
Audio: {audio_path or 'Skipped'}
Video: {video_path or 'Skipped'}
{'─'*80}
"""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)


# ────────────────────────────────────────────────
# Main Workflow
# ────────────────────────────────────────────────

def generate_legacy_track(user_input: str, background_image: str = DEFAULT_BACKGROUND_IMAGE):
    """
    Full pipeline: prompt → music (optional) → visualizer → vault
    """
    os.makedirs(LEGACY_VAULT_PATH, exist_ok=True)

    print("\nGenerating Suno prompt (offline)...")
    prompt = generate_suno_prompt(user_input)
    print("\n" + "═"*60)
    print("Generated Suno Prompt:")
    print(prompt)
    print("═"*60 + "\n")

    audio_path = None
    print("Attempting Suno music generation (online)...")
    audio_path = call_suno_api(prompt)

    video_path = None
    if audio_path:
        print("\nCreating visualizer video (offline)...")
        # Extract short lyrics snippet from prompt for overlay (simple heuristic)
        lyrics_snippet = prompt.split("[Lyrics]")[1].split("[Style]")[0].strip()[:200] + "..." if "[Lyrics]" in prompt else ""
        video_path = create_visualizer(audio_path, background_image, lyrics_text=lyrics_snippet)

    # Log everything
    log_generation(user_input, prompt, audio_path, video_path)

    print("\n" + "═"*60)
    print("Generation complete.")
    if audio_path:
        print(f"Audio: {audio_path}")
    if video_path:
        print(f"Video: {video_path}")
    print("Files archived in:", LEGACY_VAULT_PATH)
    print("═"*60)


# ────────────────────────────────────────────────
# CLI Interface
# ────────────────────────────────────────────────

if __name__ == "__main__":
    print("═"*70)
    print("neoSHADE Legacy Music Generator – BruceAI Powered")
    print("Create values-aligned tracks for family legacy & personal arcs")
    print("Type your idea below (or 'quit'/'q' to exit)")
    print("═"*70 + "\n")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ['quit', 'q', 'exit', '']:
            print("\nSession ended. Files saved in legacy_vault/")
            break
        
        if user_input:
            generate_legacy_track(user_input)
        else:
            print("Please enter a music idea (e.g., 'reggae track on overcoming loss with hope').")
