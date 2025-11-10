"""
Optical Physics Module for Vision Simulation
Implements lens formula, vision conditions, and power calculations
"""

import math


class VisionPhysics:
    """
    Manages optical physics calculations for eye and lens system.
    Implements lens formula: 1/f = 1/v - 1/u
    """
    
    # Standard constants (in cm)
    NORMAL_NEAR_POINT = 25.0  # Standard near point for normal vision
    MIN_NEAR_POINT = 10.0     # Extreme myopia
    MAX_NEAR_POINT = 100.0    # Extreme hyperopia
    
    # Lens power range (in diopters)
    MIN_POWER = -10.0
    MAX_POWER = 10.0
    
    # Vision condition types
    VISION_TYPES = {
        'normal': {'near_point': 25.0, 'description': 'Normal Vision'},
        'myopia': {'near_point': 15.0, 'description': 'Myopia (Nearsighted)'},
        'hyperopia': {'near_point': 40.0, 'description': 'Hyperopia (Farsighted)'},
        'presbyopia': {'near_point': 50.0, 'description': 'Presbyopia (Age-related)'}
    }
    
    # Preset patient cases
    PRESETS = {
        'normal': {
            'near_point': 25.0,
            'age': 25,
            'description': 'Normal Vision - Student'
        },
        'mild_myopia': {
            'near_point': 15.0,
            'age': 20,
            'description': 'Mild Myopia - Young Adult'
        },
        'moderate_myopia': {
            'near_point': 12.0,
            'age': 18,
            'description': 'Moderate Myopia - Teen'
        },
        'mild_hyperopia': {
            'near_point': 40.0,
            'age': 45,
            'description': 'Mild Hyperopia - Middle-aged'
        },
        'presbyopia': {
            'near_point': 50.0,
            'age': 60,
            'description': 'Presbyopia - Elderly'
        }
    }
    
    def __init__(self, near_point=25.0, object_distance=25.0):
        """
        Initialize vision physics engine.
        
        Args:
            near_point (float): Minimum clear vision distance in cm
            object_distance (float): Current object distance in cm
        """
        self._near_point = self._clamp_near_point(near_point)
        self._object_distance = self._clamp_distance(object_distance)
        self._lens_power = 0.0  # Diopters
        self._age = 25
        
        self._calculate_required_power()
    
    @property
    def near_point(self):
        """Get near point distance in cm"""
        return self._near_point
    
    @near_point.setter
    def near_point(self, value):
        """Set near point and recalculate"""
        self._near_point = self._clamp_near_point(value)
        self._calculate_required_power()
    
    @property
    def object_distance(self):
        """Get object distance in cm"""
        return self._object_distance
    
    @object_distance.setter
    def object_distance(self, value):
        """Set object distance"""
        self._object_distance = self._clamp_distance(value)
    
    @property
    def lens_power(self):
        """Get lens power in diopters"""
        return self._lens_power
    
    @lens_power.setter
    def lens_power(self, value):
        """Set lens power"""
        self._lens_power = max(self.MIN_POWER, min(self.MAX_POWER, value))
    
    @property
    def age(self):
        """Get patient age"""
        return self._age
    
    @age.setter
    def age(self, value):
        """Set age and adjust near point for presbyopia"""
        self._age = max(5, min(100, value))
        # Simulate presbyopia with age
        if self._age > 40:
            age_factor = (self._age - 40) / 60.0  # 0 to 1 over age 40-100
            self._near_point = 25.0 + (age_factor * 30.0)  # Up to 55cm
            self._calculate_required_power()
    
    def _clamp_near_point(self, value):
        """Ensure near point is within valid range"""
        return max(self.MIN_NEAR_POINT, min(self.MAX_NEAR_POINT, value))
    
    def _clamp_distance(self, value):
        """Ensure distance is valid"""
        return max(5.0, min(200.0, value))
    
    def _calculate_required_power(self):
        """
        Calculate required lens power to correct vision.
        Uses lens formula: 1/f = 1/v - 1/u
        
        Where:
        f = focal length of corrective lens
        v = image distance (defective eye's near point, negative)
        u = object distance (normal near point = -25cm)
        """
        if abs(self._near_point - self.NORMAL_NEAR_POINT) < 0.1:
            self._required_power = 0.0
            return
        
        # Convert to meters for diopter calculation
        v = -self._near_point / 100.0  # Defective near point (negative)
        u = -self.NORMAL_NEAR_POINT / 100.0  # Normal near point (negative)
        
        # Lens formula: 1/f = 1/v - 1/u
        focal_length_inv = (1.0 / v) - (1.0 / u)
        
        # Power in diopters (P = 1/f in meters)
        self._required_power = focal_length_inv
    
    def get_required_power(self):
        """Get the calculated required lens power in diopters"""
        return self._required_power
    
    def get_vision_condition(self):
        """
        Determine vision condition based on near point.
        
        Returns:
            str: Vision condition type
        """
        if self._near_point < 20.0:
            return 'myopia'
        elif self._near_point > 30.0:
            if self._age > 45:
                return 'presbyopia'
            else:
                return 'hyperopia'
        else:
            return 'normal'
    
    def get_lens_type(self):
        """
        Determine required lens type.
        
        Returns:
            str: 'concave', 'convex', or 'none'
        """
        if self._near_point < self.NORMAL_NEAR_POINT - 2:
            return 'concave'  # Diverging lens for myopia
        elif self._near_point > self.NORMAL_NEAR_POINT + 2:
            return 'convex'   # Converging lens for hyperopia
        else:
            return 'none'
    
    def is_clear_vision(self):
        """
        Check if current lens power provides clear vision.
        
        Returns:
            bool: True if vision is clear with current lens
        """
        # Check if object is at a viewable distance with current correction
        power_diff = abs(self._lens_power - self._required_power)
        return power_diff < 0.25  # Within 0.25 diopter tolerance
    
    def get_effective_near_point(self):
        """
        Calculate effective near point with current lens correction.
        
        Returns:
            float: Effective near point in cm
        """
        if abs(self._lens_power) < 0.01:
            return self._near_point
        
        # With corrective lens, calculate new near point
        # P = 1/f, so f = 1/P (in meters)
        if abs(self._lens_power) > 0.01:
            focal_length = 1.0 / self._lens_power  # in meters
            
            # Using lens formula to find new image distance
            u = -self.NORMAL_NEAR_POINT / 100.0  # Object at 25cm
            f = focal_length
            
            # 1/v = 1/f + 1/u
            if abs(f - u) > 0.001:
                v = (f * u) / (f + u)
                effective_near_point = abs(v * 100.0)  # Convert to cm
                return min(100.0, max(10.0, effective_near_point))
        
        return self._near_point
    
    def get_focus_quality(self):
        """
        Calculate focus quality at current object distance.
        
        Returns:
            float: Focus quality from 0 (blurred) to 1 (sharp)
        """
        effective_np = self.get_effective_near_point()
        
        # If object is at effective near point, perfect focus
        if abs(self._object_distance - effective_np) < 2.0:
            return 1.0
        
        # Calculate blur based on distance from optimal
        distance_error = abs(self._object_distance - effective_np)
        max_blur_distance = 30.0
        
        focus = max(0.0, 1.0 - (distance_error / max_blur_distance))
        return focus
    
    def get_ray_convergence_point(self, lens_present=True):
        """
        Calculate where light rays converge after passing through eye+lens system.
        
        Args:
            lens_present (bool): Whether corrective lens is applied
        
        Returns:
            float: Convergence distance from lens (cm)
        """
        if not lens_present or abs(self._lens_power) < 0.01:
            # Without lens, rays converge at defective near point
            return self._near_point
        
        # With lens, rays should converge at corrected point
        return self.get_effective_near_point()
    
    def set_preset(self, preset_name):
        """
        Apply a preset patient case.
        
        Args:
            preset_name (str): Name of preset
        
        Returns:
            bool: True if preset was applied
        """
        if preset_name in self.PRESETS:
            preset = self.PRESETS[preset_name]
            self._near_point = preset['near_point']
            self._age = preset['age']
            self._calculate_required_power()
            return True
        return False
    
    def get_status_text(self):
        """
        Get formatted status information.
        
        Returns:
            dict: Status information
        """
        return {
            'near_point': f'{self._near_point:.1f}',
            'object_distance': f'{self._object_distance:.1f}',
            'required_power': f'{self._required_power:+.2f}',
            'current_power': f'{self._lens_power:+.2f}',
            'condition': self.get_vision_condition().title(),
            'lens_type': self.get_lens_type().title(),
            'focus_quality': f'{self.get_focus_quality() * 100:.0f}',
            'age': f'{self._age}'
        }
    
    def __str__(self):
        """String representation"""
        condition = self.get_vision_condition().title()
        return (f"Vision: {condition}, "
                f"Near Point: {self._near_point:.1f}cm, "
                f"Required: {self._required_power:+.2f}D, "
                f"Current: {self._lens_power:+.2f}D")
