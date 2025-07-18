# NeuroNest 🌱

A relaxing interactive mindfulness application that helps you grow a virtual tree through calm interactions. The tree grows when you're relaxed and shrinks when you're stressed, encouraging mindful breathing and relaxation.

## Features

- **Interactive Tree Growth**: Watch your tree grow as you practice mindfulness
- **Three Game Modes**:
  - 🌳 **Static Tree**: Classic tree that grows with calm interactions
  - 🎞️ **Animated Tree**: Beautiful animated tree sequence
  - 💖 **Health Bar Mode**: Track your wellness with a health indicator
- **Relaxing Audio**: Soothing background music and water sounds
- **Visual Effects**: Falling leaves and water drop animations

## Installation

1. **Clone or download** this repository
2. **Navigate** to the project directory:
   ```bash
   cd NeuroNest
   ```
3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
```bash
python mindgarden.py
```

### Controls
- **[C]** - Calm mode (helps tree grow)
- **[B]** - Blink/Water tree (moderate use helps growth, excessive use causes stress)
- **[R]** - Reset the current session
- **[1, 2, 3]** - Switch between game modes
- **[ESC]** - Quit the application

### Game Modes
1. **Static Tree Mode**: Tree grows in size and changes the sky color
2. **Animated Tree Mode**: Beautiful frame-by-frame tree animation
3. **Health Bar Mode**: Animated tree with a health indicator

## Utility Scripts

### Extract Frames from GIF
```bash
python extract_frames.py [gif_file_path] [output_directory]
```
Example:
```bash
python extract_frames.py my_animation.gif frames
```

### Remove Background from Frames
```bash
python remove_gif_background.py
```
This will process all PNG files in the `frames/` directory and make their backgrounds transparent.

## Assets Required

The application expects these files in the project directory:
- `tree_small.png` - Small tree sprite
- `tree_medium.png` - Medium tree sprite  
- `tree_large.png` - Large tree sprite
- `calm.mp3` - Background music (optional)
- `water.wav` - Water sound effect (optional)
- `frames/` directory with numbered frame files (frame_000.png, frame_001.png, etc.)

## Tips for Relaxation

- Use **[C]** frequently for steady growth - start small and watch it grow!
- Use **[B]** sparingly - it represents controlled breathing
- Avoid rapid or excessive **[B]** presses as this simulates stress
- The tree starts small to encourage mindful growth through relaxation
- Watch the tree grow as you practice mindful breathing
- Enjoy the relaxing background music and visual effects

## Troubleshooting

- **Missing dependencies**: Run `pip install -r requirements.txt`
- **Missing assets**: Ensure all image and audio files are in the project directory
- **No sound**: Check that your system audio is enabled and files `calm.mp3` and `water.wav` exist

## Contributing

Feel free to contribute by:
- Adding new tree sprites or animations
- Improving the relaxation mechanics
- Adding new visual effects
- Enhancing the audio experience

## License

This project is open source. Feel free to use, modify, and distribute as needed.

