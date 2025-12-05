# Color Blindness Simulation & Filter (CBSF)

## Prerequisites
- Python 3.8+
- Webcam

## Quick Start (Windows PowerShell)

Copy and paste these commands into your PowerShell terminal one by one:

1.  **Create a virtual environment**:
    ```powershell
    python -m venv venv
    ```

2.  **Activate the virtual environment**:
    ```powershell
    .\venv\Scripts\Activate
    ```
    *(You should see `(venv)` appear at the start of your command line)*

3.  **Install dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```powershell
    python main.py
    ```

## Usage
- The application will open a window showing your webcam feed.
- It will automatically detect **traffic lights** and **stop signs**.
- Detected objects will have a **color correction filter** applied to their bounding box.
- Press **'q'** to quit the application.
