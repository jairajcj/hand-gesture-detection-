"""
Color Blindness Correction System
Real-time camera application to help colorblind individuals see colors more accurately.
Supports Protanopia, Deuteranopia, and Tritanopia correction.
"""

import cv2
import numpy as np
from typing import Tuple


class ColorBlindnessCorrector:
    """
    Implements Daltonization algorithms for color blindness correction.
    Uses LMS (Long, Medium, Short wavelength) color space transformation.
    """
    
    def __init__(self):
        # RGB to LMS transformation matrix
        self.rgb2lms = np.array([
            [17.8824, 43.5161, 4.11935],
            [3.45565, 27.1554, 3.86714],
            [0.0299566, 0.184309, 1.46709]
        ])
        
        # LMS to RGB transformation matrix (inverse)
        self.lms2rgb = np.linalg.inv(self.rgb2lms)
        
        # Simulation matrices for different types of color blindness
        # Protanopia (red-blind) - missing L-cones
        self.protanopia_sim = np.array([
            [0.0, 2.02344, -2.52581],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ])
        
        # Deuteranopia (green-blind) - missing M-cones
        self.deuteranopia_sim = np.array([
            [1.0, 0.0, 0.0],
            [0.494207, 0.0, 1.24827],
            [0.0, 0.0, 1.0]
        ])
        
        # Tritanopia (blue-blind) - missing S-cones
        self.tritanopia_sim = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [-0.395913, 0.801109, 0.0]
        ])
        
        self.current_mode = 'normal'
        
    def rgb_to_lms(self, rgb_image: np.ndarray) -> np.ndarray:
        """Convert RGB image to LMS color space."""
        # Normalize to 0-1 range
        rgb_normalized = rgb_image.astype(np.float32) / 255.0
        
        # Reshape for matrix multiplication
        h, w, c = rgb_normalized.shape
        rgb_reshaped = rgb_normalized.reshape(-1, 3)
        
        # Apply transformation
        lms = rgb_reshaped @ self.rgb2lms.T
        
        return lms.reshape(h, w, 3)
    
    def lms_to_rgb(self, lms_image: np.ndarray) -> np.ndarray:
        """Convert LMS image back to RGB color space."""
        h, w, c = lms_image.shape
        lms_reshaped = lms_image.reshape(-1, 3)
        
        # Apply transformation
        rgb = lms_reshaped @ self.lms2rgb.T
        
        # Clip and denormalize
        rgb = np.clip(rgb, 0, 1)
        rgb = (rgb * 255).astype(np.uint8)
        
        return rgb.reshape(h, w, 3)
    
    def simulate_colorblindness(self, lms_image: np.ndarray, cb_type: str) -> np.ndarray:
        """Simulate how a colorblind person would see the image."""
        h, w, c = lms_image.shape
        lms_reshaped = lms_image.reshape(-1, 3)
        
        if cb_type == 'protanopia':
            sim_matrix = self.protanopia_sim
        elif cb_type == 'deuteranopia':
            sim_matrix = self.deuteranopia_sim
        elif cb_type == 'tritanopia':
            sim_matrix = self.tritanopia_sim
        else:
            return lms_image
        
        # Apply simulation
        lms_sim = lms_reshaped @ sim_matrix.T
        
        return lms_sim.reshape(h, w, 3)
    
    def daltonize(self, rgb_image: np.ndarray, cb_type: str) -> np.ndarray:
        """
        Apply Daltonization algorithm to correct for color blindness.
        
        Algorithm:
        1. Convert RGB to LMS
        2. Simulate colorblindness in LMS space
        3. Calculate error between original and simulated
        4. Add error back to original with specific weights
        5. Convert back to RGB
        """
        # Convert to LMS
        lms_original = self.rgb_to_lms(rgb_image)
        
        # Simulate colorblindness
        lms_simulated = self.simulate_colorblindness(lms_original, cb_type)
        
        # Calculate error
        lms_error = lms_original - lms_simulated
        
        # Error correction matrix (shifts error to visible channels)
        if cb_type == 'protanopia':
            # Shift red information to green and blue
            error_correction = np.array([
                [0, 0, 0],
                [0.7, 1, 0],
                [0.7, 0, 1]
            ])
        elif cb_type == 'deuteranopia':
            # Shift green information to red and blue
            error_correction = np.array([
                [1, 0.7, 0],
                [0, 0, 0],
                [0, 0.7, 1]
            ])
        elif cb_type == 'tritanopia':
            # Shift blue information to red and green
            error_correction = np.array([
                [1, 0, 0.7],
                [0, 1, 0.7],
                [0, 0, 0]
            ])
        else:
            return rgb_image
        
        # Apply error correction
        h, w, c = lms_error.shape
        lms_error_reshaped = lms_error.reshape(-1, 3)
        lms_corrected_error = lms_error_reshaped @ error_correction.T
        lms_corrected_error = lms_corrected_error.reshape(h, w, 3)
        
        # Add corrected error back to original
        lms_corrected = lms_original + lms_corrected_error
        
        # Convert back to RGB
        rgb_corrected = self.lms_to_rgb(lms_corrected)
        
        return rgb_corrected
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a single frame based on current mode."""
        if self.current_mode == 'normal':
            return frame
        elif self.current_mode in ['protanopia', 'deuteranopia', 'tritanopia']:
            return self.daltonize(frame, self.current_mode)
        else:
            return frame
    
    def set_mode(self, mode: str):
        """Set the correction mode."""
        valid_modes = ['normal', 'protanopia', 'deuteranopia', 'tritanopia']
        if mode in valid_modes:
            self.current_mode = mode
            print(f"Mode changed to: {mode.upper()}")
        else:
            print(f"Invalid mode: {mode}")


class ColorBlindnessApp:
    """Main application for real-time color blindness correction."""
    
    def __init__(self, camera_id: int = 0, width: int = 640, height: int = 480):
        self.corrector = ColorBlindnessCorrector()
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = None
        self.fps = 0
        
    def initialize_camera(self) -> bool:
        """Initialize camera capture."""
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            print("Error: Could not open camera")
            return False
        
        # Set camera properties for performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Camera initialized successfully")
        return True
    
    def draw_ui(self, frame: np.ndarray) -> np.ndarray:
        """Draw UI elements on the frame."""
        # Create a copy to draw on
        display_frame = frame.copy()
        
        # Draw semi-transparent background for text
        overlay = display_frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, display_frame, 0.4, 0, display_frame)
        
        # Draw text
        font = cv2.FONT_HERSHEY_SIMPLEX
        mode_text = f"Mode: {self.corrector.current_mode.upper()}"
        fps_text = f"FPS: {self.fps:.1f}"
        
        cv2.putText(display_frame, mode_text, (20, 40), font, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, fps_text, (20, 70), font, 0.6, (255, 255, 255), 1)
        
        # Instructions
        cv2.putText(display_frame, "Controls:", (20, 100), font, 0.5, (200, 200, 200), 1)
        
        # Draw controls panel
        cv2.rectangle(overlay, (10, 130), (500, 250), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, display_frame, 0.4, 0, display_frame)
        
        controls = [
            "N - Normal (no correction)",
            "P - Protanopia (red-blind)",
            "D - Deuteranopia (green-blind)",
            "T - Tritanopia (blue-blind)",
            "Q - Quit"
        ]
        
        y_offset = 155
        for control in controls:
            cv2.putText(display_frame, control, (20, y_offset), font, 0.45, (200, 200, 200), 1)
            y_offset += 25
        
        return display_frame
    
    def run(self):
        """Main application loop."""
        if not self.initialize_camera():
            return
        
        print("\n" + "="*50)
        print("Color Blindness Correction System")
        print("="*50)
        print("\nControls:")
        print("  N - Normal mode (no correction)")
        print("  P - Protanopia correction (red-blind)")
        print("  D - Deuteranopia correction (green-blind)")
        print("  T - Tritanopia correction (blue-blind)")
        print("  Q - Quit")
        print("\nStarting camera feed...\n")
        
        # For FPS calculation
        import time
        prev_time = time.time()
        
        while True:
            # Capture frame
            ret, frame = self.cap.read()
            
            if not ret:
                print("Error: Failed to capture frame")
                break
            
            # Process frame
            processed_frame = self.corrector.process_frame(frame)
            
            # Calculate FPS
            current_time = time.time()
            self.fps = 1 / (current_time - prev_time)
            prev_time = current_time
            
            # Draw UI
            display_frame = self.draw_ui(processed_frame)
            
            # Display
            cv2.imshow('Color Blindness Correction', display_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == ord('Q'):
                print("\nExiting...")
                break
            elif key == ord('n') or key == ord('N'):
                self.corrector.set_mode('normal')
            elif key == ord('p') or key == ord('P'):
                self.corrector.set_mode('protanopia')
            elif key == ord('d') or key == ord('D'):
                self.corrector.set_mode('deuteranopia')
            elif key == ord('t') or key == ord('T'):
                self.corrector.set_mode('tritanopia')
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed successfully")


def main():
    """Entry point for the application."""
    # Create and run the application
    # You can adjust camera_id, width, and height as needed
    app = ColorBlindnessApp(camera_id=0, width=640, height=480)
    app.run()


if __name__ == "__main__":
    main()
