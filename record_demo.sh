#!/bin/bash

# Screen recording script for MindGarden demo
echo "Starting MindGarden Screen Recording Demo"
echo "Recording will start in 5 seconds..."
echo "Press Ctrl+C to stop recording"

# Wait 5 seconds
sleep 5

# Get screen dimensions (macOS)
SCREEN_SIZE=$(system_profiler SPDisplaysDataType | grep Resolution | head -1 | awk '{print $2"x"$4}')

# Record screen with audio
ffmpeg -f avfoundation -i "1:0" -r 30 -s $SCREEN_SIZE -c:v libx264 -preset ultrafast -c:a aac mindgarden_demo_$(date +%Y%m%d_%H%M%S).mp4

echo "Recording saved as mindgarden_demo_$(date +%Y%m%d_%H%M%S).mp4"
