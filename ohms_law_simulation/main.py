#!/usr/bin/env python3
"""
Ohm's Law Interactive 3D Simulation
Main entry point for the educational physics simulation

Author: Interactive Physics Education
Description: Visual demonstration of V = I * R using Panda3D
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    AmbientLight, DirectionalLight, 
    Vec3, Vec4, Point3,
    WindowProperties, loadPrcFileData,
    ClockObject
)
import sys
import math

from simulation.physics import OhmsLawPhysics
from simulation.circuit import Circuit
from simulation.ui import SimulationUI, HelpOverlay


# Configure Panda3D settings before importing ShowBase
loadPrcFileData("", """
    window-title Ohm's Law Interactive Simulation
    win-size 1280 720
    framebuffer-multisample 1
    multisamples 2
    show-frame-rate-meter false
    sync-video true
""")


class OhmsLawSimulation(ShowBase):
    """
    Main simulation class that orchestrates all components.
    Handles initialization, update loop, and user interaction.
    """
    
    def __init__(self):
        """Initialize the simulation"""
        super().__init__()
        
        # Disable default camera controls
        self.disableMouse()
        
        # Camera control state
        self.camera_distance = 15.0
        self.camera_heading = 0.0  # Horizontal rotation
        self.camera_pitch = -20.0  # Vertical rotation
        self.mouse_drag_active = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        # Movement speed
        self.move_speed = 0.5
        self.rotate_speed = 2.0
        
        # Initialize physics engine
        self.physics = OhmsLawPhysics(voltage=12.0, resistance=10.0)
        
        # Setup scene
        self._setup_camera()
        self._setup_lights()
        self._setup_background()
        
        # Enable FPS meter
        self.setFrameRateMeter(True)
        
        # Create circuit visualization
        self.circuit = Circuit(self.render)
        
        # Create UI
        self.ui = SimulationUI(self.physics, self.on_parameters_changed)
        
        # Create help overlay
        self.help_overlay = HelpOverlay()
        
        # Setup input handlers
        self._setup_input()
        
        # Add update task
        self.taskMgr.add(self.update_simulation, "update_simulation")
        self.taskMgr.add(self.update_camera, "update_camera")
        
        # Initial update
        self.on_parameters_changed()
        self._update_camera_position()
        
        print("=" * 60)
        print("Ohm's Law Interactive Simulation")
        print("=" * 60)
        print("Controls:")
        print("  MOUSE DRAG: Click and drag to orbit camera")
        print("  WASD: Free movement in 3D space")
        print("  Q/E: Move up/down")
        print("  ARROW KEYS: Orbit around circuit")
        print("  MOUSE WHEEL / +/-: Zoom in/out")
        print("  1-5: Quick presets")
        print("  H: Toggle help")
        print("  F: Toggle wireframe")
        print("  R: Reset simulation")
        print("  ESC: Exit")
        print("=" * 60)
        print(f"Initial State: {self.physics}")
        print("=" * 60)
    
    def _setup_camera(self):
        """Configure camera position and orientation"""
        # Initial camera setup - will be controlled dynamically
        self.camera.setPos(0, -15, 3)
        self.camera.lookAt(0, 0, 0)
        
        # Set camera field of view
        self.camLens.setFov(60)
    
    def _setup_lights(self):
        """Create lighting for the 3D scene"""
        # Ambient light for overall illumination
        ambient = AmbientLight('ambient_light')
        ambient.setColor(Vec4(0.4, 0.4, 0.45, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)
        
        # Directional light (main light source)
        directional = DirectionalLight('directional_light')
        directional.setColor(Vec4(0.8, 0.8, 0.75, 1))
        directional_np = self.render.attachNewNode(directional)
        directional_np.setHpr(45, -45, 0)
        self.render.setLight(directional_np)
        
        # Secondary directional light for better visibility
        directional2 = DirectionalLight('directional_light_2')
        directional2.setColor(Vec4(0.4, 0.4, 0.45, 1))
        directional2_np = self.render.attachNewNode(directional2)
        directional2_np.setHpr(-45, -30, 0)
        self.render.setLight(directional2_np)
    
    def _setup_background(self):
        """Set background color"""
        # Dark blue-gray background for better contrast
        self.setBackgroundColor(0.1, 0.12, 0.15)
    
    def _setup_input(self):
        """Setup keyboard and mouse input handlers"""
        # ESC key to exit
        self.accept('escape', self.exit_simulation)
        
        # H key to toggle help
        self.accept('h', self.help_overlay.toggle)
        
        # R key to reset to defaults
        self.accept('r', self.reset_simulation)
        
        # F key to toggle wireframe
        self.accept('f', self.toggle_wireframe)
        
        # Number keys for quick presets
        self.accept('1', lambda: self._quick_preset('normal'))
        self.accept('2', lambda: self._quick_preset('high_current'))
        self.accept('3', lambda: self._quick_preset('low_current'))
        self.accept('4', lambda: self._quick_preset('short_circuit'))
        self.accept('5', lambda: self._quick_preset('open_circuit'))
        
        # WASD for free camera movement
        self.accept('w', self.set_key, ['forward', True])
        self.accept('w-up', self.set_key, ['forward', False])
        self.accept('s', self.set_key, ['backward', True])
        self.accept('s-up', self.set_key, ['backward', False])
        self.accept('a', self.set_key, ['left', True])
        self.accept('a-up', self.set_key, ['left', False])
        self.accept('d', self.set_key, ['right', True])
        self.accept('d-up', self.set_key, ['right', False])
        
        # Q/E for up/down
        self.accept('q', self.set_key, ['down', True])
        self.accept('q-up', self.set_key, ['down', False])
        self.accept('e', self.set_key, ['up', True])
        self.accept('e-up', self.set_key, ['up', False])
        
        # Arrow keys for orbit
        self.accept('arrow_left', self.set_key, ['orbit_left', True])
        self.accept('arrow_left-up', self.set_key, ['orbit_left', False])
        self.accept('arrow_right', self.set_key, ['orbit_right', True])
        self.accept('arrow_right-up', self.set_key, ['orbit_right', False])
        self.accept('arrow_up', self.set_key, ['orbit_up', True])
        self.accept('arrow_up-up', self.set_key, ['orbit_up', False])
        self.accept('arrow_down', self.set_key, ['orbit_down', True])
        self.accept('arrow_down-up', self.set_key, ['orbit_down', False])
        
        # Camera zoom with mouse wheel or +/- keys
        self.accept('wheel_up', self.zoom_in)
        self.accept('wheel_down', self.zoom_out)
        self.accept('+', self.zoom_in)
        self.accept('=', self.zoom_in)
        self.accept('-', self.zoom_out)
        self.accept('_', self.zoom_out)
        
        # Mouse drag for camera orbit
        self.accept('mouse1', self.start_mouse_drag)
        self.accept('mouse1-up', self.stop_mouse_drag)
        
        # Initialize key state
        self.keys = {
            'forward': False, 'backward': False,
            'left': False, 'right': False,
            'up': False, 'down': False,
            'orbit_left': False, 'orbit_right': False,
            'orbit_up': False, 'orbit_down': False
        }
    
    def set_key(self, key, value):
        """Set key state for continuous movement"""
        self.keys[key] = value
    
    def start_mouse_drag(self):
        """Start mouse drag for camera orbit"""
        if self.mouseWatcherNode.hasMouse():
            self.mouse_drag_active = True
            self.last_mouse_x = self.mouseWatcherNode.getMouseX()
            self.last_mouse_y = self.mouseWatcherNode.getMouseY()
    
    def stop_mouse_drag(self):
        """Stop mouse drag"""
        self.mouse_drag_active = False
    
    def toggle_wireframe(self):
        """Toggle wireframe rendering"""
        self.render.toggleWireframe()
    
    def update_camera(self, task):
        """Update camera position based on input"""
        dt = self.taskMgr.globalClock.getDt()
        
        # Mouse drag orbit
        if self.mouse_drag_active and self.mouseWatcherNode.hasMouse():
            mouse_x = self.mouseWatcherNode.getMouseX()
            mouse_y = self.mouseWatcherNode.getMouseY()
            
            dx = mouse_x - self.last_mouse_x
            dy = mouse_y - self.last_mouse_y
            
            self.camera_heading -= dx * 100.0
            self.camera_pitch += dy * 100.0
            
            # Clamp pitch
            self.camera_pitch = max(-89, min(89, self.camera_pitch))
            
            self.last_mouse_x = mouse_x
            self.last_mouse_y = mouse_y
        
        # Arrow key orbit
        if self.keys['orbit_left']:
            self.camera_heading -= self.rotate_speed
        if self.keys['orbit_right']:
            self.camera_heading += self.rotate_speed
        if self.keys['orbit_up']:
            self.camera_pitch += self.rotate_speed
            self.camera_pitch = min(89, self.camera_pitch)
        if self.keys['orbit_down']:
            self.camera_pitch -= self.rotate_speed
            self.camera_pitch = max(-89, self.camera_pitch)
        
        # WASD free movement
        forward_vec = self.camera.getMat().getRow3(1)
        right_vec = self.camera.getMat().getRow3(0)
        up_vec = Vec3(0, 0, 1)
        
        if self.keys['forward']:
            self.camera.setPos(self.camera.getPos() + forward_vec * self.move_speed)
        if self.keys['backward']:
            self.camera.setPos(self.camera.getPos() - forward_vec * self.move_speed)
        if self.keys['left']:
            self.camera.setPos(self.camera.getPos() - right_vec * self.move_speed)
        if self.keys['right']:
            self.camera.setPos(self.camera.getPos() + right_vec * self.move_speed)
        if self.keys['up']:
            self.camera.setPos(self.camera.getPos() + up_vec * self.move_speed)
        if self.keys['down']:
            self.camera.setPos(self.camera.getPos() - up_vec * self.move_speed)
        
        # Update camera orientation
        self._update_camera_position()
        
        return task.cont
    
    def _update_camera_position(self):
        """Update camera position based on heading, pitch, and distance"""
        import math
        
        # Convert to radians
        h_rad = math.radians(self.camera_heading)
        p_rad = math.radians(self.camera_pitch)
        
        # Calculate spherical coordinates
        x = self.camera_distance * math.cos(p_rad) * math.sin(h_rad)
        y = -self.camera_distance * math.cos(p_rad) * math.cos(h_rad)
        z = self.camera_distance * math.sin(p_rad)
        
        # Only update if not using WASD (preserve free movement)
        if not any([self.keys['forward'], self.keys['backward'], 
                   self.keys['left'], self.keys['right'],
                   self.keys['up'], self.keys['down']]):
            self.camera.setPos(x, y, z)
        
        # Always look at origin
        self.camera.lookAt(0, 0, 0)
    
    def _quick_preset(self, preset_name):
        """
        Apply preset and update UI.
        
        Args:
            preset_name (str): Name of preset to apply
        """
        if self.physics.set_preset(preset_name):
            # Update UI sliders
            self.ui.voltage_slider['value'] = self.physics.voltage
            self.ui.resistance_slider['value'] = self.physics.resistance
            self.ui.update_displays()
            self.on_parameters_changed()
            print(f"Applied preset: {preset_name} - {self.physics}")
    
    def on_parameters_changed(self):
        """
        Callback when voltage or resistance changes.
        Updates circuit visualization.
        """
        # Update circuit with new values
        self.circuit.update(
            self.physics.voltage,
            self.physics.resistance,
            self.physics.current,
            self.physics.MAX_VOLTAGE,
            self.physics.MAX_RESISTANCE
        )
    
    def update_simulation(self, task):
        """
        Main update loop called every frame.
        
        Args:
            task: Panda3D task object
        
        Returns:
            Task.cont to continue running
        """
        # Update UI displays (in case physics changed elsewhere)
        self.ui.update_displays()
        
        # Continue running
        return task.cont
    
    def reset_simulation(self):
        """Reset simulation to default values"""
        self.physics.voltage = 12.0
        self.physics.resistance = 10.0
        self.ui.voltage_slider['value'] = self.physics.voltage
        self.ui.resistance_slider['value'] = self.physics.resistance
        self.ui.update_displays()
        self.on_parameters_changed()
        
        # Reset camera
        self.camera_distance = 15.0
        self.camera_heading = 0.0
        self.camera_pitch = -20.0
        self._update_camera_position()
        
        print(f"Reset to defaults: {self.physics}")
    
    def zoom_in(self):
        """Zoom camera in"""
        self.camera_distance = max(5.0, self.camera_distance - 1.0)
        self._update_camera_position()
    
    def zoom_out(self):
        """Zoom camera out"""
        self.camera_distance = min(30.0, self.camera_distance + 1.0)
        self._update_camera_position()
    
    def exit_simulation(self):
        """Clean up and exit"""
        print("\n" + "=" * 60)
        print("Exiting Ohm's Law Simulation")
        print(f"Final State: {self.physics}")
        print("=" * 60)
        
        # Cleanup
        self.circuit.cleanup()
        self.ui.cleanup()
        self.help_overlay.cleanup()
        
        # Exit
        sys.exit(0)


def main():
    """Main entry point"""
    try:
        app = OhmsLawSimulation()
        app.run()
    except Exception as e:
        print(f"\nError running simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()