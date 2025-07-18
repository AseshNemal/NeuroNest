# 🧠 NeuroNest

**Brain-Computer Interface Relaxation Applicat├├── 📁 PROJECT_STRUCTURE.md   # Detailed structure guide─ 📄 LICENS## 💻 Development Workflow      ## 🔧 System Requirements         # MIT Licenseon**

A neurofeedback therapy and mindfulness training application that creates relaxing, interactive experiences responding to your mental state through## 📄 License

**MIT License** - Free for personal and commercial use

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### **License Summary:**
- ✅ **Commercial use** - Use in commercial projects
- ✅ **Modification** - Change and adapt the code
- ✅ **Distribution** - Share with others
- ✅ **Private use** - Use for personal projects
- ⚠️ **Liability** - No warranty provided
- ⚠️ **License notice** - Must include license in derivativessual and audio feedback.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install pygame

# 2. Run the application
python neuronest.py
```

## 🎮 How to Use

### **Controls:**
- **[1, 2, 3]** - Select experience mode
- **[C]** - Calm state (grow your tree)
- **[B]** - Blink/interaction (water effects)
- **[R]** - Reset session
- **[ESC]** - Exit

### **Experience Modes:**
1. **Static Tree Evolution** - Watch your tree grow through mindful breathing
2. **Animated Meditation** - Interactive animation responds to your calm state  
3. **Health & Wellness** - Track your relaxation progress with health metrics

## 🎥 Recording Your Sessions

### **System Audio Recording:**
```bash
# Record with full game audio
./scripts/record_system_audio.sh
```

### **Setup for macOS:**
1. Install BlackHole: `brew install --cask blackhole-2ch`
2. Set BlackHole 2ch as system audio output
3. Run recording script

## 📁 Project Structure

```
NeuroNest/
├── 🎮 neuronest.py           # Main application entry point
├── 📖 README.md              # Project overview and quick start
├── 📦 requirements.txt       # Python dependencies
├── � LICENSE                # MIT License
├── �📁 PROJECT_STRUCTURE.md   # Detailed structure guide
├── 🎨 assets/                # Media files
│   ├── 🎵 calm.mp3          # Background ambient music
│   ├── 🌊 water.wav         # Water sound effects
│   ├── 🌳 tree_small.png    # Tree growth stage 1
│   ├── 🌲 tree_medium.png   # Tree growth stage 2
│   ├── 🌴 tree_large.png    # Tree growth stage 3
│   └── 🎬 frames/           # Animation frames (99 files)
├── 🔧 scripts/              # Utilities and recording tools
│   ├── 🎙️ record_system_audio.sh    # System audio recording
│   ├── 🎧 record_with_blackhole.sh  # Enhanced audio setup
│   ├── 🎤 record_mic_only.sh        # Microphone fallback
│   ├── 🎬 extract_frames.py         # Animation processing
│   ├── 🖼️ remove_gif_background.py  # Image processing
│   ├── 📏 test_scaling.py           # Graphics testing
│   └── ⚙️ test_setup.py            # Environment verification
└── 📚 docs/                 # Documentation
    ├── TECHNICAL_DOCUMENTATION.md   # Complete technical guide
    └── PROBLEMS_ANALYSIS.md         # Issue tracking & solutions
```

### **📊 Organization Benefits:**
- **🎯 Clear Separation:** Each folder serves a specific purpose
- **🔍 Easy Navigation:** Find files quickly by category
- **🛠️ Maintainable:** Simple to add new features and assets
- **👥 Collaborative:** Professional structure for team development
- **📈 Scalable:** Ready for future expansion and enhancements

## 🛠️ Technology Stack

- **Python 3.13.3** - Core application
- **Pygame 2.6.1** - Graphics and audio
- **FFmpeg** - Professional video recording
- **BlackHole 2ch** - System audio capture

## 🧠 BCI Integration

**Current:** Keyboard simulation for testing and demonstration
**Future:** Real EEG device integration for brain-computer interface

### **Applications:**
- Neurofeedback therapy
- Stress reduction training
- Meditation enhancement
- ADHD therapy support
- Anxiety management

## 🎯 Features

### **Visual Effects:**
- Dynamic sky color transitions
- Particle-based animations (leaves, water drops)
- Progressive tree growth with 3 evolution stages
- Real-time health metrics visualization

### **Audio System:**
- Background ambient music
- Interactive water sound effects
- Multi-channel audio mixing
- High-quality recording support

### **Recording Capabilities:**
- 4K resolution support (2880×1800)
- Professional H.264 video encoding
- High-fidelity AAC audio
- System audio capture

## � Development Workflow

### **Setup:**
```bash
# Clone the repository
git clone https://github.com/AseshNemal/NeuroNest.git
cd NeuroNest

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python neuronest.py
```

### **Testing Recording:**
```bash
# Test system audio recording
./scripts/record_system_audio.sh

# Test with enhanced audio setup
./scripts/record_with_blackhole.sh

# Verify environment setup
python scripts/test_setup.py
```

## �🔧 System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- 2GB storage
- 1280×720 display

**Recommended:**
- Python 3.13.3
- 8GB+ RAM
- macOS 12.0+ (for recording)
- 1920×1080+ display

## 📊 Performance

- **30 FPS** target frame rate
- **<3 second** startup time
- **~150MB** memory usage
- **15-25%** CPU usage

## 🔬 Research Applications

This application is designed for:
- **Neurofeedback Research** - Real-time brain state monitoring
- **Therapeutic Use** - Clinical relaxation and stress reduction
- **Academic Studies** - Meditation and mindfulness research
- **Data Collection** - Session metrics and progress tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- **Issues:** GitHub Issues
- **Documentation:** `/docs/TECHNICAL_DOCUMENTATION.md`
- **Research:** Academic collaboration welcome

## � Quick Reference

### **Key Files:**
- `neuronest.py` - Main application
- `scripts/record_system_audio.sh` - Recording tool
- `docs/TECHNICAL_DOCUMENTATION.md` - Complete guide
- `PROJECT_STRUCTURE.md` - Folder organization
- `LICENSE` - MIT License terms

### **Essential Commands:**
```bash
python neuronest.py              # Run application
./scripts/record_system_audio.sh # Record session
python scripts/test_setup.py     # Verify setup
```

### **File Count:**
- **Main App:** 1 file
- **Assets:** 105 files (images, audio, animations)
- **Scripts:** 7 utility files
- **Documentation:** 4 files
- **License:** 1 file
- **Total:** ~118 organized files

## �📄 License

Open source - see license file for details.

---

**Developed for Brain-Computer Interface Research**  
*Combining neuroscience, technology, and mindfulness*

🌱 *Grow your mind, nurture your well-being*

