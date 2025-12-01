# ML Visions Santa Hat

Projector-camera calibration and live feed system.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or in VSCode: `Ctrl+Shift+P` → "Python: Create Environment" → select venv

## Usage

1. Connect camera (`/dev/video0`) and projector
2. Activate venv: `source .venv/bin/activate`
3. Run: `python ThomasStarterScript.py`
4. Position camera using preview window, press Enter in the camera preview window when ready
5. Wait for calibration circles (~40 seconds)
6. Live warped feed will display on projector

## Platforms

- **Dev**: Ubuntu Linux (Thomas's laptop, Colin's laptop/22.04)
- **Deploy**: NVIDIA Jetson Orin Nano Super (Colin maintains via VSCode Remote SSH)

## Notes

- Python 3.10+ required (3.10 on Jetson JetPack 6.2, 3.12 on Ubuntu 24.04)
- If you get Qt/display errors, try: `QT_QPA_PLATFORM=xcb python ThomasStarterScript.py`

## Contributors

- Thomas - Core implementation
- Colin - Jetson deployment & maintenance
