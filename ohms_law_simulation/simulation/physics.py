"""
Physics Module for Ohm's Law Simulation
Handles all electrical calculations and validations
"""


class OhmsLawPhysics:
    """
    Manages physics calculations for the Ohm's Law simulation.
    Implements V = I × R and related electrical formulas.
    """
    
    # Physical constants and limits
    MIN_VOLTAGE = 1.0      # Volts
    MAX_VOLTAGE = 50.0     # Volts
    MIN_RESISTANCE = 1.0   # Ohms
    MAX_RESISTANCE = 100.0 # Ohms
    MIN_SAFE_RESISTANCE = 0.1  # Prevent division by zero
    
    # Preset scenarios
    PRESETS = {
        'normal': {'voltage': 12.0, 'resistance': 10.0},
        'high_current': {'voltage': 24.0, 'resistance': 2.0},
        'low_current': {'voltage': 5.0, 'resistance': 50.0},
        'short_circuit': {'voltage': 12.0, 'resistance': 0.1},
        'open_circuit': {'voltage': 12.0, 'resistance': 100.0}
    }
    
    def __init__(self, voltage=12.0, resistance=10.0):
        """
        Initialize physics engine with default values.
        
        Args:
            voltage (float): Initial voltage in volts
            resistance (float): Initial resistance in ohms
        """
        self._voltage = self._clamp_voltage(voltage)
        self._resistance = self._clamp_resistance(resistance)
        self._current = 0.0
        self._power = 0.0
        self._update_calculations()
    
    @property
    def voltage(self):
        """Get current voltage in volts"""
        return self._voltage
    
    @voltage.setter
    def voltage(self, value):
        """Set voltage and recalculate dependent values"""
        self._voltage = self._clamp_voltage(value)
        self._update_calculations()
    
    @property
    def resistance(self):
        """Get current resistance in ohms"""
        return self._resistance
    
    @resistance.setter
    def resistance(self, value):
        """Set resistance and recalculate dependent values"""
        self._resistance = self._clamp_resistance(value)
        self._update_calculations()
    
    @property
    def current(self):
        """Get calculated current in amperes"""
        return self._current
    
    @property
    def power(self):
        """Get calculated power in watts"""
        return self._power
    
    def _clamp_voltage(self, voltage):
        """Ensure voltage is within safe limits"""
        return max(self.MIN_VOLTAGE, min(self.MAX_VOLTAGE, voltage))
    
    def _clamp_resistance(self, resistance):
        """Ensure resistance is within safe limits"""
        return max(self.MIN_RESISTANCE, min(self.MAX_RESISTANCE, resistance))
    
    def _update_calculations(self):
        """
        Update all dependent calculations based on current V and R.
        Implements Ohm's Law: I = V / R and Power Law: P = V × I
        """
        # Prevent division by zero
        safe_resistance = max(self._resistance, self.MIN_SAFE_RESISTANCE)
        
        # Ohm's Law: I = V / R
        self._current = self._voltage / safe_resistance
        
        # Power Law: P = V × I
        self._power = self._voltage * self._current
    
    def set_preset(self, preset_name):
        """
        Apply a preset scenario.
        
        Args:
            preset_name (str): Name of preset ('normal', 'high_current', etc.)
        
        Returns:
            bool: True if preset was applied, False if preset not found
        """
        if preset_name in self.PRESETS:
            preset = self.PRESETS[preset_name]
            self.voltage = preset['voltage']
            self.resistance = preset['resistance']
            return True
        return False
    
    def get_electron_speed_factor(self, base_speed=1.0):
        """
        Calculate visual speed factor for electron animation.
        Speed is proportional to current flow.
        
        Args:
            base_speed (float): Base speed multiplier
        
        Returns:
            float: Speed factor for electron animation
        """
        # Map current to a reasonable visual speed
        # Higher current = faster electrons
        return base_speed * (1.0 + self._current * 0.5)
    
    def get_intensity_color(self, base_color=(1, 1, 0, 1)):
        """
        Calculate color intensity based on current.
        Higher current = brighter/more intense color.
        
        Args:
            base_color (tuple): RGBA base color
        
        Returns:
            tuple: Modified RGBA color with intensity
        """
        # Normalize current to 0-1 range for color intensity
        # Assuming max current of ~50A (50V / 1Ω)
        intensity = min(self._current / 50.0, 1.0)
        
        r, g, b, a = base_color
        return (
            r * (0.3 + 0.7 * intensity),
            g * (0.3 + 0.7 * intensity),
            b * (0.3 + 0.7 * intensity),
            a
        )
    
    def get_status_text(self):
        """
        Get formatted status text for display.
        
        Returns:
            dict: Dictionary with formatted electrical values
        """
        return {
            'voltage': f'{self._voltage:.2f}',
            'current': f'{self._current:.3f}',
            'resistance': f'{self._resistance:.2f}',
            'power': f'{self._power:.2f}'
        }
    
    def is_dangerous(self):
        """
        Check if current configuration is potentially dangerous.
        
        Returns:
            tuple: (is_dangerous: bool, warning_message: str)
        """
        # Check for very high current (potential short circuit)
        if self._current > 20.0:
            return (True, "WARNING: Very high current! Risk of short circuit!")
        
        # Check for very high power
        if self._power > 500.0:
            return (True, "WARNING: Very high power dissipation!")
        
        return (False, "")
    
    def __str__(self):
        """String representation of current state"""
        return (f"V={self._voltage:.2f}V, "
                f"I={self._current:.3f}A, "
                f"R={self._resistance:.2f}Ω, "
                f"P={self._power:.2f}W")
