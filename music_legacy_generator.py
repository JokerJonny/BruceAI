#!/usr/bin/env python3
"""
music_legacy_generator.py
Part of BruceAI / NeoLegacy ecosystem
Generates Suno prompts, calls music API, creates visualizer videos,
and stores outputs in legacy vault — all while staying aligned with
conscience, truth, and human values.

Requires:
- Ollama running locally with 'persona' model loaded
- FFmpeg installed (sudo apt install ffmpeg)
- Optional: third-party Suno API key (TTAPI.io, SunoAPI.org, etc.)
"""

import os
import subprocess
import requests
from datetime import datetime
from langchain_community.llms import Ollama

# ────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────

OLLAMA_MODEL = "persona"                # Your custom neoSHADE-tuned Mistral model
LEGACY_VAULT_PATH = "./legacy_vault"    # Change to your preferred storage path
DEFAULT_BACKGROUND = "album_art.jpg"    # Default image for visualizers

# Suno API config (replace with your provider)
SUNO_API_URL = "https://api.ttapi.io/suno/v1/music"  # example endpoint
SUNO_API_KEY = "YOUR_API_KEY_HERE"                   # fill this

# ────────────────────────────────────────────────
# LLM Prompt Generator
# ────────────────────────────────────────────────

llm = Ollama(model=OLLAMA_MODEL)

def generate_suno_prompt(user_input: str) -> str:
    """
    Create a high-quality, Suno-ready prompt using your neoSHADE style.
    """
    query = f"""
You are neoSHADE — a values-aligned music creator.
Generate a complete Suno prompt for the following request:
{user_input}

Rules:
- Style: neoSHADE — positive, transparent, motivational, real-life arcs
- Draw from Jung (shadow integration), Peterson (responsibility, meaning), Greek thinkers (virtue, logos)
- Include: full lyrics snippet (8–16 lines), genre/mode (reggae, rock, jazz, acoustic, cinematic, hip-hop, etc.), tempo/BPM, mood/vibe, frequency hints, instrumentation ideas
- Keep lyrics positive, resilient, truthful — no nihilism or despair
- Suggest 1–2 visualizer concepts for video (e.g., cosmic waves, family photos, symbolic shadows)
- Format output for direct copy-paste into Suno (clear sections: [Lyrics], [Style], [Video Ideas])
"""
    return llm(query).strip()


# ────────────────────────────────────────────────
# Suno Music Generation (online)
# ────────────────────────────────────────────────

def call_suno_api(prompt: str, timeout=120) -> str | None:
    """
    Call third-party Suno API to generate music.
    Returns path to downloaded MP3 or None on failure.
    """
    if not SUNO_API_KEY or SUNO_API_KEY == "YOUR_API_KEY_HERE":
        print("Warning: Suno API key not set. Skipping generation.")
        return None

    payload = {
        "prompt": prompt,
        "mv": "chirp-v4-5+",           # or latest model
        "custom": True,
        "tags": "neoSHADE, legacy, motivational"
    }

    headers = {"Authorization": f"Bearer {SUNO_API_KEY}"}

    try:
        response = requests.post(SUNO_API_URL, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        audio_url = data.get("audio_url") or data.get("url")
        if not audio_url:
            print("Error: No audio URL returned.")
            return None

        filename = f"legacy_track_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        filepath = os.path.join(LEGACY_VAULT_PATH, filename)

        with open(filepath, "wb") as f:
            f.write(requests.get(audio_url).content)

        print(f"Music generated and saved: {filepath}")
        return filepath

    except Exception as e:
        print(f"Suno API error: {e}")
        return None


# ────────────────────────────────────────────────
# Simple Video Visualizer (offline)
# ────────────────────────────────────────────────

def create_visualizer(audio_path: str, background_image: str = DEFAULT_BACKGROUND, lyrics_text: str = "", output_name: str = None) -> str:
    """
    Create a basic MP4 visualizer: static image + audio + optional lyrics overlay.
    Requires FFmpeg.
    """
    if not os.path.isfile(audio_path):
        print(f"Audio file not found: {audio_path}")
        return None

    if output_name is None:
        base = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = os.path.join(LEGACY_VAULT_PATH, f"{base}_visualizer.mp4")
    else:
        output_path = os.path.join(LEGACY_VAULT_PATH, output_name)

    # Build FFmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", background_image,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest"
    ]

    # Add lyrics overlay if provided
    if lyrics_text:
        # Escape single quotes in lyrics
        safe_lyrics = lyrics_text.replace("'", "'\\''")
        vf = f"drawtext=text='{safe_lyrics}':fontcolor=white:fontsize=28:x=(w-tw)/2:y=h-th-40:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        cmd.extend(["-vf", vf])

    cmd.append(output_path)

    try:
        subprocess.run(cmd, check=True)
        print(f"Visualizer created: {output_path}")
        return output_path
    except Exception as e:
        print(f"FFmpeg error: {e}")
        return None


# ────────────────────────────────────────────────
# Main Legacy Workflow
# ────────────────────────────────────────────────

def generate_legacy_track(user_input: str, background_image: str = DEFAULT_BACKGROUND):
    """
    Full pipeline: prompt → music → video → vault
    """
    # 1. Ensure vault exists
    os.makedirs(LEGACY_VAULT_PATH, exist_ok=True)

    # 2. Generate optimized Suno prompt (offline)
    print("Generating Suno prompt...")
    prompt = generate_suno_prompt(user_input)
    print("\n=== Generated Suno Prompt ===\n")
    print(prompt)
    print("\n" + "="*60 + "\n")

    # 3. Generate music (online)
    print("Calling Suno API...")
    audio_path = call_suno_api(prompt)

    if audio_path:
        # 4. Create visualizer (offline)
        print("Creating visualizer...")
        video_path = create_visualizer(audio_path, background_image=background_image)

        # 5. Optional: add metadata / log to vault
        log_path = os.path.join(LEGACY_VAULT_PATH, "generation_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now()}] Generated from: {user_input}\n")
            f.write(f"Prompt:\n{prompt}\n")
            f.write(f"Audio: {audio_path}\n")
            if video_path:
                f.write(f"Video: {video_path}\n")
            f.write("-"*80 + "\n")

        print("\nLegacy track generation complete.")
        print(f"Audio: {audio_path}")
        if video_path:
            print(f"Video: {video_path}")

    else:
        print("Music generation skipped or failed. You can copy-paste the prompt into Suno manually.")


# ────────────────────────────────────────────────
# Example Usage
# ────────────────────────────────────────────────

if __name__ == "__main__":
    # Example legacy household prompt
    example_input = (
        "Create a motivational jazz-slow jam about a family overcoming generational trauma, "
        "with a Jungian shadow integration arc, positive resolution, real-life resilience story, "
        "and warm, healing frequency."
    )

    generate_legacy_track(
        user_input=example_input,
        background_image="family_tree_art.jpg"  # replace with your image
    )
