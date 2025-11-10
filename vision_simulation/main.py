"""
Vision & Eyeglass Power Simulation
Educational tool demonstrating optical physics of corrective lenses
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    DirectionalLight, AmbientLight, PointLight,
    WindowProperties, AntialiasAttrib, Vec3, ClockObject
)
from direct.task import Task
from simulation.physics import VisionPhysics
from simulation.optical_components import VisionScene
from simulation.ui import VisionUI
import math


class VisionSimulation(ShowBase):
    """Main application for vision simulation"""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        # Camera control state (initialize BEFORE setup_camera)
        self.camera_distance = 18.0  # Farther back for better overview
        self.camera_heading = 25.0  # Slight angle for depth
        self.camera_pitch = 15.0  # Looking slightly down
        self.camera_velocity = Vec3(0, 0, 0)
        self.camera_speed = 0.12
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.mouse_dragging = False
        
        # Configuration
        self.setup_window()
        self.setup_lights()
        self.setup_camera()
        
        # Physics and scene
        self.physics = VisionPhysics()
        self.scene = VisionScene(self.render, self.physics)
        
        # UI
        self.ui = VisionUI(self.physics, self.on_physics_update, self)
        
        # Setup controls
        self.setup_input()
        
        # Initialize scene
        self.update_scene()
        self.ui.update_displays()
        
        # Add update task
        self.taskMgr.add(self.update_camera, "update_camera")
        
        # FPS meter
        self.setFrameRateMeter(True)
        
        print("\n" + "="*70)
        print("Vision & Eyeglass Power Simulation - Ready!")
        print("="*70)
        print("\nCONTROLS:")
        print("  Mouse Drag: Orbit around scene")
        print("  Scroll Wheel: Zoom in/out")
        print("  WASD: Free movement in 3D space")
        print("  Q/E: Move down/up")
        print("  Arrow Keys: Precise rotation")
        print("  F: Toggle wireframe mode")
        print("  ESC: Exit simulation")
        print("\nUI CONTROLS:")
        print("  Near Point: Minimum clear vision distance")
        print("  Object Distance: Distance to viewed object")
        print("  Lens Power: Corrective lens strength (diopters)")
        print("  Age: Patient age (affects near point)")
        print("  Presets: Load common vision conditions")
        print("\nOPTICAL CONCEPTS:")
        print("  • Myopia (nearsighted): Distant objects blurry → Concave lens")
        print("  • Hyperopia (farsighted): Close objects blurry → Convex lens")
        print("  • Presbyopia: Age-related near vision loss → Reading glasses")
        print("  • Lens formula: 1/f = 1/v - 1/u")
        print("="*70 + "\n")
    
    def setup_window(self):
        """Configure window properties"""
        props = WindowProperties()
        props.setTitle("Vision & Eyeglass Power Simulation")
        props.setSize(1600, 900)
        self.win.requestProperties(props)
        
        # Enable antialiasing
        self.render.setAntialias(AntialiasAttrib.MAuto)
        
        # Set background color (lighter, more neutral)
        self.setBackgroundColor(0.22, 0.25, 0.30)  # Lighter blue-gray
    
    def setup_lights(self):
        """Setup bright, clear scene lighting"""
        # Brighter ambient light for better visibility
        ambient = AmbientLight("ambient")
        ambient.setColor((0.5, 0.5, 0.55, 1))  # Brighter
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)
        
        # Strong key light (main)
        key_light = DirectionalLight("key_light")
        key_light.setColor((1.0, 1.0, 0.95, 1))  # Bright white
        key_np = self.render.attachNewNode(key_light)
        key_np.setHpr(45, -50, 0)
        self.render.setLight(key_np)
        
        # Strong fill light from opposite side
        fill_light = DirectionalLight("fill_light")
        fill_light.setColor((0.7, 0.7, 0.75, 1))  # Brighter fill
        fill_np = self.render.attachNewNode(fill_light)
        fill_np.setHpr(-45, -30, 0)
        self.render.setLight(fill_np)
        
        # Rim light from behind
        rim_light = DirectionalLight("rim_light")
        rim_light.setColor((0.5, 0.55, 0.6, 1))  # Brighter rim
        rim_np = self.render.attachNewNode(rim_light)
        rim_np.setHpr(180, -20, 0)
        self.render.setLight(rim_np)
        
        # Bright point light for eye detail
        point_light = PointLight("point_light")
        point_light.setColor((0.8, 0.8, 0.9, 1))  # Brighter
        point_np = self.render.attachNewNode(point_light)
        point_np.setPos(3, -6, 4)
        self.render.setLight(point_np)
        
        # Additional point light from front
        front_light = PointLight("front_light")
        front_light.setColor((0.6, 0.6, 0.7, 1))
        front_np = self.render.attachNewNode(front_light)
        front_np.setPos(0, -8, 2)
        self.render.setLight(front_np)
    
    def setup_camera(self):
        """Configure initial camera position"""
        self.update_camera_position()
    
    def setup_input(self):
        """Setup keyboard and mouse controls"""
        # Keyboard
        self.accept("escape", self.userExit)
        self.accept("f", self.toggle_wireframe)
        
        # Camera movement
        self.accept("w", self.set_camera_velocity, [Vec3(0, 1, 0)])
        self.accept("w-up", self.clear_camera_velocity, [Vec3(0, 1, 0)])
        self.accept("s", self.set_camera_velocity, [Vec3(0, -1, 0)])
        self.accept("s-up", self.clear_camera_velocity, [Vec3(0, -1, 0)])
        self.accept("a", self.set_camera_velocity, [Vec3(-1, 0, 0)])
        self.accept("a-up", self.clear_camera_velocity, [Vec3(-1, 0, 0)])
        self.accept("d", self.set_camera_velocity, [Vec3(1, 0, 0)])
        self.accept("d-up", self.clear_camera_velocity, [Vec3(1, 0, 0)])
        self.accept("q", self.set_camera_velocity, [Vec3(0, 0, -1)])
        self.accept("q-up", self.clear_camera_velocity, [Vec3(0, 0, -1)])
        self.accept("e", self.set_camera_velocity, [Vec3(0, 0, 1)])
        self.accept("e-up", self.clear_camera_velocity, [Vec3(0, 0, 1)])
        
        # Arrow keys for precise rotation
        self.accept("arrow_left", self.rotate_camera, [-5, 0])
        self.accept("arrow_right", self.rotate_camera, [5, 0])
        self.accept("arrow_up", self.rotate_camera, [0, 5])
        self.accept("arrow_down", self.rotate_camera, [0, -5])
        
        # Mouse
        self.accept("mouse1", self.start_mouse_drag)
        self.accept("mouse1-up", self.stop_mouse_drag)
        self.accept("wheel_up", self.zoom_camera, [-1.0])
        self.accept("wheel_down", self.zoom_camera, [1.0])
    
    def toggle_wireframe(self):
        """Toggle wireframe rendering"""
        if self.render.hasRenderMode():
            self.render.clearRenderMode()
        else:
            self.render.setRenderModeWireframe()
    
    def set_camera_velocity(self, direction):
        """Add to camera velocity"""
        self.camera_velocity += direction
    
    def clear_camera_velocity(self, direction):
        """Remove from camera velocity"""
        self.camera_velocity -= direction
    
    def rotate_camera(self, heading_change, pitch_change):
        """Rotate camera by specific amounts"""
        self.camera_heading += heading_change
        self.camera_pitch = max(-89, min(89, self.camera_pitch + pitch_change))
        self.update_camera_position()
    
    def start_mouse_drag(self):
        """Start mouse drag for orbit control"""
        if self.mouseWatcherNode.hasMouse():
            self.mouse_dragging = True
            self.last_mouse_x = self.mouseWatcherNode.getMouseX()
            self.last_mouse_y = self.mouseWatcherNode.getMouseY()
    
    def stop_mouse_drag(self):
        """Stop mouse drag"""
        self.mouse_dragging = False
    
    def zoom_camera(self, delta):
        """Zoom camera in/out"""
        self.camera_distance = max(5, min(40, self.camera_distance + delta))
        self.update_camera_position()
    
    def update_camera(self, task):
        """Update camera every frame"""
        dt = self.taskMgr.globalClock.getDt()
        
        # Handle mouse drag
        if self.mouse_dragging and self.mouseWatcherNode.hasMouse():
            mouse_x = self.mouseWatcherNode.getMouseX()
            mouse_y = self.mouseWatcherNode.getMouseY()
            
            dx = mouse_x - self.last_mouse_x
            dy = mouse_y - self.last_mouse_y
            
            self.camera_heading -= dx * 80
            self.camera_pitch = max(-89, min(89, self.camera_pitch + dy * 80))
            
            self.last_mouse_x = mouse_x
            self.last_mouse_y = mouse_y
        
        # Handle WASD movement
        if self.camera_velocity.length() > 0:
            # Get camera direction vectors
            heading_rad = math.radians(self.camera_heading)
            pitch_rad = math.radians(self.camera_pitch)
            
            forward = Vec3(
                math.sin(heading_rad),
                math.cos(heading_rad),
                0
            )
            right = Vec3(
                math.cos(heading_rad),
                -math.sin(heading_rad),
                0
            )
            up = Vec3(0, 0, 1)
            
            # Calculate movement
            move = (
                forward * self.camera_velocity.y +
                right * self.camera_velocity.x +
                up * self.camera_velocity.z
            ) * self.camera_speed
            
            # Update camera position
            current_pos = self.camera.getPos()
            self.camera.setPos(current_pos + move)
        else:
            # Update orbital camera position
            self.update_camera_position()
        
        return Task.cont
    
    def update_camera_position(self):
        """Update camera position based on spherical coordinates"""
        # Convert to radians
        heading_rad = math.radians(self.camera_heading)
        pitch_rad = math.radians(self.camera_pitch)
        
        # Calculate position
        x = self.camera_distance * math.cos(pitch_rad) * math.sin(heading_rad)
        y = -self.camera_distance * math.cos(pitch_rad) * math.cos(heading_rad)
        z = self.camera_distance * math.sin(pitch_rad)
        
        self.camera.setPos(x, y, z)
        self.camera.lookAt(0, 0, 0)
    
    def on_physics_update(self):
        """Called when physics parameters change"""
        self.update_scene()
    
    def update_scene(self):
        """Update 3D scene based on physics"""
        # Get current status
        status = self.physics.get_status_text()
        
        # Update corrective lens power and position
        lens_power = self.physics.lens_power
        object_distance_cm = self.physics.object_distance
        
        # Position lens between eye and object
        lens_distance = -2.5  # cm in front of eye
        
        self.scene.update_corrective_lens(lens_power, lens_distance)
        
        # Update test object position
        object_pos = -object_distance_cm / 10.0  # Convert to simulation units
        self.scene.update_object_distance(object_pos)
        
        # Update light rays based on focus quality
        focus_quality = float(status['focus_quality'])
        self.scene.update_light_rays(focus_quality)


def main():
    """Entry point for vision simulation"""
    app = VisionSimulation()
    app.run()


if __name__ == "__main__":
    main()
