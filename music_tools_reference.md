# Music Legacy Tools Reference – BruceAI / NeoLegacy

**Central guide for all music-related tools in this repository**  
Last updated: February 2026  
Purpose: Quick access, reminders, examples, troubleshooting, and future expansion notes for creating values-aligned music tracks for personal and family legacy preservation.

## Overview
This repo contains tools to generate music and visualizers in the neoSHADE style — positive, transparent, motivational, real-life emotional arcs, drawing from Jung (shadow integration), Peterson (responsibility/meaning), Greek virtue, and your own life stories.

Main file: `music_legacy_generator.py`  
Purpose:  
- Offline prompt generation using your neoSHADE-tuned Mistral persona (Ollama)  
- Optional call to third-party Suno API for audio generation  
- Simple visualizer video creation (FFmpeg: static image + audio + lyrics overlay)  
- Automatic archiving in `./legacy_vault/` for long-term family/heirloom storage

All outputs remain under your full ownership and the BruceAI Custom License — non-commercial, conscience-aligned use only.

## Quick Start – How to Run

1. Pull the latest repo
   ```bash
   git pull origin main

Install dependencies (do this once)Bashpip install -r requirements.txt
Make sure Ollama is running with your persona modelBashollama run persona
Install FFmpeg (required for video creation)Bashsudo apt update
sudo apt install ffmpeg
(Optional) Create .env from .env.example and add your Suno API keytextSUNO_API_KEY=sk-your-real-key-here
SUNO_API_URL=https://api.ttapi.io/suno/v1/music
Run the toolBashpython3 music_legacy_generator.py
At the prompt (>), type your music idea — or type 'quit' to exit

Example inputs (copy-paste ready):

"slow reggae-soul track on overcoming generational trauma, positive Jungian shadow integration arc, real-life resilience story, warm healing frequencies, 80–90 BPM, acoustic guitar and soft horns"
"motivational acoustic ballad on standing alone with quiet strength, Peterson responsibility theme, 70–80 BPM, fingerstyle guitar and light strings"
"cinematic jazz-slow jam on cosmic alignment and becoming whole, real-life arc of self-discovery, 60–75 BPM, upright bass, soft piano, atmospheric pads"
"uplifting hip-hop with spoken-word bridge about leaving a legacy of truth and love, real family story, positive frequency, 90–100 BPM, boom-bap drums, soulful sample"

What happens:

Generates a detailed Suno prompt (offline)
(If API key set) Calls Suno to create audio → saves MP3
Creates MP4 visualizer (image + audio + optional lyrics overlay)
Logs everything in legacy_vault/generation_log.txt

Requirements & Setup Checklist
Python dependencies (requirements.txt)
textollama>=0.3.0
langchain-community>=0.2.0
requests>=2.31.0
python-dotenv>=1.0.0
System dependencies

Ollama — install and run ollama pull mistral
Create custom persona model (Modelfile example below)
FFmpeg — sudo apt install ffmpeg

.env file (copy from .env.example — never commit!)
textSUNO_API_KEY=sk-your-real-key-here
SUNO_API_URL=https://api.ttapi.io/suno/v1/music   # or your provider
Modelfile example (for Ollama – create once)
textFROM mistral
SYSTEM """
You are neoSHADE — a values-aligned music creator.
Respond positively, transparently, motivationally.
Draw from Jung (shadow integration), Peterson (responsibility, meaning), Greek thinkers (virtue, logos).
Focus on real-life arcs, resilience, love, legacy.
Generate Suno prompts with lyrics, genre, tempo, mood, instrumentation.
Keep everything uplifting — no nihilism or despair.
"""
PARAMETER temperature 0.7
Create it:
Bashollama create persona -f Modelfile
Troubleshooting Quick Fixes
Ollama not responding

Run in separate terminal: ollama serve
Then: ollama run persona
Check model exists: ollama list

FFmpeg command fails

Reinstall: sudo apt install --reinstall ffmpeg
Verify: ffmpeg -version

Suno API error

Check key in .env
Test endpoint in browser/Postman
Try different provider (TTAPI.io, SunoAPI.org, AIMLAPI.com)
Fallback: copy prompt manually into Suno web

No vault folder

Script creates ./legacy_vault/ automatically

Slow on Raspberry Pi

Use smaller quantized model: ollama pull mistral:7b-instruct-q4_0
Reduce temperature or prompt length

Future Expansion Ideas (Roadmap)

RAG Integration
Index your 1400+ lyrics backup folder → prompts pull from existing work
(Add ChromaDB + OllamaEmbeddings)
Batch Album Mode
Input file with 8–12 track titles/themes → generate full arc
(Add loop over CSV/JSON)
Alexa Voice Trigger
"Alexa, ask Bruce to make a legacy song about courage"
(Flask API on Pi + Alexa Skill)
Local Image Generation
Stable Diffusion on Pi for custom backgrounds
(Replace static album_art.jpg)
Vault Security
Encrypt vault folder (LUKS)
Auto-backup to USB/external drive
Export for family hand-down
Metadata & Tagging
Add ID3 tags to MP3s (title, artist=neoSHADE, comment=legacy arc)
Multi-Model Support
Toggle between Mistral, Llama3, Gemma via Ollama

All future additions must remain under BruceAI Custom License — non-commercial, no AI training, conscience-aligned only.
Final Reminder
This tool exists to help create music that carries truth, love, resilience, and legacy — never for exploitation or scale.
Use it responsibly. Honor the purpose.
© 2025–2026 Jonathan M. George (JokerJonny / NeoShade AI)
All rights reserved under BruceAI Custom License.
