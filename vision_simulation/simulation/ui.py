"""
UI Module for Vision Simulation
Professional interface for controlling vision parameters
"""

from direct.gui.DirectGui import (
    DirectFrame, DirectLabel, DirectButton, DirectSlider, OnscreenText
)
from panda3d.core import TextNode


class VisionUI:
    """Manages all UI elements for vision simulation"""
    
    def __init__(self, physics_engine, update_callback, showbase):
        """
        Initialize UI system.
        
        Args:
            physics_engine: Reference to VisionPhysics instance
            update_callback: Function to call when values change
            showbase: ShowBase instance for accessing window properties
        """
        self.physics = physics_engine
        self.update_callback = update_callback
        self.showbase = showbase
        self.elements = []
        self._create_ui()
    
    def _create_ui(self):
        """Create all UI elements with professional positioning"""
        # Calculate positions based on aspect ratio
        aspect_ratio = self.showbase.getAspectRatio()
        self.left_edge = -aspect_ratio + 0.3
        self.right_edge = aspect_ratio - 0.3
        
        self._create_title()
        self._create_near_point_slider()
        self._create_object_distance_slider()
        self._create_lens_power_slider()
        self._create_age_slider()
        self._create_displays()
        self._create_preset_buttons()
        self._create_info_panel()
    
    def _create_title(self):
        self.title = OnscreenText(
            text="Vision & Eyeglass Power Simulator",
            pos=(0, 0.92),
            scale=0.085,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            mayChange=False,
            shadow=(0, 0, 0, 0.8),
            shadowOffset=(0.04, 0.04)
        )
        self.elements.append(self.title)
        
        self.subtitle = OnscreenText(
            text="Interactive Optical Physics Education",
            pos=(0, 0.84),
            scale=0.055,
            fg=(0.7, 0.9, 1.0, 1),
            align=TextNode.ACenter,
            mayChange=False,
            shadow=(0, 0, 0, 0.6),
            shadowOffset=(0.03, 0.03)
        )
        self.elements.append(self.subtitle)
    
    def _create_near_point_slider(self):
        # Panel - far left
        panel = DirectFrame(
            pos=(-1.35, 0, 0.6),
            frameSize=(-0.42, 0.42, -0.22, 0.22),
            frameColor=(0.12, 0.14, 0.18, 0.9)
        )
        self.elements.append(panel)
        
        # Label
        label = DirectLabel(
            text="NEAR POINT (cm)",
            pos=(-1.35, 0, 0.75),
            scale=0.05,
            text_fg=(1, 0.7, 0.4, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(label)
        
        # Slider
        self.near_point_slider = DirectSlider(
            range=(self.physics.MIN_NEAR_POINT, self.physics.MAX_NEAR_POINT),
            value=self.physics.near_point,
            pageSize=1,
            pos=(-1.35, 0, 0.63),
            scale=0.42,
            command=self._on_near_point_change,
            frameColor=(0.2, 0.22, 0.25, 0.95),
            thumb_frameColor=(1, 0.6, 0.3, 1),
            relief=2
        )
        self.elements.append(self.near_point_slider)
        
        # Value display
        self.near_point_value = DirectLabel(
            text=f"{self.physics.near_point:.1f} cm",
            pos=(-1.35, 0, 0.48),
            scale=0.055,
            text_fg=(1, 1, 1, 1),
            frameColor=(0.18, 0.12, 0.08, 0.95),
            pad=(0.35, 0.22),
            relief=2
        )
        self.elements.append(self.near_point_value)
    
    def _create_object_distance_slider(self):
        # Panel - far left
        panel = DirectFrame(
            pos=(-1.35, 0, 0.15),
            frameSize=(-0.42, 0.42, -0.22, 0.22),
            frameColor=(0.12, 0.14, 0.18, 0.9)
        )
        self.elements.append(panel)
        
        # Label
        label = DirectLabel(
            text="OBJECT DISTANCE (cm)",
            pos=(-1.35, 0, 0.3),
            scale=0.05,
            text_fg=(0.4, 0.8, 1.0, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(label)
        
        # Slider
        self.distance_slider = DirectSlider(
            range=(10.0, 100.0),
            value=self.physics.object_distance,
            pageSize=1,
            pos=(-1.35, 0, 0.18),
            scale=0.42,
            command=self._on_distance_change,
            frameColor=(0.2, 0.22, 0.25, 0.95),
            thumb_frameColor=(0.3, 0.7, 1.0, 1),
            relief=2
        )
        self.elements.append(self.distance_slider)
        
        # Value display
        self.distance_value = DirectLabel(
            text=f"{self.physics.object_distance:.1f} cm",
            pos=(-1.35, 0, 0.03),
            scale=0.055,
            text_fg=(1, 1, 1, 1),
            frameColor=(0.05, 0.12, 0.18, 0.95),
            pad=(0.35, 0.22),
            relief=2
        )
        self.elements.append(self.distance_value)
    
    def _create_lens_power_slider(self):
        # Panel - far left
        panel = DirectFrame(
            pos=(-1.35, 0, -0.3),
            frameSize=(-0.42, 0.42, -0.22, 0.22),
            frameColor=(0.12, 0.14, 0.18, 0.9)
        )
        self.elements.append(panel)
        
        # Label
        label = DirectLabel(
            text="LENS POWER (Diopters)",
            pos=(-1.35, 0, -0.15),
            scale=0.05,
            text_fg=(0.6, 1.0, 0.6, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(label)
        
        # Slider
        self.power_slider = DirectSlider(
            range=(self.physics.MIN_POWER, self.physics.MAX_POWER),
            value=self.physics.lens_power,
            pageSize=0.25,
            pos=(-1.35, 0, -0.27),
            scale=0.42,
            command=self._on_power_change,
            frameColor=(0.2, 0.22, 0.25, 0.95),
            thumb_frameColor=(0.5, 1.0, 0.5, 1),
            relief=2
        )
        self.elements.append(self.power_slider)
        
        # Value display
        self.power_value = DirectLabel(
            text=f"{self.physics.lens_power:+.2f} D",
            pos=(-1.35, 0, -0.42),
            scale=0.055,
            text_fg=(1, 1, 1, 1),
            frameColor=(0.08, 0.15, 0.08, 0.95),
            pad=(0.35, 0.22),
            relief=2
        )
        self.elements.append(self.power_value)
    
    def _create_age_slider(self):
        # Panel - far left
        panel = DirectFrame(
            pos=(-1.35, 0, -0.75),
            frameSize=(-0.42, 0.42, -0.22, 0.22),
            frameColor=(0.12, 0.14, 0.18, 0.9)
        )
        self.elements.append(panel)
        
        # Label
        label = DirectLabel(
            text="AGE (years)",
            pos=(-1.35, 0, -0.6),
            scale=0.05,
            text_fg=(1.0, 0.8, 0.6, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(label)
        
        # Slider
        self.age_slider = DirectSlider(
            range=(10, 80),
            value=self.physics.age,
            pageSize=5,
            pos=(-1.35, 0, -0.72),
            scale=0.42,
            command=self._on_age_change,
            frameColor=(0.2, 0.22, 0.25, 0.95),
            thumb_frameColor=(1.0, 0.7, 0.5, 1),
            relief=2
        )
        self.elements.append(self.age_slider)
        
        # Value display
        self.age_value = DirectLabel(
            text=f"{self.physics.age} years",
            pos=(-1.35, 0, -0.87),
            scale=0.055,
            text_fg=(1, 1, 1, 1),
            frameColor=(0.15, 0.10, 0.08, 0.95),
            pad=(0.35, 0.22),
            relief=2
        )
        self.elements.append(self.age_value)
    
    def _create_displays(self):
        # Display panel - far right
        panel = DirectFrame(
            pos=(1.35, 0, 0.45),
            frameSize=(-0.48, 0.48, -0.6, 0.4),
            frameColor=(0.08, 0.10, 0.13, 0.92)
        )
        self.elements.append(panel)
        
        # Title
        title = DirectLabel(
            text="DIAGNOSIS",
            pos=(1.35, 0, 0.75),
            scale=0.06,
            text_fg=(1, 1, 0.5, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(title)
        
        # Condition display
        cond_label = DirectLabel(
            text="Condition:",
            pos=(1.35, 0, 0.62),
            scale=0.045,
            text_fg=(0.8, 0.8, 0.8, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(cond_label)
        
        self.condition_display = DirectLabel(
            text="Normal",
            pos=(1.35, 0, 0.53),
            scale=0.065,
            text_fg=(0.5, 1.0, 0.5, 1),
            frameColor=(0.1, 0.15, 0.1, 0.95),
            pad=(0.45, 0.25),
            relief=2
        )
        self.elements.append(self.condition_display)
        
        # Required power
        req_label = DirectLabel(
            text="Required Power:",
            pos=(1.35, 0, 0.35),
            scale=0.045,
            text_fg=(0.8, 0.8, 0.8, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(req_label)
        
        self.required_power_display = DirectLabel(
            text="+0.00 D",
            pos=(1.35, 0, 0.26),
            scale=0.07,
            text_fg=(1, 1, 0.3, 1),
            frameColor=(0.15, 0.12, 0.05, 0.95),
            pad=(0.4, 0.25),
            relief=2
        )
        self.elements.append(self.required_power_display)
        
        # Lens type
        lens_label = DirectLabel(
            text="Lens Type:",
            pos=(1.35, 0, 0.08),
            scale=0.045,
            text_fg=(0.8, 0.8, 0.8, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(lens_label)
        
        self.lens_type_display = DirectLabel(
            text="None",
            pos=(1.35, 0, -0.01),
            scale=0.065,
            text_fg=(0.7, 0.7, 1.0, 1),
            frameColor=(0.08, 0.08, 0.15, 0.95),
            pad=(0.4, 0.25),
            relief=2
        )
        self.elements.append(self.lens_type_display)
        
        # Focus quality
        focus_label = DirectLabel(
            text="Focus Quality:",
            pos=(1.35, 0, -0.19),
            scale=0.055,
            text_fg=(0.8, 0.8, 0.8, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(focus_label)
        
        self.focus_display = DirectLabel(
            text="100%",
            pos=(1.35, 0, -0.28),
            scale=0.07,
            text_fg=(0.5, 1.0, 0.5, 1),
            frameColor=(0.08, 0.15, 0.08, 0.95),
            pad=(0.35, 0.25),
            relief=2
        )
        self.elements.append(self.focus_display)
    
    def _create_preset_buttons(self):
        # Preset panel - far right
        panel = DirectFrame(
            pos=(1.35, 0, -0.6),
            frameSize=(-0.48, 0.48, -0.35, 0.12),
            frameColor=(0.08, 0.10, 0.13, 0.92)
        )
        self.elements.append(panel)
        
        title = DirectLabel(
            text="PATIENT PRESETS",
            pos=(1.35, 0, -0.42),
            scale=0.05,
            text_fg=(0.7, 0.9, 1.0, 1),
            frameColor=(0, 0, 0, 0)
        )
        self.elements.append(title)
        
        presets = [
            ("Normal Vision", "normal", -0.53, (0.3, 0.6, 0.3, 0.9)),
            ("Mild Myopia", "mild_myopia", -0.63, (0.6, 0.4, 0.6, 0.9)),
            ("Moderate Myopia", "moderate_myopia", -0.73, (0.7, 0.3, 0.5, 0.9)),
            ("Mild Hyperopia", "mild_hyperopia", -0.83, (0.4, 0.5, 0.7, 0.9)),
            ("Presbyopia", "presbyopia", -0.93, (0.8, 0.6, 0.4, 0.9))
        ]
        
        for label, preset, y_pos, color in presets:
            button = DirectButton(
                text=label,
                pos=(1.35, 0, y_pos),
                scale=0.042,
                command=self._on_preset_click,
                extraArgs=[preset],
                frameColor=color,
                text_fg=(1, 1, 1, 1),
                relief=2,
                pressEffect=1,
                pad=(0.25, 0.12)
            )
            self.elements.append(button)
    
    def _create_info_panel(self):
        # Create panel positioned behind the formula text
        panel = DirectFrame(
            pos=(0, 0, -0.82),  
            frameSize=(-0.65, 0.65, -0.05, 0.05), 
            frameColor=(0.1, 0.1, 0.15, 0.85)
        )
        self.elements.append(panel)
        
        formula = OnscreenText(
            text="Lens Formula: 1/f = 1/v - 1/u  |  Power (D) = 1/f (meters)",
            pos=(0, -0.83),
            scale=0.045,
            fg=(0.9, 0.9, 0.6, 1),
            align=TextNode.ACenter,
            mayChange=False
        )
        self.elements.append(formula)
        
    def _on_near_point_change(self):
        self.physics.near_point = self.near_point_slider['value']
        self.update_displays()
        self.update_callback()
    
    def _on_distance_change(self):
        self.physics.object_distance = self.distance_slider['value']
        self.update_displays()
        self.update_callback()
    
    def _on_power_change(self):
        self.physics.lens_power = self.power_slider['value']
        self.update_displays()
        self.update_callback()
    
    def _on_age_change(self):
        self.physics.age = int(self.age_slider['value'])
        self.near_point_slider['value'] = self.physics.near_point
        self.update_displays()
        self.update_callback()
    
    def _on_preset_click(self, preset_name):
        if self.physics.set_preset(preset_name):
            self.near_point_slider['value'] = self.physics.near_point
            self.age_slider['value'] = self.physics.age
            self.distance_slider['value'] = self.physics.object_distance
            self.power_slider['value'] = 0.0
            self.physics.lens_power = 0.0
            self.update_displays()
            self.update_callback()
    
    def update_displays(self):
        status = self.physics.get_status_text()
        
        self.near_point_value['text'] = f"{status['near_point']} cm"
        self.distance_value['text'] = f"{status['object_distance']} cm"
        self.power_value['text'] = f"{status['current_power']} D"
        self.age_value['text'] = f"{status['age']} years"
        
        condition = status['condition']
        self.condition_display['text'] = condition
        
        if condition == 'Normal':
            self.condition_display['text_fg'] = (1.5, 1.0, 0.5, 1)
        elif condition == 'Myopia':
            self.condition_display['text_fg'] = (1.0, 0.6, 0.8, 1)
        elif condition == 'Hyperopia':
            self.condition_display['text_fg'] = (0.6, 0.8, 1.0, 1)
        else:
            self.condition_display['text_fg'] = (1.0, 0.8, 0.6, 1)
        
        self.required_power_display['text'] = f"{status['required_power']} D"
        self.lens_type_display['text'] = status['lens_type']
        
        focus = float(status['focus_quality'])
        self.focus_display['text'] = f"{focus:.0f}%"
        
        if focus > 80:
            self.focus_display['text_fg'] = (0.5, 1.0, 0.5, 1)
        elif focus > 50:
            self.focus_display['text_fg'] = (1.0, 1.0, 0.5, 1)
        else:
            self.focus_display['text_fg'] = (1.0, 0.5, 0.5, 1)
    
    def cleanup(self):
        for element in self.elements:
            element.destroy()
        self.elements.clear()