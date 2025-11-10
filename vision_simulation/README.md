# Vision & Eyeglass Power Simulation

![Physics](https://img.shields.io/badge/Physics-Optics-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Panda3D](https://img.shields.io/badge/Panda3D-1.10+-orange)
![Education](https://img.shields.io/badge/Education-3D_Simulation-purple)
![Biology](https://img.shields.io/badge/Biology-Anatomy-red)
![MIT License](https://img.shields.io/badge/License-MIT-brightgreen)

An immersive educational 3D visualization of **human eye optics and vision correction** built with Panda3D. Experience real-time optical relationships through interactive controls and dynamic visual feedback.

---

## 🎓 Educational Objectives

- **Visual Learning**: See lens formula and light refraction in action with animated ray tracing
- **Interactive Exploration**: Experiment with different vision conditions and corrective lenses
- **Real-time Feedback**: Observe how changing lens power affects focus on the retina
- **Preset Scenarios**: Learn from common vision conditions (myopia, hyperopia, presbyopia)
- **Intuitive Understanding**: Develop intuition about optical relationships and corrective principles

---

## ✨ Features

### 🎮 Interactive Controls
- **Near Point Slider**: Adjust minimum clear vision distance (10-100cm)
- **Object Distance Slider**: Modify test object distance (10-100cm)
- **Lens Power Slider**: Adjust corrective lens strength (-10D to +10D)
- **Age Slider**: Change accommodation ability (10-80 years)
- **Real-time Calculations**: Instant optical power and focus quality updates
- **Preset Scenarios**: 
  - Normal Vision (25cm near point)
  - Mild Myopia (15cm near point)
  - Moderate Myopia (12cm near point)
  - Mild Hyperopia (40cm near point)
  - Presbyopia (50cm near point, age 60)

### 👁️ Visual Feedback
- **Ray Tracing**: Multi-segment light path visualization with refraction
- **Focus Indicators**: Visual cues for proper/improper focus on retina
- **Color Coding**: Different colors for incident and refracted rays
- **Anatomical Accuracy**: Detailed eye model with cornea, lens, retina, fovea
- **Dynamic Focal Point**: Shows where light converges based on correction

### 🎯 3D Visualization
- **Anatomical Eye Model**: Cornea, crystalline lens, retina, fovea, optic nerve
- **Corrective Lenses**: Transparent lenses showing power adjustment
- **Light Rays**: Animated rays showing complete optical path
- **Test Object**: Professional Snellen chart with letter E
- **Professional Labels**: Clear anatomical pointers with dashed lines

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Run
```bash
# Clone or download the project
cd vision_simulation

# Install dependencies
pip install panda3d

# Run the simulation
python main.py
```

### 🎮 Controls Summary

| Key | Action |
|-----|--------|
| `Mouse Drag` | Orbit around scene |
| `Scroll Wheel` | Zoom in/out |
| `Arrow Keys` | Precise rotation |
| `F` | Toggle wireframe mode |
| `ESC` | Exit simulation |

---

## 📸 Simulation Interface

### Main Interface Features

<div align="center">
<img width="1919" height="1048" alt="Vision Simulation Interface" src="https://github.com/user-attachments/assets/cfc0455e-13d1-4955-b71e-9c950bb5ad59" />
<img width="1919" height="1048" alt="Vision Simulation Close-up" src="https://github.com/user-attachments/assets/fac8525b-b5f8-40b0-b1a8-7ae26141e6b8" />
</div>

- **Left Panel**: Interactive sliders for all optical parameters
- **Right Panel**: Real-time diagnosis and patient presets  
- **Central View**: 3D anatomical eye with ray tracing
- **Info Panel**: Lens formula and optical principles
- **Top Bar**: Simulation title and educational context
- **Control Sliders**: Precise adjustment of vision parameters
- **Diagnostic Display**: Live feedback on vision condition and correction quality
- **Preset Buttons**: Quick-load common vision scenarios
- **3D Visualization**: Interactive anatomical model with light ray tracing


### Visual Elements
- **Yellow Rays**: Light paths from object to retina
- **Green Focal Point**: Convergence point of light rays
- **Colored Buttons**: Patient condition presets
- **Transparent Lens**: Corrective eyeglass lens
- **Anatomical Labels**: Professional pointers to eye structures

---

## 🏗️ Project Structure

```
vision_simulation/
├── main.py                 # Main application controller
├── simulation/
│   ├── __init__.py
│   ├── physics.py          # Optical calculations & presets
│   ├── optical_components.py # 3D eye models & ray tracing
│   └── ui.py              # Interactive GUI controls
└── README.md
```

### Core Modules

#### `main.py`
- **VisionSimulation** class: Main application controller
- Camera setup and orbital controls
- Input handling and scene management
- Real-time physics updates

#### `simulation/physics.py`
- **VisionPhysics** class: Optical calculations
- Lens formula implementation (1/f = 1/v - 1/u)
- Diopter power calculations (P = 1/f)
- Age-based accommodation effects
- Patient preset configurations

#### `simulation/optical_components.py`
- **EyeModel** class: Anatomical 3D eye assembly
- **CorrectiveLens**: Eyeglass lens visualization
- **LightRay**: Ray tracing with refraction
- **VisionScene**: Complete optical environment

#### `simulation/ui.py`
- **VisionUI** class: Professional interface
- DirectGUI sliders and displays
- Preset buttons and diagnostic panels
- Real-time status updates

---

## 📚 Educational Use Cases

### 🏫 Classroom Demonstrations
1. **Basic Concepts**: Demonstrate lens formula and focal relationships
2. **Vision Conditions**: Show how myopia and hyperopia affect focus
3. **Correction Principles**: Explain how eyeglasses correct vision
4. **Age Effects**: Illustrate presbyopia and accommodation loss

### 🔬 Student Experiments
- Predict focal points before adjusting lens power
- Compare theoretical calculations with simulation
- Explore different vision correction scenarios
- Document optical relationships and observations

### 🧪 Lab Activities
1. **Verify Lens Formula**: Test with multiple object distances
2. **Vision Analysis**: Calculate required corrective power for conditions
3. **Problem Solving**: Use simulation to check optical physics problems

---

## 🔧 Optical Physics

### Core Equations
- **Lens Formula**: `1/f = 1/v - 1/u`
- **Optical Power**: `P = 1/f` (in diopters, f in meters)
- **Near Point**: Minimum distance for clear vision
- **Accommodation**: Eye's ability to change focus

### Vision Conditions
- **Myopia (Nearsighted)**: Near point < 25cm → Concave lenses
- **Hyperopia (Farsighted)**: Near point > 25cm → Convex lenses  
- **Presbyopia**: Age-related accommodation loss → Reading glasses
- **Normal Vision**: Near point ≈ 25cm → No correction needed

---

## 🎮 UI Controls Detail

### Parameter Ranges
- **Near Point**: 10cm (extreme myopia) to 100cm (severe hyperopia)
- **Object Distance**: 10cm to 100cm
- **Lens Power**: -10D (strong concave) to +10D (strong convex)
- **Age**: 10 years (full accommodation) to 80 years (presbyopia)

### Diagnostic Display
- **Condition**: Auto-detected vision type
- **Required Power**: Calculated corrective power
- **Lens Type**: Recommended lens type
- **Focus Quality**: Percentage of optimal focus

---

## 🔧 Customization

### Modifying Value Ranges
Edit `simulation/physics.py`:
```python
MIN_NEAR_POINT = 10.0     # Extreme myopia
MAX_NEAR_POINT = 100.0    # Extreme hyperopia
MIN_POWER = -10.0         # Strong concave
MAX_POWER = 10.0          # Strong convex
```

### Adding New Presets
```python
PRESETS = {
    'custom_preset': {
        'near_point': 30.0,
        'age': 35,
        'description': 'Custom Vision Condition'
    }
}
```

---

## 🐛 Troubleshooting

### Common Issues
**Problem**: `pip install panda3d` fails
- **Solution**: Update pip: `pip install --upgrade pip`

**Problem**: Low frame rate
- **Solution**: Reduce ray count in `optical_components.py`
- **Solution**: Update graphics drivers

**Problem**: Black screen or missing components
- **Solution**: Check Panda3D installation
- **Solution**: Update graphics drivers

**Problem**: Camera controls not working
- **Solution**: Ensure mouse/focus is on the 3D window
- **Solution**: Check for conflicting keyboard shortcuts

---

## 🚧 Future Enhancements

- Astigmatism simulation with cylindrical lenses
- Contact lens effects visualization
- Surgical corrections (LASIK) simulation
- Color vision deficiencies
- Multiple lens systems (bifocals, progressives)
- Wavefront analysis and aberrations

---

## 📖 Learning Resources

### Eye Optics & Vision Science
- [American Academy of Ophthalmology - Eye Health](https://www.aao.org/eye-health)
- [National Eye Institute (NIH) - How Eyes Work](https://www.nei.nih.gov/learn-about-eye-health/healthy-vision/how-eyes-work)
- [HyperPhysics - Vision and Eye Optics](http://hyperphysics.phy-astr.gsu.edu/hbase/vision)
- [Physics Classroom - Refraction and Lenses](https://www.physicsclassroom.com/class/refrn)

### Optical Physics
- [MIT OpenCourseWare - Geometric Optics](https://ocw.mit.edu/courses/physics/8-03sc-physics-iii-vibrations-and-waves-fall-2016/geometric-optics/)
- [Optical Society - Optics for Kids](https://www.optics4kids.org/)
- [PhET Interactive Simulations - Geometric Optics](https://phet.colorado.edu/en/simulations/geometric-optics)

### Panda3D Development
- [Panda3D Manual](https://docs.panda3d.org/)
- [Panda3D Tutorial](https://arsthaumaturgis.github.io/Panda3DTutorial.io/)

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. 🍴 Fork the project
2. 🌿 Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔃 Open a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

<a href="https://x.com/hridewel" style="text-decoration: none; margin-right: 20px;">
  <img src="https://cdn-icons-png.flaticon.com/24/733/733579.png" alt="Twitter" style="vertical-align: middle;" />
</a>
&nbsp;&nbsp;&nbsp;
<a href="https://www.linkedin.com/in/hridoychowdhury/" style="text-decoration: none;">
  <img src="https://cdn-icons-png.flaticon.com/24/174/174857.png" alt="LinkedIn" style="vertical-align: middle;" /> 
</a>

---

## 🎓 Credits

**Concept**: Interactive optics education  
**Engine**: Panda3D - Open-source 3D engine  
**Physics**: Based on classical optics and lens formulas  
**Anatomy**: Accurate human eye model based on biological references

---

**Made with ❤️ for physics and biology education**

*Visualize. Understand. Learn.*

---

*Part of the Science Simulations Collection - Bridging Physics and Biology through Interactive 3D Visualization*