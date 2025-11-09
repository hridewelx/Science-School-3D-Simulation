# Ohm's Law Interactive 3D Simulation

![Physics](https://img.shields.io/badge/Physics-Interactive-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Panda3D](https://img.shields.io/badge/Panda3D-1.10+-orange)
![Education](https://img.shields.io/badge/Education-3D_Simulation-purple)
![MIT License](https://img.shields.io/badge/License-MIT-brightgreen)

An immersive educational 3D visualization of **Ohm's Law** (V = I × R) built with Panda3D. Experience real-time electrical relationships through interactive controls and dynamic visual feedback.

---

## 🎓 Educational Objectives

- **Visual Learning**: See Ohm's Law in action with animated electron flow
- **Interactive Exploration**: Experiment with different voltage and resistance values
- **Real-time Feedback**: Observe how changing one parameter affects others
- **Preset Scenarios**: Learn from common circuit configurations
- **Intuitive Understanding**: Develop intuition about electrical relationships

---

## ✨ Features

### 🎮 Interactive Controls
- **Voltage Slider**: Adjust voltage from 1V to 50V
- **Resistance Slider**: Modify resistance from 1Ω to 100Ω
- **Real-time Calculations**: Instant current and power updates
- **Preset Scenarios**: 
  - Normal Operation (12V, 10Ω)
  - High Current (24V, 2Ω)
  - Low Current (5V, 50Ω)
  - Short Circuit (12V, 0.1Ω)
  - Open Circuit (12V, 100Ω)

### 👁️ Visual Feedback
- **Electron Animation**: Yellow particles representing electron flow
- **Speed Variation**: Particle speed proportional to current
- **Color Intensity**: Visual indicators based on electrical values
- **Component Highlighting**: Battery and resistor change appearance with parameters
- **Warning System**: Alerts for potentially dangerous conditions

### 🎯 3D Visualization
- **Battery**: Red geometric representation with voltage indicators
- **Resistor**: Blue component with resistance-dependent coloring
- **Wires**: Gray connecting elements
- **Electrons**: Animated yellow spheres showing current flow
- **Professional Lighting**: Multi-directional lighting for clear visibility

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Run
```bash
# Clone or download the project
cd ohms_law_simulation

# Install dependencies
pip install panda3d

# Run the simulation
python main.py
```

### 🎮 Controls Summary

| Key | Action |
|-----|--------|
| `H` | Toggle help overlay |
| `R` | Reset to default values |
| `ESC` | Exit simulation |
| `1-5` | Quick preset selection |
| `Mouse Drag` | Rotate camera |
| `WASD` | Free camera movement |
| `+/-` | Zoom in/out |

---

## 📸 Simulation Preview

### Main Interface
![Ohm's Law Simulation Main Interface](https://github.com/user-attachments/assets/53e57fc4-739d-46ae-88e5-2437d26dd8a7)
*Interactive controls with real-time circuit visualization*

### Electron Flow  
![Electron Flow Visualization](https://github.com/user-attachments/assets/24b5f9cf-a8bb-48ec-a573-6486db29ce6f)
*Yellow particles showing current intensity through circuit*

---

## 🏗️ Project Structure

```
ohms_law_simulation/
├── main.py                 # Main application controller
├── simulation/
│   ├── physics.py          # Ohm's Law calculations & presets
│   ├── circuit.py          # 3D circuit components & animation
│   └── ui.py              # Interactive GUI controls
├── requirements.txt        # Dependencies
└── README.md              # This file
```

### Core Modules

#### `main.py`
- **OhmsLawSimulation** class: Main application controller
- Camera setup and scene configuration
- Input handling and event management

#### `simulation/physics.py`
- **OhmsLawPhysics** class: Electrical calculations
- Ohm's Law implementation (I = V / R)
- Power calculations (P = V × I)
- Safety checks and warnings

#### `simulation/circuit.py`
- **Circuit** class: Complete 3D circuit assembly
- **Battery**, **Resistor**, **Wire** components
- **Electron** particles: Current flow animation

#### `simulation/ui.py`
- **SimulationUI** class: Interactive controls
- DirectGUI sliders and displays
- Preset buttons and help system

---

## 📚 Educational Use Cases

### 🏫 Classroom Demonstrations
1. **Basic Concepts**: Demonstrate V = I × R relationship
2. **Cause and Effect**: Show how changing V or R affects I
3. **Power Dissipation**: Explain P = V × I with visual feedback
4. **Safety**: Illustrate dangers of short circuits

### 🔬 Student Experiments
- Predict outcomes before adjusting sliders
- Compare theoretical calculations with simulation
- Explore extreme scenarios safely
- Document observations and relationships

### 🧪 Lab Activities
1. **Verify Ohm's Law**: Test with multiple V and R combinations
2. **Power Analysis**: Calculate and observe power dissipation
3. **Problem Solving**: Use simulation to check homework solutions

---

## 🔧 Customization

### Modifying Value Ranges
Edit `simulation/physics.py`:
```python
MIN_VOLTAGE = 1.0      # Minimum voltage
MAX_VOLTAGE = 50.0     # Maximum voltage
MIN_RESISTANCE = 1.0   # Minimum resistance
MAX_RESISTANCE = 100.0 # Maximum resistance
```

### Adding New Presets
```python
PRESETS = {
    'my_preset': {'voltage': 15.0, 'resistance': 25.0}
}
```

---

## 🐛 Troubleshooting

### Common Issues
**Problem**: `pip install panda3d` fails
- **Solution**: Update pip: `pip install --upgrade pip`

**Problem**: Low frame rate
- **Solution**: Reduce electron count in `circuit.py`
- **Solution**: Update graphics drivers

**Problem**: Black screen or missing components
- **Solution**: Check Panda3D installation
- **Solution**: Update graphics drivers

---

## 🚧 Future Enhancements

- Multiple resistors in series/parallel
- Capacitors and inductors
- AC circuit simulation
- Multimeter visualization
- Data export for analysis
- Circuit designer mode

---

## 📖 Learning Resources

### Ohm's Law
- [Khan Academy - Ohm's Law](https://www.khanacademy.org/science/physics/electric-charge-electric-force-and-voltage/electric-current-resistivity-and-ohms-law)
- [Electronics Tutorials - Ohm's Law](https://www.electronics-tutorials.ws/dccircuits/dcp_2.html)

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

## 👨‍💻 Developer

<a href="https://x.com/hridewel" style="text-decoration: none; margin-right: 20px;">
  <img src="https://cdn-icons-png.flaticon.com/24/733/733579.png" alt="Twitter" style="vertical-align: middle;" />
</a>
&nbsp;&nbsp;&nbsp;
<a href="https://www.linkedin.com/in/hridoychowdhury/" style="text-decoration: none;">
  <img src="https://cdn-icons-png.flaticon.com/24/174/174857.png" alt="LinkedIn" style="vertical-align: middle;" /> 
</a>

---

## 🎓 Credits

**Concept**: Interactive physics education  
**Engine**: Panda3D - Open-source 3D engine  
**Physics**: Based on Georg Ohm's fundamental law (1827)

---

**Made with ❤️ for physics education**

*Visualize. Understand. Learn.*