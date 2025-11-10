"""
Eye Anatomy and Lens System Components
Creates 3D models of eye parts and corrective lenses
"""

from panda3d.core import (
    NodePath, GeomNode, LineSegs, TextNode,
    Vec3, Vec4, Point3,
    Geom, GeomVertexFormat, GeomVertexData, GeomVertexWriter,
    GeomTriangles, GeomLines
)
import math


def create_sphere(radius=0.5, segments=20):
    """Create a sphere geometry"""
    format = GeomVertexFormat.getV3n3c4()
    vdata = GeomVertexData('sphere', format, Geom.UHStatic)
    
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    
    prim = GeomTriangles(Geom.UHStatic)
    
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
            
            # Triangles
            vertices = [
                (x0 * zr0, y0 * zr0, z0, x0, y0, z0 / radius),
                (x1 * zr0, y1 * zr0, z0, x1, y1, z0 / radius),
                (x1 * zr1, y1 * zr1, z1, x1, y1, z1 / radius),
                (x0 * zr0, y0 * zr0, z0, x0, y0, z0 / radius),
                (x1 * zr1, y1 * zr1, z1, x1, y1, z1 / radius),
                (x0 * zr1, y0 * zr1, z1, x0, y0, z1 / radius)
            ]
            
            for vx, vy, vz, nx, ny, nz in vertices:
                vertex.addData3f(vx, vy, vz)
                normal.addData3f(nx, ny, nz)
                color.addData4f(1, 1, 1, 1)
    
    num_vertices = segments * segments * 6
    for i in range(num_vertices):
        prim.addVertex(i)
    
    geom = Geom(vdata)
    geom.addPrimitive(prim)
    
    node = GeomNode('sphere')
    node.addGeom(geom)
    
    return NodePath(node)


def create_disk(radius=0.5, segments=30):
    """Create a disk (filled circle)"""
    format = GeomVertexFormat.getV3n3c4()
    vdata = GeomVertexData('disk', format, Geom.UHStatic)
    
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    
    prim = GeomTriangles(Geom.UHStatic)
    
    # Center vertex
    vertex.addData3f(0, 0, 0)
    normal.addData3f(0, 0, 1)
    color.addData4f(1, 1, 1, 1)
    
    # Circle vertices
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertex.addData3f(x, y, 0)
        normal.addData3f(0, 0, 1)
        color.addData4f(1, 1, 1, 1)
    
    # Create triangles
    for i in range(segments):
        prim.addVertices(0, i + 1, i + 2)
    
    geom = Geom(vdata)
    geom.addPrimitive(prim)
    
    node = GeomNode('disk')
    node.addGeom(geom)
    
    return NodePath(node)


class EyeModel:
    """3D anatomical model of human eye - Clean and focused"""
    
    def __init__(self, parent_node):
        self.node = parent_node.attachNewNode("eye_model")
        self.node.setScale(1.8)
        self._create_eye()
    
    def _create_eye(self):
        """Build anatomically accurate eye components"""
        # Eyeball (sclera - white outer shell) - More transparent
        self.eyeball = create_sphere(1.0, 40)
        self.eyeball.reparentTo(self.node)
        self.eyeball.setColor(0.95, 0.95, 0.98, 0.25)  # Much more transparent
        self.eyeball.setTransparency(True)
        
        # Vitreous humor (clear gel filling the eye) - Very transparent
        self.vitreous = create_sphere(0.88, 32)
        self.vitreous.reparentTo(self.node)
        self.vitreous.setColor(0.8, 0.9, 1.0, 0.08)  # Nearly invisible
        self.vitreous.setTransparency(True)
        
        # Cornea (clear bulging front surface) - More transparent
        self.cornea = create_sphere(0.52, 28)
        self.cornea.reparentTo(self.node)
        self.cornea.setPos(0, 1.0, 0)
        self.cornea.setScale(1.05, 0.35, 1.05)
        self.cornea.setColor(0.7, 0.9, 1.0, 0.25)  # More transparent
        self.cornea.setTransparency(True)
        
        # Iris (colored muscle controlling pupil) - Keep opaque for visibility
        self.iris = create_disk(0.38, 48)
        self.iris.reparentTo(self.node)
        self.iris.setPos(0, 0.82, 0)
        self.iris.setH(90)
        self.iris.setColor(0.15, 0.35, 0.65, 1.0)
        
        # Pupil (opening in center of iris) - Keep opaque
        self.pupil = create_disk(0.15, 32)
        self.pupil.reparentTo(self.node)
        self.pupil.setPos(0, 0.83, 0)
        self.pupil.setH(90)
        self.pupil.setColor(0.05, 0.05, 0.1, 1.0)
        
        # Crystalline lens (flexible focusing element) - Semi-transparent
        self.crystalline_lens = create_sphere(0.32, 28)
        self.crystalline_lens.reparentTo(self.node)
        self.crystalline_lens.setPos(0, 0.55, 0)
        self.crystalline_lens.setScale(1.0, 0.5, 1.0)
        self.crystalline_lens.setColor(0.95, 0.92, 0.7, 0.35)  # More transparent
        self.crystalline_lens.setTransparency(True)
        
        # Retina (light-sensitive curved back surface) - Keep visible but transparent
        # Make it concave (curved inward) for anatomical accuracy
        self.retina = create_sphere(0.88, 32)
        self.retina.reparentTo(self.node)
        self.retina.setScale(1.0, 0.35, 1.0)  # Flatten to show only back portion
        self.retina.setPos(0, -0.7, 0)
        self.retina.setColor(0.95, 0.35, 0.35, 0.75)  # Slightly more transparent to see rays
        self.retina.setTransparency(True)
        
        # Fovea (central high-acuity spot on retina) - Keep visible
        self.fovea = create_disk(0.12, 24)
        self.fovea.reparentTo(self.node)
        self.fovea.setPos(0, -0.95, 0)
        self.fovea.setH(-90)
        self.fovea.setColor(0.85, 0.25, 0.25, 0.9)
        
        # Focal point indicator (shows where light converges) - Always visible
        self.focal_point = create_sphere(0.12, 20)  # Slightly larger for better visibility
        self.focal_point.reparentTo(self.node)
        self.focal_point.setPos(0, -0.95, 0)
        self.focal_point.setColor(1.0, 1.0, 0.4, 1.0)  # Bright yellow, fully opaque
        # Keep solid rendering - no transparency to avoid occlusion issues
        self.focal_point.setLightOff()  # Disable lighting for consistent brightness
        
        # Optic nerve (carries signals to brain) - Keep opaque
        self.optic_nerve = create_sphere(0.18, 20)
        self.optic_nerve.reparentTo(self.node)
        self.optic_nerve.setPos(0.25, -0.95, -0.15)
        self.optic_nerve.setScale(0.8, 0.6, 0.8)
        self.optic_nerve.setColor(0.9, 0.8, 0.5, 1.0)
    
    def set_position(self, x, y, z):
        self.node.setPos(x, y, z)
    
    def set_scale(self, scale):
        self.node.setScale(scale)
    
    def cleanup(self):
        self.node.removeNode()


class CorrectiveLens:
    """3D model of eyeglass lens - Simplified"""
    
    def __init__(self, parent_node, lens_type='convex'):
        self.node = parent_node.attachNewNode("corrective_lens")
        self.node.setScale(2.0)
        self.lens_type = lens_type
        self._create_lens()
    
    def _create_lens(self):
        """Create simplified lens geometry"""
        # Main lens disk only
        self.lens_disk = create_disk(1.0, 50)
        self.lens_disk.reparentTo(self.node)
        self.lens_disk.setH(90)
        self.lens_disk.setColor(0.7, 0.9, 1.0, 0.55)
        self.lens_disk.setTransparency(True)
    
    def set_position(self, x, y, z):
        self.node.setPos(x, y, z)
    
    def set_power_visual(self, power):
        # Simplified color changes
        intensity = min(abs(power) / 5.0, 1.0)
        alpha = 0.2 + (intensity * 0.4)
        
        if power > 0.1:
            self.lens_disk.setColor(0.6, 0.8, 1.0, alpha)  # Blue for convex
        elif power < -0.1:
            self.lens_disk.setColor(1.0, 0.9, 0.6, alpha)  # Amber for concave
        else:
            self.lens_disk.setColor(0.9, 0.9, 0.9, 0.2)   # Neutral
    
    def update_type(self, lens_type):
        if lens_type != self.lens_type:
            self.lens_type = lens_type
    
    def cleanup(self):
        self.node.removeNode()


class LightRay:
    """Visual representation of light ray"""
    
    def __init__(self, parent_node, start_pos, end_pos, color=(1, 1, 0.3, 0.9)):
        self.node = parent_node.attachNewNode("light_ray")
        self.start = start_pos
        self.end = end_pos
        self.color = color
        self._create_ray()
    
    def _create_ray(self):
        """Create ray visualization"""
        # Main ray line
        lines = LineSegs()
        lines.setThickness(4.5)
        lines.setColor(*self.color)
        
        if hasattr(self, 'segments') and len(self.segments) > 1:
            # Draw multi-segment path
            lines.moveTo(*self.segments[0])
            for segment in self.segments[1:]:
                lines.drawTo(*segment)
        else:
            # Simple two-point line
            lines.moveTo(*self.start)
            lines.drawTo(*self.end)
        
        self.ray_node = self.node.attachNewNode(lines.create())
    
    def update_path_segments(self, segments):
        self.segments = segments
        self.start = segments[0]
        self.end = segments[-1]
        if hasattr(self, 'ray_node'):
            self.ray_node.removeNode()
        self._create_ray()
    
    def set_color(self, color):
        self.color = color
        self.ray_node.removeNode()
        self._create_ray()
    
    def cleanup(self):
        self.node.removeNode()


class VisionScene:
    """Complete vision testing scene"""
    
    def __init__(self, parent_node, physics_engine=None):
        self.parent = parent_node
        self.physics = physics_engine  # Store physics reference for ray calculations
        self.light_rays = []
        self._create_scene()
    
    def _create_scene(self):
        """Build essential scene only"""
        # Create eye model
        self.eye = EyeModel(self.parent)
        self.eye.set_position(0, 0, 0)
        self.eye.set_scale(1.5)
        
        # Create corrective lens
        self.lens = CorrectiveLens(self.parent, 'none')
        self.lens.set_position(0, 3.0, 0)
        
        # Create test object
        self.test_object = self._create_test_object()
        self.test_object.setPos(0, 6.0, 0)
        
        # Create light rays
        self._create_light_rays(7)
        
        # Add professional labels
        self._create_labels()
        
        # Add optical axis
        self._create_optical_axis()
    
    def _create_test_object(self):
        """Create professional Snellen eye chart with letter E"""
        object_node = self.parent.attachNewNode("test_object")
        
        # Wall background (light gray/beige clinical setting)
        wall_bg = create_disk(1.5, 4)
        wall_bg.reparentTo(object_node)
        wall_bg.setScale(2.0, 1.0, 2.2)
        wall_bg.setH(90)
        wall_bg.setPos(0, -0.05, 0)  # Slightly behind chart
        wall_bg.setColor(0.88, 0.90, 0.85, 5.0)  # Soft clinical beige
        
        # Eye chart background (white board)
        chart = create_disk(0.9, 4)
        chart.reparentTo(object_node)
        chart.setScale(1.3, 1.0, 1.6)
        chart.setH(90)
        chart.setColor(0.98, 0.98, 1.0, 1.0)  # Clean white
        
        # Chart frame (black border)
        frame_lines = LineSegs()
        frame_lines.setThickness(6.0)
        frame_lines.setColor(0.15, 0.15, 0.2, 1.0)
        
        # Draw chart border
        corners = [
            (-1.17, 0, -1.44), (1.17, 0, -1.44),
            (1.17, 0, 1.44), (-1.17, 0, 1.44), (-1.17, 0, -1.44)
        ]
        for i in range(len(corners) - 1):
            frame_lines.moveTo(*corners[i])
            frame_lines.drawTo(*corners[i+1])
        
        object_node.attachNewNode(frame_lines.create())
        
        # Create large letter "E" (classic Snellen chart)
        e_lines = LineSegs()
        e_lines.setThickness(8.0)
        e_lines.setColor(0.1, 0.1, 0.15, 1.0)  # Dark text
        
        # Letter E dimensions (large and clear)
        e_width = 0.9
        e_height = 1.1
        bar_thick = 0.18
        y_offset = 0.02  # Slight forward offset
        
        # Top bar
        e_lines.moveTo(-e_width/2, y_offset, e_height/2)
        e_lines.drawTo(e_width/2, y_offset, e_height/2)
        e_lines.drawTo(e_width/2, y_offset, e_height/2 - bar_thick)
        e_lines.drawTo(-e_width/2, y_offset, e_height/2 - bar_thick)
        e_lines.drawTo(-e_width/2, y_offset, e_height/2)
        
        # Middle bar
        e_lines.moveTo(-e_width/2, y_offset, bar_thick/2)
        e_lines.drawTo(e_width/2 - 0.15, y_offset, bar_thick/2)
        e_lines.drawTo(e_width/2 - 0.15, y_offset, -bar_thick/2)
        e_lines.drawTo(-e_width/2, y_offset, -bar_thick/2)
        e_lines.drawTo(-e_width/2, y_offset, bar_thick/2)
        
        # Bottom bar
        e_lines.moveTo(-e_width/2, y_offset, -e_height/2)
        e_lines.drawTo(e_width/2, y_offset, -e_height/2)
        e_lines.drawTo(e_width/2, y_offset, -e_height/2 + bar_thick)
        e_lines.drawTo(-e_width/2, y_offset, -e_height/2 + bar_thick)
        e_lines.drawTo(-e_width/2, y_offset, -e_height/2)
        
        # Left vertical bar
        e_lines.moveTo(-e_width/2, y_offset, -e_height/2)
        e_lines.drawTo(-e_width/2 + bar_thick, y_offset, -e_height/2)
        e_lines.drawTo(-e_width/2 + bar_thick, y_offset, e_height/2)
        e_lines.drawTo(-e_width/2, y_offset, e_height/2)
        e_lines.drawTo(-e_width/2, y_offset, -e_height/2)
        
        object_node.attachNewNode(e_lines.create())
        
        # Add "SNELLEN CHART" title text
        title_lines = LineSegs()
        title_lines.setThickness(4.0)
        title_lines.setColor(0.3, 0.3, 0.4, 1.0)
        
        # Simple text lines for "20/20"
        text_y = 0.03
        title_lines.moveTo(-0.5, text_y, -1.25)
        title_lines.drawTo(0.5, text_y, -1.25)
        
        object_node.attachNewNode(title_lines.create())
        
        # Add indicator arrows pointing to the test object
        indicator = LineSegs()
        indicator.setThickness(5.0)
        indicator.setColor(0.2, 0.9, 0.3, 0.9)  # Bright green
        
        # Left arrow
        arrow_y = 0.05
        arrow_z = 1.8
        indicator.moveTo(-1.8, arrow_y, arrow_z)
        indicator.drawTo(-1.4, arrow_y, arrow_z)
        # Arrowhead
        indicator.drawTo(-1.5, arrow_y, arrow_z + 0.1)
        indicator.moveTo(-1.4, arrow_y, arrow_z)
        indicator.drawTo(-1.5, arrow_y, arrow_z - 0.1)
        
        # Right arrow
        indicator.moveTo(1.8, arrow_y, arrow_z)
        indicator.drawTo(1.4, arrow_y, arrow_z)
        # Arrowhead
        indicator.drawTo(1.5, arrow_y, arrow_z + 0.1)
        indicator.moveTo(1.4, arrow_y, arrow_z)
        indicator.drawTo(1.5, arrow_y, arrow_z - 0.1)
        
        object_node.attachNewNode(indicator.create())
        
        # Add "TEST OBJECT" text indicator above
        indicator_text = TextNode('test_indicator')
        indicator_text.setText("TEST OBJECT")
        indicator_text.setAlign(TextNode.ACenter)
        indicator_text.setTextColor(0.2, 0.9, 0.3, 1.0)
        
        text_np = object_node.attachNewNode(indicator_text)
        text_np.setScale(0.35)
        text_np.setPos(0, 0.08, 2.0)
        text_np.setBillboardPointEye()
        
        return object_node
    
    def _create_light_rays(self, count=7):
        """Create light rays from object to eye"""
        # Clear existing rays
        for ray in self.light_rays:
            ray.cleanup()
        self.light_rays.clear()
        
        # Create rays at different angles
        object_y = self.test_object.getY()
        
        for i in range(count):
            # Spread rays vertically
            z_offset = (i - count//2) * 0.5
            
            start_pos = (0, object_y, z_offset)
            end_pos = (0, 1.5, z_offset * 0.35)
            
            # Color based on position
            if abs(i - count//2) <= 1:
                color = (0.4, 1.0, 0.4, 1.0)  # Bright green for central rays
            else:
                color = (0.3, 0.8, 0.3, 0.85)  # Dimmer green for outer rays
            
            ray = LightRay(self.parent, start_pos, end_pos, color)
            self.light_rays.append(ray)
    
    def _create_labels(self):
        """Create clear, professional 3D text labels pointing to exact anatomy"""
        # Professional color scheme
        label_colors = {
            'CORNEA': (0.5, 0.85, 1.0, 1.0),
            'PUPIL': (0.4, 0.4, 0.8, 1.0),
            'CRYSTALLINE': (1.0, 0.95, 0.5, 1.0),
            'RETINA': (1.0, 0.4, 0.4, 1.0),
            'FOVEA': (0.9, 0.3, 0.3, 1.0),
            'OPTIC': (0.8, 0.7, 0.4, 1.0),
        }
        
        # Precise labels pointing to exact anatomical structures
        labels = [
            # (text, label_pos, scale, exact_point_on_anatomy, color_key)
            ("CORNEA", (-2.2, 2.2, 2.5), 0.42, (0, 1.8, 0), 'CORNEA'),
            ("PUPIL", (2.2, 1.8, 2.2), 0.38, (0, 0.83, 0), 'PUPIL'),
            ("CRYSTALLINE\nLENS", (-2.5, 1.2, -2.2), 0.40, (0, 0.55, 0), 'CRYSTALLINE'),
            ("RETINA", (2.5, -1.8, 2.2), 0.42, (0, -0.95, 0.3), 'RETINA'),
            ("FOVEA\n(Focus)", (0, -2.5, -3.0), 0.38, (0, -0.95, 0), 'FOVEA'),
            ("OPTIC\nNERVE", (-2.8, -2.2, -2.5), 0.38, (0.25, -0.95, -0.15), 'OPTIC'),
        ]
        
        self.label_nodes = []
        
        for text, label_pos, scale, point_to, color_key in labels:
            color = label_colors[color_key]
            
            # Create precise pointer line with dashes
            pointer = LineSegs()
            pointer.setThickness(3.0)
            pointer.setColor(color[0], color[1], color[2], 0.85)
            
            start = Vec3(*label_pos)
            end = Vec3(*point_to)
            direction = end - start
            length = direction.length()
            direction.normalize()
            
            # Draw dashed line
            dash_length = 0.25
            gap_length = 0.12
            current_pos = start
            
            while (current_pos - start).length() < length - 0.1:
                remaining = length - (current_pos - start).length()
                dash_end = current_pos + direction * min(dash_length, remaining)
                pointer.moveTo(current_pos)
                pointer.drawTo(dash_end)
                current_pos = dash_end + direction * gap_length
            
            pointer_np = self.parent.attachNewNode(pointer.create())
            self.label_nodes.append(pointer_np)
            
            # Create arrowhead at anatomy point
            arrow = LineSegs()
            arrow.setThickness(4.5)
            arrow.setColor(*color)
            
            up = Vec3(0, 0, 1)
            side1 = direction.cross(up)
            if side1.length() < 0.01:
                side1 = Vec3(1, 0, 0)
            side1.normalize()
            side2 = direction.cross(side1)
            side2.normalize()
            
            arrow_size = 0.18
            
            # Solid arrowhead
            arrow.moveTo(end)
            arrow.drawTo(end - direction * arrow_size + side1 * arrow_size * 0.6)
            arrow.drawTo(end - direction * arrow_size + side2 * arrow_size * 0.6)
            arrow.drawTo(end)
            arrow.drawTo(end - direction * arrow_size - side1 * arrow_size * 0.6)
            arrow.drawTo(end - direction * arrow_size - side2 * arrow_size * 0.6)
            arrow.drawTo(end)
            
            arrow_np = self.parent.attachNewNode(arrow.create())
            self.label_nodes.append(arrow_np)
            
            # Create professional text label
            text_node = TextNode('label')
            text_node.setText(text)
            text_node.setAlign(TextNode.ACenter)
            text_node.setTextColor(1, 1, 1, 1)
            
            label_np = self.parent.attachNewNode(text_node)
            label_np.setScale(scale)
            label_np.setPos(*label_pos)
            
            # Background sizing
            if '\n' in text:
                bg_width = scale * 2.4
                bg_height = scale * 1.3
            else:
                bg_width = scale * 2.0
                bg_height = scale * 0.65
            
            # Create background plate
            bg_format = GeomVertexFormat.getV3c4()
            bg_vdata = GeomVertexData('bg', bg_format, Geom.UHStatic)
            bg_vertex = GeomVertexWriter(bg_vdata, 'vertex')
            bg_color_writer = GeomVertexWriter(bg_vdata, 'color')
            
            vertices = [
                (-bg_width, 0.01, -bg_height),
                (bg_width, 0.01, -bg_height),
                (bg_width, 0.01, bg_height),
                (-bg_width, 0.01, bg_height)
            ]
            
            for vx, vy, vz in vertices:
                bg_vertex.addData3f(vx, vy, vz)
                bg_color_writer.addData4f(color[0]*0.35, color[1]*0.35, color[2]*0.35, 0.95)
            
            bg_prim = GeomTriangles(Geom.UHStatic)
            bg_prim.addVertices(0, 1, 2)
            bg_prim.addVertices(0, 2, 3)
            
            bg_geom = Geom(bg_vdata)
            bg_geom.addPrimitive(bg_prim)
            bg_node = GeomNode('bg')
            bg_node.addGeom(bg_geom)
            bg_np = self.parent.attachNewNode(bg_node)
            bg_np.setPos(*label_pos)
            bg_np.setBillboardPointEye()
            
            self.label_nodes.extend([label_np, bg_np])
            label_np.setBillboardPointEye()
            bg_np = self.parent.attachNewNode(bg_node)
            bg_np.setPos(*label_pos)
            bg_np.setBillboardPointEye()
            
            self.label_nodes.extend([label_np, bg_np])
            label_np.setBillboardPointEye()

    def _create_optical_axis(self):
        """Create simplified optical axis with key distance markers"""
        # Main optical axis line (subtle)
        axis = LineSegs()
        axis.setThickness(2.0)
        axis.setColor(0.6, 0.6, 0.7, 0.4)
        
        y_start = -2.0
        y_end = 8.5
        
        axis.moveTo(0, y_start, 0)
        axis.drawTo(0, y_end, 0)
        
        axis_np = self.parent.attachNewNode(axis.create())
        
        # Add only key measurement markers (simplified)
        marker_lines = LineSegs()
        marker_lines.setThickness(1.5)
        marker_lines.setColor(0.7, 0.7, 0.8, 0.35)
        
        # Mark key positions only
        key_positions = [6.0, 3.0, 0, -0.95]  # Object, Lens, Eye, Retina
        
        for y in key_positions:
            marker_lines.moveTo(-0.25, y, 0)
            marker_lines.drawTo(0.25, y, 0)
        
        markers_np = self.parent.attachNewNode(marker_lines.create())
        
        if not hasattr(self, 'label_nodes'):
            self.label_nodes = []
        self.label_nodes.extend([axis_np, markers_np])
        self.label_nodes.extend([axis_np, markers_np])

    def _update_light_rays(self):
        """Update light ray paths based on actual physics calculations"""
        # Safety check - if no physics engine, use simple straight rays
        if not self.physics:
            for i, ray in enumerate(self.light_rays):
                count = len(self.light_rays)
                z_offset = (i - count//2) * 0.6
                object_y = self.test_object.getY()
                segments = [
                    (0, object_y, z_offset),
                    (0, 1.2, z_offset * 0.5),
                    (0, -0.98, z_offset * 0.2)
                ]
                ray.update_path_segments(segments)
            return
        
        object_y = self.test_object.getY()
        lens_y = self.lens.node.getY()
        
        count = len(self.light_rays)
        
        # Get physics calculations
        effective_near_point = self.physics.get_effective_near_point()
        required_power = self.physics.get_required_power()
        lens_power = self.physics.lens_power
        
        # Calculate focus point based on lens correction
        focus_error = abs(lens_power - required_power)
        
        if focus_error < 0.25:  # Good correction
            focus_y = -0.98  # Perfect focus on retina
        else:
            # Calculate focus shift based on correction error
            focus_shift = (lens_power - required_power) * 0.8
            focus_y = -0.98 + focus_shift
        
        # Clamp focus to reasonable bounds
        focus_y = max(-2.0, min(1.5, focus_y))
        
        # Update focal point position
        self.eye.focal_point.setPos(0, focus_y, 0)
        
        # Update focal point color based on focus quality (always fully opaque)
        focus_quality = self.physics.get_focus_quality()
        if focus_quality > 80:
            self.eye.focal_point.setColor(0.3, 1.0, 0.3, 1.0)  # Bright green
        elif focus_quality > 50:
            self.eye.focal_point.setColor(1.0, 1.0, 0.3, 1.0)  # Yellow
        else:
            self.eye.focal_point.setColor(1.0, 0.3, 0.3, 1.0)  # Red
        
        for i, ray in enumerate(self.light_rays):
            # Vertical spread at object
            z_offset = (i - count//2) * 0.6
            
            # Start from object point
            start_pos = (0, object_y, z_offset)
            
            if self.lens.node.isHidden() or abs(lens_power) < 0.1:
                # No corrective lens or zero power
                if abs(self.physics.near_point - 25.0) < 1.0:
                    # Normal vision - rays converge on retina
                    cornea_z = z_offset * 0.5
                    lens_z = z_offset * 0.25
                    retina_z = z_offset * 0.15
                    
                    segments = [
                        start_pos,
                        (0, 1.2, cornea_z),
                        (0, 0.65, lens_z),
                        (0, -0.98, retina_z)
                    ]
                else:
                    # Defective vision without correction
                    defect_factor = (self.physics.near_point - 25.0) / 25.0
                    focus_shift = defect_factor * 1.5
                    focus_y_uncorrected = -0.98 + focus_shift
                    
                    segments = [
                        start_pos,
                        (0, 1.2, z_offset * 0.7),
                        (0, 0.65, z_offset * 0.5),
                        (0, focus_y_uncorrected, z_offset * 0.3)
                    ]
            else:
                # With corrective lens
                lens_strength = abs(lens_power) / 5.0
                lens_bend = z_offset * (0.3 + lens_strength * 0.4)
                
                if lens_power > 0:  # Convex lens
                    lens_bend = -lens_bend
                else:  # Concave lens
                    lens_bend = lens_bend
                
                segments = [
                    start_pos,
                    (0, lens_y, z_offset * 0.8),
                    (0, lens_y + 0.5, lens_bend),
                    (0, 1.2, z_offset * 0.4),
                    (0, 0.65, z_offset * 0.2),
                    (0, focus_y, z_offset * 0.08)
                ]
            
            # Update ray to show complete path
            ray.update_path_segments(segments)

    def update_lens_power(self, power, lens_type):
        """Update corrective lens appearance"""
        self.lens.update_type(lens_type)
        self.lens.set_power_visual(power)
        
        if abs(power) < 0.1:
            self.lens.node.hide()
        else:
            self.lens.node.show()
        
        # Update visualization
        self._update_light_rays()

    def update_corrective_lens(self, power, distance):
        """Update corrective lens power and position"""
        self.lens.set_power_visual(power)
        
        if abs(power) < 0.1:
            self.lens.node.hide()
        else:
            self.lens.node.show()
            
        self.lens.node.setY(distance / 10.0)
        self._update_light_rays()

    def update_object_distance(self, distance):
        """Update test object distance"""
        self.test_object.setY(distance)
        self._update_light_rays()

    def update_light_rays(self, focus_quality):
        """Update light ray colors based on focus quality"""
        if focus_quality > 80:
            color = (0.3, 1.0, 0.3, 0.8)
            self.eye.focal_point.setColor(0.3, 1.0, 0.3, 1.0)  # Fully opaque
        elif focus_quality > 50:
            color = (1.0, 1.0, 0.3, 0.7)
            self.eye.focal_point.setColor(1.0, 1.0, 0.3, 1.0)  # Fully opaque
        else:
            color = (1.0, 0.3, 0.3, 0.6)
            self.eye.focal_point.setColor(1.0, 0.3, 0.3, 1.0)  # Fully opaque
        
        for ray in self.light_rays:
            ray.set_color(color)

    def cleanup(self):
        """Clean up all scene elements"""
        self.eye.cleanup()
        self.lens.cleanup()
        self.test_object.removeNode()
        
        for ray in self.light_rays:
            ray.cleanup()
        self.light_rays.clear()
        
        if hasattr(self, 'label_nodes'):
            for label in self.label_nodes:
                label.removeNode()
            self.label_nodes.clear()