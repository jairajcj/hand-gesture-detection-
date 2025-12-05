import numpy as np
import cv2

class ColorCorrector:
    def __init__(self, mode='deuteranopia'):
        self.mode = mode
        # LMS Daltonization matrices
        # Source: http://www.daltonize.org/2010/05/lms-daltonization-algorithm.html
        
        # RGB to LMS
        self.lms_matrix = np.array([[17.8824, 43.5161, 4.11935],
                                    [3.45565, 27.1554, 3.86714],
                                    [0.0299566, 0.184309, 1.46709]])
        
        # LMS to RGB
        self.rgb_matrix_inv = np.linalg.inv(self.lms_matrix)
        
        # Simulation matrices (Simulate color blindness)
        # Deuteranopia (Green-blind)
        self.sim_deuteranopia = np.array([[1, 0, 0],
                                          [0.494207, 0, 1.24827],
                                          [0, 0, 1]])
        
        # Error modification matrix (Shift colors)
        self.err_mod = np.array([[0, 0, 0],
                                 [0.7, 1, 0],
                                 [0.7, 0, 1]])

    def apply_correction(self, image):
        """
        Applies Daltonization to the image region.
        """
        # 1. Convert to float
        img_float = image.astype(float)
        
        # 2. Convert RGB to LMS
        # OpenCV uses BGR, so convert to RGB first
        img_rgb = cv2.cvtColor(img_float.astype(np.uint8), cv2.COLOR_BGR2RGB).astype(float)
        
        h, w = img_rgb.shape[:2]
        
        # Reshape for matrix multiplication
        img_flat = img_rgb.reshape(-1, 3).T # 3 x N
        
        lms = np.dot(self.lms_matrix, img_flat)
        
        # 3. Simulate color blindness (Deuteranopia)
        lms_sim = np.dot(self.sim_deuteranopia, lms)
        
        # 4. Calculate error (Difference between original and simulated)
        # We need original LMS for this, but usually we calculate error in RGB space or LMS space
        # Standard Daltonization: 
        # Error = Original - Simulated
        # Correction = Error * Modification_Matrix
        # Result = Original + Correction
        
        # Let's do it in RGB space as per some implementations, or LMS. 
        # Let's stick to a simplified approach often used:
        # 1. RGB -> LMS
        # 2. LMS -> LMS_Sim
        # 3. LMS_Sim -> RGB_Sim
        # 4. Err = RGB - RGB_Sim
        # 5. Correction = Err * Shift_Matrix
        # 6. Final = RGB + Correction
        
        rgb_sim = np.dot(self.rgb_matrix_inv, lms_sim)
        
        # Calculate error
        error = img_flat - rgb_sim
        
        # Apply correction
        correction = np.dot(self.err_mod, error)
        
        # Add correction to original
        dtpn = img_flat + correction
        
        # Clip and reshape
        dtpn = np.clip(dtpn, 0, 255)
        dtpn = dtpn.T.reshape(h, w, 3)
        
        # Convert back to BGR
        result = cv2.cvtColor(dtpn.astype(np.uint8), cv2.COLOR_RGB2BGR)
        
        return result
