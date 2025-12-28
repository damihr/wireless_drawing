# 🎨 Wireless Air Drawing

Draw in the air using hand gestures! Works both as a Python desktop application and as a web application on GitHub Pages.

## 🌐 Web Version (GitHub Pages)

**Draw online:** https://damihr.github.io/wireless_drawing/

The web version uses MediaPipe for JavaScript and runs entirely in your browser - no installation needed!

### Features:
- **Pinch to Draw** - Pinch your thumb and index finger together to draw
- **Fist to Erase** - Make a fist and use your hand like a mop to erase
- **Clear Canvas** - Press 'C' to clear the entire canvas
- Real-time hand tracking via webcam
- Beautiful UI with webcam background

### Controls:
- **Pinch** (thumb + index finger) = Draw with red line
- **Fist** (all fingers closed) = Erase like a mop
- **C** = Clear entire canvas
- **Q** = Quit (web version)

## 💻 Python Desktop Version

For running locally with Python.

### Requirements

- **Python 3.9** (recommended for macOS stability with MediaPipe)
- Webcam/camera
- macOS/Linux/Windows

### Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:damihr/wireless_drawing.git
   cd wireless_drawing
   ```

2. **Create a virtual environment:**
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Usage

1. **Run the Python version:**
   ```bash
   python air_draw.py
   ```

2. **Or use the web version:**
   - Open `index.html` in your browser
   - Or deploy to GitHub Pages (see below)

## 🚀 Deploying to GitHub Pages

1. **Push the repository to GitHub**
2. **Go to repository Settings → Pages**
3. **Select source:** Deploy from a branch
4. **Select branch:** `main` and folder: `/ (root)`
5. **Save**

Your drawing app will be live at: `https://damihr.github.io/wireless_drawing/`

## 📁 Files

- **`air_draw.py`** - Python desktop version (OpenCV + MediaPipe)
- **`index.html`** - Web version (MediaPipe JS + Canvas)
- **`requirements.txt`** - Python dependencies

## 🎮 Gestures

### Draw Mode
- Pinch your thumb and index finger together
- Move your hand to draw a red line
- The drawing follows the midpoint between your thumb and index finger

### Erase Mode
- Make a fist (all fingers closed)
- Move your hand over the drawing
- Your entire hand surface acts like a mop, erasing everything it touches

### Clear Canvas
- Press **C** key to clear the entire canvas
- Shows a confirmation message

## 🛠️ Troubleshooting

### Web Version
- **Camera not working:** Make sure you allow camera access when prompted
- **Hands not detected:** Ensure good lighting and keep hands visible
- **Performance issues:** Close other browser tabs, use Chrome/Edge for best performance

### Python Version
- **MediaPipe errors:** Use Python 3.9 and ensure dependencies are installed
- **Camera not found:** Check camera permissions and try different camera index
- **Drawing not smooth:** Ensure good lighting and stable hand position

## 📝 Notes

- The web version uses MediaPipe JavaScript SDK (runs entirely client-side)
- The Python version uses MediaPipe Python SDK (requires installation)
- Both versions support the same gestures and features
- Web version is optimized for modern browsers (Chrome, Edge, Firefox, Safari)
- Drawing uses an offscreen canvas for better performance

## License

MIT License

