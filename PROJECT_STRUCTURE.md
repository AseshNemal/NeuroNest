# 📁 NeuroNest Project Structure

## 🎯 Clean Folder Organization

```
NeuroNest/
├── 🎮 neuronest.py           # Main application entry point
├── 📖 README.md              # Project overview and quick start
├── 📦 requirements.txt       # Python dependencies
├── � LICENSE                # MIT License
├── 📁 PROJECT_STRUCTURE.md   # Detailed structure guide
├── �📚 docs/                  # Documentation
│   ├── TECHNICAL_DOCUMENTATION.md
│   └── PROBLEMS_ANALYSIS.md
├── 🎨 assets/                # Media files
│   ├── 🎵 calm.mp3          # Background music
│   ├── 🌊 water.wav         # Water sound effects
│   ├── 🌳 tree_small.png    # Tree stage 1
│   ├── 🌲 tree_medium.png   # Tree stage 2
│   ├── 🌴 tree_large.png    # Tree stage 3
│   └── 🎬 frames/           # Animation frames (99 files)
│       ├── frame_000.png
│       ├── frame_001.png
│       └── ... (frame_002.png to frame_098.png)
└── 🔧 scripts/              # Utilities and recording tools
    ├── 🎙️ record_system_audio.sh
    ├── 🎧 record_with_blackhole.sh
    ├── 🎤 record_mic_only.sh
    ├── 🎬 extract_frames.py
    ├── 🖼️ remove_gif_background.py
    ├── 📏 test_scaling.py
    └── ⚙️ test_setup.py
```

## 📊 File Count Summary

- **Main Application**: 1 file (`neuronest.py`)
- **Documentation**: 3 files (README.md + 2 in docs/)
- **Assets**: 6 files + 99 animation frames = 105 files
- **Scripts**: 7 utility files
- **Configuration**: 1 file (`requirements.txt`)
- **License**: 1 file (`LICENSE`)

**Total Project Files**: ~118 files (excluding .venv and .git)

## 🎯 Folder Purpose

### **Root Directory**
- Contains only essential files: main app, README, requirements
- Clean and minimal for easy navigation

### **assets/ 🎨**
- All media files (images, audio, animations)
- Organized by type and purpose
- Referenced by main application

### **scripts/ 🔧**
- Recording tools and utilities
- Development and testing scripts
- Audio processing tools

### **docs/ 📚**
- Technical documentation
- Problem analysis and solutions
- Architecture and setup guides

## ✅ Organization Benefits

1. **Clear Separation**: Each folder has a specific purpose
2. **Easy Navigation**: Find files quickly by category
3. **Maintainable**: Easy to add new files in appropriate locations
4. **Professional**: Clean structure for development and collaboration
5. **Scalable**: Ready for future expansion

## 🚀 Quick Start

```bash
# Run the application
python neuronest.py

# Use recording scripts
./scripts/record_system_audio.sh

# View documentation
open docs/TECHNICAL_DOCUMENTATION.md
```

---
*Generated: July 18, 2025*
