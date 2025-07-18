#!/bin/bash

# MindGarden System Audio Recording Script
# This script captures screen + system audio using BlackHole routing

# Configuration
OUTPUT_FILE="mindgarden_system_audio_$(date +%Y%m%d_%H%M%S).mp4"

echo "🎮 MindGarden Recording - System Audio Only"
echo "========================================"
echo ""
echo "📺 Starting screen recording with system audio..."
echo "🎵 Capturing: Background music + Water sounds + Game audio"
echo "🎤 No microphone input"
echo "🎮 Key press indicators: VISIBLE"
echo "📁 Output file: $OUTPUT_FILE"
echo ""
echo "Press Ctrl+C to stop recording"
echo ""

# Start recording with BlackHole for system audio
ffmpeg \
    -f avfoundation \
    -i "1:BlackHole 2ch" \
    -vcodec libx264 \
    -preset fast \
    -crf 18 \
    -pix_fmt yuv420p \
    -acodec aac \
    -ar 48000 \
    -ac 2 \
    -ab 192k \
    -r 30 \
    "$OUTPUT_FILE"

echo ""
echo "🎬 Recording completed!"
echo "📁 File saved as: $OUTPUT_FILE"
echo "📊 File size: $(du -h "$OUTPUT_FILE" | cut -f1)"
