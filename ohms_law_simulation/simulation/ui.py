"""
UI Module for Ohm's Law Simulation
Handles all user interface elements using DirectGUI
"""

from direct.gui.DirectGui import (
    DirectFrame, DirectLabel, DirectButton, DirectSlider, OnscreenText
)
from panda3d.core import TextNode, Vec3


class SimulationUI:
    """
    Manages all UI elements for the simulation including sliders,
    labels, buttons, and real-time displays.
    """
    
    def __init__(self, physics_engine, update_callback):
        """
        Initialize UI system.
        
        Args:
            physics_engine: Reference to OhmsLawPhysics instance
            update_callback: Function to call when values change
        """
        self.physics = physics_engine
        self.update_callback = update_callback
        self.elements = []
        
        self._create_ui()
    
    def _create_ui(self):
        """Create all UI elements"""
        self._create_title()
        self._create_voltage_slider()
        self._create_resistance_slider()
        self._create_displays()
        self._create_preset_buttons()
        self._create_info_panel()
        self._create_warning_label()
    
    def _create_title(self):
        """Create main title"""
        self.title = OnscreenText(
            text="Ohm's Law Interactive Simulation",
            pos=(0, 0.92),
            scale=0.09,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            mayChange=False,
            shadow=(0, 0, 0, 0.8),
            shadowOffset=(0.05, 0.05)
        )
        self.elements.append(self.title)
        
        self.subtitle = OnscreenText(
            text="V = I x R",
            pos=(0, 0.84),
            scale=0.07,
            fg=(1, 1, 0.3, 1),
            align=TextNode.ACenter,
            mayChange=False,
            shadow=(0, 0, 0, 0.6),
            shadowOffset=(0.03, 0.03)
        )
        self.elements.append(self.subtitle)
    
    def _create_voltage_slider(self):
        """Create voltage control slider"""
        # Background panel
        voltage_panel = DirectFrame(
            pos=(-1.3, 0, 0.6),
            frameSize=(-0.4, 0.4, -0.25, 0.25),
            frameColor=(0.15, 0.15, 0.2, 0.85)
        )
        self.elements.append(voltage_panel)
        
        # Label
        voltage_label = DirectLabel(
            text="VOLTAGE (V)",
            pos=(-1.3, 0, 0.78),
            scale=0.055,
            text_fg=(1, 0.4, 0.4, 1),
            frameColor=(0, 0, 0, 0),
            text_font=None,
            textMayChange=False
        )
        self.elements.append(voltage_label)
        
        # Slider
        self.voltage_slider = DirectSlider(
            range=(self.physics.MIN_VOLTAGE, self.physics.MAX_VOLTAGE),
            value=self.physics.voltage,
            pageSize=1,
            pos=(-1.3, 0, 0.63),
            scale=0.4,
            command=self._on_voltage_change,
            frameColor=(0.25, 0.25, 0.3, 0.9),
            thumb_frameColor=(1, 0.2, 0.2, 1),
            relief=1
        )
        self.elements.append(self.voltage_slider)
        
        # Value display with glow effect
        self.voltage_value_label = DirectLabel(
            text=f"{self.physics.voltage:.1f}V",
            pos=(-1.3, 0, 0.48),
            scale=0.06,
            text_fg=(1, 1, 1, 1),
            frameColor=(0.2, 0.05, 0.05, 0.9),
            pad=(0.4, 0.25),
            relief=1
        )
        self.elements.append(self.voltage_value_label)
    
    def _create_resistance_slider(self):
        """Create resistance control slider"""
        # Background panel
        resistance_panel = DirectFrame(
            pos=(-1.3, 0, 0.15),
            frameSize=(-0.4, 0.4, -0.25, 0.25),
            frameColor=(0.15, 0.15, 0.2, 0.85)
        )
        self.elements.append(resistance_panel)
        
        # Label
        resistance_label = DirectLabel(
            text="RESISTANCE (Ohm)",
            pos=(-1.3, 0, 0.33),
            scale=0.055,
            text_fg=(0.4, 0.6, 1, 1),
            frameColor=(0, 0, 0, 0),
            textMayChange=False
        )
        self.elements.append(resistance_label)
        
        # Slider
        self.resistance_slider = DirectSlider(
            range=(self.physics.MIN_RESISTANCE, self.physics.MAX_RESISTANCE),
            value=self.physics.resistance,
            pageSize=1,
            pos=(-1.3, 0, 0.18),
            scale=0.4,
            command=self._on_resistance_change,
            frameColor=(0.25, 0.25, 0.3, 0.9),
            thumb_frameColor=(0.2, 0.4, 1, 1),
            relief=1
        )
        self.elements.append(self.resistance_slider)
        
        # Value display
        self.resistance_value_label = DirectLabel(
            text=f"{self.physics.resistance:.1f} Ohm",
            pos=(-1.3, 0, 0.03),
            scale=0.06,
            text_fg=(1, 1, 1, 1),
            frameColor=(0.05, 0.1, 0.2, 0.9),
            pad=(0.4, 0.25),
            relief=1
        )
        self.elements.append(self.resistance_value_label)
    
    def _create_displays(self):
        """Create read-only displays for calculated values"""
        # Display panel background
        display_panel = DirectFrame(
            pos=(1.6, 0, 0.55),
            frameSize=(-0.45, 0.45, -0.35, 0.35),
            frameColor=(0.1, 0.12, 0.15, 0.9)
        )
        self.elements.append(display_panel)
        
        # Current display
        current_label = DirectLabel(
            text="CURRENT",
            pos=(1.6, 0, 0.78),
            scale=0.055,
            text_fg=(1, 1, 0.4, 1),
            frameColor=(0, 0, 0, 0),
            text_align=TextNode.ACenter
        )
        self.elements.append(current_label)
        
        self.current_display = DirectLabel(
            text=f"{self.physics.current:.3f} A",
            pos=(1.6, 0, 0.68),
            scale=0.08,
            text_fg=(1, 1, 0.2, 1),
            frameColor=(0.15, 0.15, 0.05, 0.95),
            text_align=TextNode.ACenter,
            pad=(0.5, 0.3),
            relief=2
        )
        self.elements.append(self.current_display)
        
        # Power display
        power_label = DirectLabel(
            text="POWER",
            pos=(1.6, 0, 0.5),
            scale=0.055,
            text_fg=(1, 0.6, 0.3, 1),
            frameColor=(0, 0, 0, 0),
            text_align=TextNode.ACenter
        )
        self.elements.append(power_label)
        
        self.power_display = DirectLabel(
            text=f"{self.physics.power:.2f} W",
            pos=(1.6, 0, 0.4),
            scale=0.08,
            text_fg=(1, 0.7, 0.2, 1),
            frameColor=(0.15, 0.08, 0.02, 0.95),
            text_align=TextNode.ACenter,
            pad=(0.5, 0.3),
            relief=2
        )
        self.elements.append(self.power_display)
    
    def _create_preset_buttons(self):
        """Create preset scenario buttons at bottom right"""
        # Preset panel background moved to bottom right
        preset_panel = DirectFrame(
            pos=(1.6, 0, -0.65), 
            frameSize=(-0.45, 0.45, -0.5, 0.15),
            frameColor=(0.1, 0.12, 0.15, 0.9)
        )
        self.elements.append(preset_panel)
        
        preset_title = DirectLabel(
            text="PRESETS",
            pos=(1.6, 0, -0.42),
            scale=0.055,
            text_fg=(0.7, 0.8, 1, 1),
            frameColor=(0, 0, 0, 0),
            text_align=TextNode.ACenter
        )
        self.elements.append(preset_title)
        
        presets = [
            ("Normal", "normal", -0.55, (0.4, 0.6, 0.4, 0.9)),
            ("High Current", "high_current", -0.65, (0.8, 0.4, 0.2, 0.9)),
            ("Low Current", "low_current", -0.75, (0.3, 0.5, 0.7, 0.9)),
            ("Short Circuit", "short_circuit", -0.85, (0.9, 0.2, 0.2, 0.9)),
            ("Open Circuit", "open_circuit", -0.95, (0.5, 0.5, 0.5, 0.9))
        ]
        
        for label, preset_name, y_offset, color in presets:
            button = DirectButton(
                text=label,
                pos=(1.6, 0, y_offset),
                scale=0.045,
                command=self._on_preset_click,
                extraArgs=[preset_name],
                frameColor=color,
                text_fg=(1, 1, 1, 1),
                relief=2,
                pressEffect=1,
                pad=(0.3, 0.15)
            )
            self.elements.append(button)
    def _create_info_panel(self):
        """Create informational panel with educational content"""
        info_bg = DirectFrame(
            pos=(-1.3, 0, -0.5),
            frameSize=(-0.35, 0.35, -0.35, 0.15),
            frameColor=(0.1, 0.1, 0.2, 0.7)
        )
        self.elements.append(info_bg)
        
        info_title = DirectLabel(
            text="Ohm's Law:",
            pos=(-1.3, 0, -0.38),
            scale=0.04,
            text_fg=(1, 1, 0.5, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(info_title)
        
        formulas = [
            ("I = V / R", -0.46),
            ("P = V x I", -0.53),
            ("V = Voltage (V)", -0.63),
            ("I = Current (A)", -0.69),
            ("R = Resistance (Ω)", -0.75),
            ("P = Power (W)", -0.81)
        ]
        
        for text, y_pos in formulas:
            label = DirectLabel(
                text=text,
                pos=(-1.3, 0, y_pos),
                scale=0.032,
                text_fg=(0.9, 0.9, 0.9, 1),
                frameColor=(0, 0, 0, 0),
                text_align=TextNode.ACenter
            )
            self.elements.append(label)
    
    def _create_warning_label(self):
        """Create warning label for dangerous conditions"""
        self.warning_label = OnscreenText(
            text="",
            pos=(0, -0.85),
            scale=0.05,
            fg=(1, 0.2, 0.2, 1),
            align=TextNode.ACenter,
            mayChange=True
        )
        self.elements.append(self.warning_label)
    
    def _on_voltage_change(self):
        """Handle voltage slider change"""
        new_voltage = self.voltage_slider['value']
        self.physics.voltage = new_voltage
        self.update_displays()
        self.update_callback()
    
    def _on_resistance_change(self):
        """Handle resistance slider change"""
        new_resistance = self.resistance_slider['value']
        self.physics.resistance = new_resistance
        self.update_displays()
        self.update_callback()
    
    def _on_preset_click(self, preset_name):
        """
        Handle preset button click.
        
        Args:
            preset_name (str): Name of the preset to apply
        """
        if self.physics.set_preset(preset_name):
            # Update sliders to match preset
            self.voltage_slider['value'] = self.physics.voltage
            self.resistance_slider['value'] = self.physics.resistance
            self.update_displays()
            self.update_callback()
    
    def update_displays(self):
        """Update all dynamic display elements"""
        # Update slider value labels
        self.voltage_value_label['text'] = f"{self.physics.voltage:.1f}V"
        self.resistance_value_label['text'] = f"{self.physics.resistance:.1f} Ohm"
        
        # Update calculated value displays with color coding
        current_color = min(self.physics.current / 10.0, 1.0)
        self.current_display['text'] = f"{self.physics.current:.3f} A"
        self.current_display['text_fg'] = (1, 1 - current_color * 0.5, 0.2, 1)
        
        power_color = min(self.physics.power / 200.0, 1.0)
        self.power_display['text'] = f"{self.physics.power:.2f} W"
        self.power_display['text_fg'] = (1, 0.7 - power_color * 0.3, 0.2, 1)
        
        # Update warning label
        is_dangerous, warning_msg = self.physics.is_dangerous()
        if is_dangerous:
            self.warning_label.setText(warning_msg)
        else:
            self.warning_label.setText("")
    
    def cleanup(self):
        """Clean up all UI elements"""
        for element in self.elements:
            element.destroy()
        self.elements.clear()


class HelpOverlay:
    """Optional help overlay with keyboard shortcuts and tips"""
    
    def __init__(self):
        """Create help overlay"""
        self.visible = False
        self.elements = []
        self._create_overlay()
        self.hide()
    
    def _create_overlay(self):
        """Create help text elements"""
        # Semi-transparent background
        self.bg = DirectFrame(
            pos=(0, 0, 0),
            frameSize=(-2, 2, -1.5, 1.5),
            frameColor=(0, 0, 0, 0.92)
        )
        self.elements.append(self.bg)
        
        # Help text with improved formatting
        help_text = [
            "3D CAMERA CONTROLS",
            "",
            "Mouse Drag: Click and drag to orbit camera",
            "WASD Keys: Free movement in 3D space",
            "Q/E Keys: Move camera up/down",
            "Arrow Keys: Orbit around circuit",
            "Mouse Wheel / +/-: Zoom in/out",
            "",
            "SIMULATION CONTROLS",
            "",
            "Left Panel: Voltage & Resistance sliders",
            "Right Panel: Preset scenario buttons",
            "Number Keys 1-5: Quick preset selection",
            "R Key: Reset to defaults",
            "F Key: Toggle wireframe view",
            "H Key: Toggle this help",
            "ESC Key: Exit simulation",
            "",
            "VISUAL INDICATORS",
            "",
            "- Yellow particles = Electron flow",
            "- Speed indicates current intensity",
            "- Color brightness shows power level",
            "- Red warnings for dangerous conditions",
            "",
            "Press H to close"
        ]
        
        y_pos = 0.7
        for line in help_text:
            if line.isupper():
                scale = 0.065
                color = (1, 0.8, 0.3, 1)
                y_spacing = 0.1
            elif line == "":
                y_pos -= 0.04
                continue
            else:
                scale = 0.048
                color = (0.9, 0.9, 0.9, 1)
                y_spacing = 0.065
            
            label = OnscreenText(
                text=line,
                pos=(0, y_pos),
                scale=scale,
                fg=color,
                align=TextNode.ACenter,
                shadow=(0, 0, 0, 0.5),
                shadowOffset=(0.02, 0.02)
            )
            self.elements.append(label)
            y_pos -= y_spacing
    
    def toggle(self):
        """Toggle help overlay visibility"""
        if self.visible:
            self.hide()
        else:
            self.show()
    
    def show(self):
        """Show help overlay"""
        self.visible = True
        for element in self.elements:
            element.show()
    
    def hide(self):
        """Hide help overlay"""
        self.visible = False
        for element in self.elements:
            element.hide()
    
    def cleanup(self):
        """Clean up help overlay"""
        for element in self.elements:
            if hasattr(element, 'destroy'):
                element.destroy()
            else:
                element.removeNode()
        self.elements.clear()
