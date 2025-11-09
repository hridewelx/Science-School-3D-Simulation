"""
Circuit Components Module
Creates all 3D visual elements using Panda3D geometric primitives
"""

from panda3d.core import (
    NodePath, GeomNode, CardMaker,
    LineSegs, Vec3, Vec4, Point3,
    Geom, GeomVertexFormat, GeomVertexData, GeomVertexWriter,
    GeomTriangles, GeomLines
)
from direct.interval.IntervalGlobal import Sequence, LerpPosInterval, Wait
import random
import math


def create_box(width=1.0, height=1.0, depth=1.0):
    """Create a box geometry programmatically"""
    format = GeomVertexFormat.getV3n3c4()
    vdata = GeomVertexData('box', format, Geom.UHStatic)
    
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    
    # Define 8 vertices of the box
    w, h, d = width/2, height/2, depth/2
    vertices = [
        (-w, -h, -d), (w, -h, -d), (w, h, -d), (-w, h, -d),  # back
        (-w, -h, d), (w, -h, d), (w, h, d), (-w, h, d)       # front
    ]
    
    # Define faces (each face is 2 triangles = 6 vertices)
    faces = [
        # back, front, right, left, top, bottom
        [0,1,2, 0,2,3], [4,6,5, 4,7,6], [1,5,6, 1,6,2],
        [0,3,7, 0,7,4], [3,2,6, 3,6,7], [0,4,5, 0,5,1]
    ]
    
    normals = [
        (0,0,-1), (0,0,1), (1,0,0), (-1,0,0), (0,1,0), (0,-1,0)
    ]
    
    prim = GeomTriangles(Geom.UHStatic)
    
    for face_idx, face in enumerate(faces):
        for idx in face:
            vertex.addData3f(*vertices[idx])
            normal.addData3f(*normals[face_idx])
            color.addData4f(1, 1, 1, 1)
    
    for i in range(len(faces) * 6):
        prim.addVertex(i)
    
    geom = Geom(vdata)
    geom.addPrimitive(prim)
    
    node = GeomNode('box')
    node.addGeom(geom)
    
    return NodePath(node)


def create_sphere(radius=0.5, segments=16):
    """Create a sphere geometry programmatically"""
    format = GeomVertexFormat.getV3n3c4()
    vdata = GeomVertexData('sphere', format, Geom.UHStatic)
    
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    
    prim = GeomTriangles(Geom.UHStatic)
    
    # Create vertices
    for lat in range(segments):
        lat0 = math.pi * (-0.5 + float(lat) / segments)
        z0 = radius * math.sin(lat0)
        zr0 = radius * math.cos(lat0)
        
        lat1 = math.pi * (-0.5 + float(lat + 1) / segments)
        z1 = radius * math.sin(lat1)
        zr1 = radius * math.cos(lat1)
        
        for lon in range(segments):
            lon0 = 2 * math.pi * float(lon) / segments
            x0 = math.cos(lon0)
            y0 = math.sin(lon0)
            
            lon1 = 2 * math.pi * float(lon + 1) / segments
            x1 = math.cos(lon1)
            y1 = math.sin(lon1)
            
            # First triangle
            vertex.addData3f(x0 * zr0, y0 * zr0, z0)
            normal.addData3f(x0, y0, z0 / radius)
            color.addData4f(1, 1, 1, 1)
            
            vertex.addData3f(x1 * zr0, y1 * zr0, z0)
            normal.addData3f(x1, y1, z0 / radius)
            color.addData4f(1, 1, 1, 1)
            
            vertex.addData3f(x1 * zr1, y1 * zr1, z1)
            normal.addData3f(x1, y1, z1 / radius)
            color.addData4f(1, 1, 1, 1)
            
            # Second triangle
            vertex.addData3f(x0 * zr0, y0 * zr0, z0)
            normal.addData3f(x0, y0, z0 / radius)
            color.addData4f(1, 1, 1, 1)
            
            vertex.addData3f(x1 * zr1, y1 * zr1, z1)
            normal.addData3f(x1, y1, z1 / radius)
            color.addData4f(1, 1, 1, 1)
            
            vertex.addData3f(x0 * zr1, y0 * zr1, z1)
            normal.addData3f(x0, y0, z1 / radius)
            color.addData4f(1, 1, 1, 1)
    
    num_vertices = segments * segments * 6
    for i in range(num_vertices):
        prim.addVertex(i)
    
    geom = Geom(vdata)
    geom.addPrimitive(prim)
    
    node = GeomNode('sphere')
    node.addGeom(geom)
    
    return NodePath(node)


class CircuitComponent:
    """Base class for all circuit components"""
    
    def __init__(self, parent_node):
        """
        Initialize component.
        
        Args:
            parent_node: Panda3D NodePath to attach this component to
        """
        self.node = parent_node.attachNewNode("component")
    
    def set_position(self, x, y, z):
        """Set component position"""
        self.node.setPos(x, y, z)
    
    def set_color(self, r, g, b, a=1.0):
        """Set component color"""
        self.node.setColor(r, g, b, a)
    
    def show(self):
        """Show component"""
        self.node.show()
    
    def hide(self):
        """Hide component"""
        self.node.hide()
    
    def cleanup(self):
        """Remove component from scene"""
        self.node.removeNode()


class Battery(CircuitComponent):
    """Visual representation of a battery using geometric shapes"""
    
    def __init__(self, parent_node):
        """
        Create a battery component.
        
        Args:
            parent_node: Parent NodePath
        """
        super().__init__(parent_node)
        self._create_geometry()
    
    def _create_geometry(self):
        """Create battery from boxes (positive and negative terminals)"""
        # Main battery body (red box)
        self.body = create_box(0.8, 0.4, 0.5)
        self.body.reparentTo(self.node)
        self.body.setColor(0.9, 0.1, 0.1, 1.0)  # Red
        
        # Positive terminal (smaller red box)
        self.positive = create_box(0.15, 0.15, 0.15)
        self.positive.reparentTo(self.node)
        self.positive.setPos(0.5, 0, 0)
        self.positive.setColor(1.0, 0.3, 0.3, 1.0)
        
        # Negative terminal (smaller dark box)
        self.negative = create_box(0.15, 0.15, 0.15)
        self.negative.reparentTo(self.node)
        self.negative.setPos(-0.5, 0, 0)
        self.negative.setColor(0.3, 0.1, 0.1, 1.0)
        
        # Add voltage label indicator (yellow stripe)
        self.indicator = create_box(0.7, 0.35, 0.1)
        self.indicator.reparentTo(self.node)
        self.indicator.setPos(0, 0, 0.3)
        self.indicator.setColor(1.0, 1.0, 0.3, 1.0)
    
    def update_voltage_visual(self, voltage, max_voltage=50.0):
        """
        Update visual representation based on voltage.
        
        Args:
            voltage (float): Current voltage
            max_voltage (float): Maximum voltage for normalization
        """
        # Change indicator brightness based on voltage
        intensity = voltage / max_voltage
        self.indicator.setColor(intensity, intensity, 0.3, 1.0)


class Resistor(CircuitComponent):
    """Visual representation of a resistor using geometric shapes"""
    
    def __init__(self, parent_node):
        """
        Create a resistor component.
        
        Args:
            parent_node: Parent NodePath
        """
        super().__init__(parent_node)
        self._create_geometry()
    
    def _create_geometry(self):
        """Create resistor from boxes with color bands"""
        # Main resistor body (blue cylinder-like box)
        self.body = create_box(1.0, 0.3, 0.3)
        self.body.reparentTo(self.node)
        self.body.setColor(0.2, 0.4, 0.8, 1.0)  # Blue
        
        # Color bands for resistance indication
        self.band1 = create_box(0.1, 0.32, 0.32)
        self.band1.reparentTo(self.node)
        self.band1.setPos(-0.3, 0, 0)
        self.band1.setColor(0.8, 0.6, 0.2, 1.0)  # Gold
        
        self.band2 = create_box(0.1, 0.32, 0.32)
        self.band2.reparentTo(self.node)
        self.band2.setPos(0.3, 0, 0)
        self.band2.setColor(0.8, 0.6, 0.2, 1.0)  # Gold
        
        # End caps (connectors)
        self.cap1 = create_box(0.15, 0.15, 0.15)
        self.cap1.reparentTo(self.node)
        self.cap1.setPos(-0.6, 0, 0)
        self.cap1.setColor(0.5, 0.5, 0.5, 1.0)
        
        self.cap2 = create_box(0.15, 0.15, 0.15)
        self.cap2.reparentTo(self.node)
        self.cap2.setPos(0.6, 0, 0)
        self.cap2.setColor(0.5, 0.5, 0.5, 1.0)
    
    def update_resistance_visual(self, resistance, max_resistance=100.0):
        """
        Update visual representation based on resistance.
        
        Args:
            resistance (float): Current resistance
            max_resistance (float): Maximum resistance for normalization
        """
        # Change color bands based on resistance level
        intensity = resistance / max_resistance
        # Higher resistance = darker blue
        self.body.setColor(0.2, 0.4 * (1 - intensity * 0.5), 0.8, 1.0)


class Wire(CircuitComponent):
    """Visual representation of wires connecting components"""
    
    def __init__(self, parent_node, start_pos, end_pos):
        """
        Create a wire between two points.
        
        Args:
            parent_node: Parent NodePath
            start_pos (tuple): Starting (x, y, z) position
            end_pos (tuple): Ending (x, y, z) position
        """
        super().__init__(parent_node)
        self._create_wire(start_pos, end_pos)
    
    def _create_wire(self, start_pos, end_pos):
        """Create wire using line segments"""
        lines = LineSegs()
        lines.setThickness(3.0)
        lines.setColor(0.3, 0.3, 0.3, 1.0)  # Gray
        
        lines.moveTo(start_pos[0], start_pos[1], start_pos[2])
        lines.drawTo(end_pos[0], end_pos[1], end_pos[2])
        
        wire_node = lines.create()
        self.wire_path = self.node.attachNewNode(wire_node)
    
    def get_path_points(self, num_points=20):
        """
        Get interpolated points along the wire for electron flow.
        
        Args:
            num_points (int): Number of points to generate
        
        Returns:
            list: List of Vec3 points along the wire
        """
        # This would need start/end positions stored
        # For now, return empty list - will be enhanced
        return []


class Electron(CircuitComponent):
    """Visual representation of an electron particle"""
    
    def __init__(self, parent_node, position=(0, 0, 0)):
        """
        Create an electron particle.
        
        Args:
            parent_node: Parent NodePath
            position (tuple): Initial (x, y, z) position
        """
        super().__init__(parent_node)
        self._create_geometry()
        self.set_position(*position)
        self.animation_sequence = None
    
    def _create_geometry(self):
        """Create electron as a small yellow sphere"""
        self.sphere = create_sphere(0.08, 12)
        self.sphere.reparentTo(self.node)
        self.sphere.setColor(1.0, 1.0, 0.2, 1.0)  # Yellow
    
    def update_color(self, intensity):
        """
        Update electron color based on current intensity.
        
        Args:
            intensity (float): Color intensity (0-1)
        """
        brightness = 0.3 + 0.7 * intensity
        self.sphere.setColor(brightness, brightness, 0.2, 1.0)
    
    def animate_along_path(self, path_points, speed_factor=1.0):
        """
        Animate electron movement along a path.
        
        Args:
            path_points (list): List of Vec3 positions
            speed_factor (float): Speed multiplier
        """
        if not path_points or len(path_points) < 2:
            return
        
        # Stop any existing animation
        if self.animation_sequence:
            self.animation_sequence.finish()
        
        # Create animation sequence
        intervals = []
        duration_per_segment = 0.1 / speed_factor
        
        for i in range(len(path_points) - 1):
            interval = LerpPosInterval(
                self.node,
                duration_per_segment,
                path_points[i + 1],
                startPos=path_points[i]
            )
            intervals.append(interval)
        
        # Loop the animation
        self.animation_sequence = Sequence(*intervals)
        self.animation_sequence.loop()
    
    def stop_animation(self):
        """Stop electron animation"""
        if self.animation_sequence:
            self.animation_sequence.finish()
            self.animation_sequence = None


class Circuit:
    """Main circuit assembly containing all components"""
    
    def __init__(self, parent_node):
        """
        Create complete circuit visualization.
        
        Args:
            parent_node: Parent NodePath
        """
        self.parent = parent_node
        self.electrons = []
        self._create_circuit()
    
    def _create_circuit(self):
        """Assemble all circuit components"""
        # Create battery on the left
        self.battery = Battery(self.parent)
        self.battery.set_position(-3, 0, 0)
        
        # Create resistor on the right
        self.resistor = Resistor(self.parent)
        self.resistor.set_position(3, 0, 0)
        
        # Create wires connecting components
        # Top wire (battery positive to resistor)
        self.wire_top = Wire(
            self.parent,
            (-2.5, 0, 0.5),
            (2.4, 0, 0.5)
        )
        
        # Bottom wire (resistor to battery negative)
        self.wire_bottom = Wire(
            self.parent,
            (2.4, 0, -0.5),
            (-2.5, 0, -0.5)
        )
        
        # Create electron flow path
        self._create_electron_path()
        
        # Create initial electrons
        self._create_electrons(num_electrons=15)
    
    def _create_electron_path(self):
        """Define the path electrons will follow around the circuit"""
        self.electron_path = [
            Point3(-2.5, 0, 0.5),   # Start at battery positive
            Point3(-1, 0, 0.5),
            Point3(0, 0, 0.5),
            Point3(1, 0, 0.5),
            Point3(2.4, 0, 0.5),    # Enter resistor
            Point3(2.4, 0, 0.3),
            Point3(2.4, 0, 0),
            Point3(2.4, 0, -0.3),
            Point3(2.4, 0, -0.5),   # Exit resistor
            Point3(1, 0, -0.5),
            Point3(0, 0, -0.5),
            Point3(-1, 0, -0.5),
            Point3(-2.5, 0, -0.5),  # Back to battery negative
            Point3(-2.5, 0, -0.3),
            Point3(-2.5, 0, 0),
            Point3(-2.5, 0, 0.3),
            Point3(-2.5, 0, 0.5),   # Complete loop
        ]
    
    def _create_electrons(self, num_electrons=15):
        """
        Create electron particles distributed along the path.
        
        Args:
            num_electrons (int): Number of electrons to create
        """
        path_length = len(self.electron_path)
        
        for i in range(num_electrons):
            # Distribute electrons evenly along path
            path_index = int((i / num_electrons) * path_length)
            position = self.electron_path[path_index % path_length]
            
            electron = Electron(self.parent, position)
            self.electrons.append(electron)
    
    def update(self, voltage, resistance, current, max_voltage=50.0, max_resistance=100.0):
        """
        Update circuit visualization based on electrical parameters.
        
        Args:
            voltage (float): Current voltage
            resistance (float): Current resistance
            current (float): Calculated current
            max_voltage (float): Maximum voltage
            max_resistance (float): Maximum resistance
        """
        # Update battery appearance
        self.battery.update_voltage_visual(voltage, max_voltage)
        
        # Update resistor appearance
        self.resistor.update_resistance_visual(resistance, max_resistance)
        
        # Update electron flow
        self._update_electron_flow(current)
    
    def _update_electron_flow(self, current):
        """
        Update electron animation speed based on current.
        
        Args:
            current (float): Current in amperes
        """
        # Calculate speed factor (higher current = faster movement)
        speed_factor = 0.5 + (current * 0.3)
        
        # Calculate color intensity
        intensity = min(current / 50.0, 1.0)
        
        # Update each electron
        for i, electron in enumerate(self.electrons):
            # Update color
            electron.update_color(intensity)
            
            # Create path starting from different positions
            start_index = int((i / len(self.electrons)) * len(self.electron_path))
            rotated_path = (
                self.electron_path[start_index:] + 
                self.electron_path[:start_index]
            )
            
            # Animate along path
            electron.animate_along_path(rotated_path, speed_factor)
    
    def cleanup(self):
        """Clean up all circuit components"""
        self.battery.cleanup()
        self.resistor.cleanup()
        self.wire_top.cleanup()
        self.wire_bottom.cleanup()
        
        for electron in self.electrons:
            electron.cleanup()
        self.electrons.clear()
