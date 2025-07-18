#!/bin/bash

# MindGarden Screen Recording with Proper Audio Capture
# Uses BlackHole for system audio + built-in microphone

echo "🎮 MindGarden Recording - Enhanced Audio Setup"
echo "=============================================="
echo ""
echo "📺 Starting screen recording with enhanced audio..."
echo "🎵 Capturing: System audio via BlackHole"
echo "🎤 Capturing: Built-in microphone"
echo "🎮 Key press indicators: VISIBLE"

# Generate timestamp for unique filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="mindgarden_audio_fixed_${TIMESTAMP}.mp4"

echo "📁 Output file: $OUTPUT_FILE"
echo ""
echo "⚠️  Make sure to:"
echo "   1. Set system audio output to BlackHole 2ch"
echo "   2. Adjust microphone levels if needed"
echo ""
echo "Press Ctrl+C to stop recording"
echo ""

# Screen recording with BlackHole for system audio + microphone
# Device 1 = Screen capture
# Device 0 = BlackHole 2ch (system audio)
# Device 1 = MacBook Pro Microphone
ffmpeg \
  -f avfoundation \
  -capture_cursor 1 \
  -capture_mouse_clicks 1 \
  -r 30 \
  -i "1" \
  -f avfoundation \
  -i ":0" \
  -f avfoundation \
  -i ":1" \
  -filter_complex "[1:a][2:a]amix=inputs=2:duration=longest:dropout_transition=0:weights=1.0 0.6[audio_out]" \
  -map 0:v \
  -map "[audio_out]" \
  -c:v libx264 \
  -preset medium \
  -crf 18 \
  -pix_fmt yuv420p \
  -c:a aac \
  -b:a 256k \
  -ar 48000 \
  -ac 2 \
  -shortest \
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
