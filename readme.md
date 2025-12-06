# Color Blindness Correction System

A real-time camera application that helps colorblind individuals see colors more accurately using advanced Daltonization algorithms.

## Overview

This software uses your camera as an "eye" and displays corrected colors on the screen, allowing colorblind individuals to perceive colors they normally cannot distinguish. The system supports three types of color blindness:

- **Protanopia** (Red-blind): Missing L-cones, difficulty distinguishing red from green
- **Deuteranopia** (Green-blind): Missing M-cones, difficulty distinguishing red from green
- **Tritanopia** (Blue-blind): Missing S-cones, difficulty distinguishing blue from yellow

## How It Works

The application uses the **Daltonization algorithm**, which:

1. Converts camera feed from RGB to LMS color space (matching human cone cells)
2. Simulates how a colorblind person would see the image
3. Calculates the difference (error) between normal and colorblind vision
4. Redistributes the "lost" color information to visible channels
5. Converts back to RGB for display

This process happens in real-time at 30+ FPS for smooth viewing.

## Installation

### Prerequisites
- Python 3.7 or higher
- A working webcam

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

That's it! The application is ready to run.

## Usage

### Running the Application

```bash
python colorblind_correction.py
```

### Controls

Once the application starts, you'll see your camera feed with an overlay showing the current mode and controls:

| Key | Action |
|-----|--------|
| **N** | Normal mode (no correction) |
| **P** | Protanopia correction (red-blind) |
| **D** | Deuteranopia correction (green-blind) |
| **T** | Tritanopia correction (blue-blind) |
| **Q** | Quit application |

### Tips for Best Results

1. **Good Lighting**: Ensure your environment is well-lit for accurate color correction
2. **Camera Quality**: Better cameras provide better color accuracy
3. **Distance**: Position yourself 1-2 feet from the camera for optimal results
4. **Test Different Modes**: Try all correction modes to see which works best for your specific type of color blindness

## Performance

- **Target FPS**: 30+ frames per second
- **Resolution**: 640x480 (default, adjustable in code)
- **Latency**: < 50ms for real-time experience

### Optimization Tips

If you experience low FPS:
- Close other applications using the camera
- Reduce resolution by modifying `width` and `height` in `main()` function
- Ensure good lighting to reduce camera processing time

## Technical Details

### Color Space Transformation

The application uses scientifically accurate transformation matrices:

- **RGB → LMS**: Converts standard RGB to Long, Medium, Short wavelength cone responses
- **LMS → RGB**: Inverse transformation back to displayable RGB
- **Simulation Matrices**: Based on research by Brettel, Viénot, and Mollon (1997)

### Algorithm Performance

- **Matrix Operations**: Optimized using NumPy for efficient computation
- **Vectorization**: All color transformations are vectorized for maximum speed
- **Memory Efficiency**: Processes frames in-place where possible

## Customization

You can customize the application by modifying parameters in `colorblind_correction.py`:

```python
# In main() function
app = ColorBlindnessApp(
    camera_id=0,      # Change if you have multiple cameras
    width=640,        # Adjust resolution
    height=480        # Adjust resolution
)
```

## Troubleshooting

### Camera Not Opening
- Check if another application is using the camera
- Try changing `camera_id` to 1 or 2 if you have multiple cameras
- On Windows, ensure camera permissions are enabled

### Low FPS
- Reduce resolution (e.g., 320x240)
- Close other applications
- Update graphics drivers

### Colors Look Wrong
- Ensure good lighting conditions
- Try different correction modes
- Check camera color calibration

## Scientific References

The Daltonization algorithm is based on:
- Brettel, H., Viénot, F., & Mollon, J. D. (1997). Computerized simulation of color appearance for dichromats. *Journal of the Optical Society of America A*, 14(10), 2647-2655.
- Fidaner, I. B., Aydin, T. O., & Çapın, T. K. (2005). *Adaptive Image Recoloring for Red-Green Dichromats*.

## License

This project is open source and available for educational and personal use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Acknowledgments

- OpenCV community for excellent computer vision tools
- Color blindness research community for algorithm development
- NumPy developers for efficient numerical computing
