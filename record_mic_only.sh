#!/bin/bash

# MindGarden Screen Recording - Microphone Only
# Simple recording with just microphone audio

echo "🎮 MindGarden Recording - Microphone Audio"
echo "=========================================="
echo ""
echo "📺 Starting screen recording..."
echo "🎤 Capturing: Microphone only"
echo "🎮 Key press indicators: VISIBLE"

# Generate timestamp for unique filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="mindgarden_mic_only_${TIMESTAMP}.mp4"

echo "📁 Output file: $OUTPUT_FILE"
echo ""
echo "Press Ctrl+C to stop recording"
echo ""

# Screen recording with microphone only
ffmpeg \
  -f avfoundation \
  -capture_cursor 1 \
  -capture_mouse_clicks 1 \
  -r 30 \
  -i "1:1" \
  -c:v libx264 \
  -preset medium \
  -crf 18 \
  -pix_fmt yuv420p \
  -c:a aac \
  -b:a 192k \
  -ar 48000 \
  -ac 2 \
  "$OUTPUT_FILE"

echo ""
echo "🎬 Recording completed!"
echo "📁 File saved as: $OUTPUT_FILE"

# Check if file was created and show size
if [ -f "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
    echo "📊 File size: $FILE_SIZE"
    
    # Check audio levels
    echo "🔊 Checking audio levels..."
    ffmpeg -i "$OUTPUT_FILE" -af "volumedetect" -f null - 2>&1 | grep -E "(mean_volume|max_volume)"
else
    echo "❌ Recording file not found!"
fi
