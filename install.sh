#!/bin/bash

# ZKTeco Attendance Extractor - Installation Script
# This script automates the complete installation process

set -e  # Exit on error

echo "=========================================="
echo "ZKTeco Attendance Extractor Installer"
echo "=========================================="
echo ""

# Check Python version
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7+ from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📦 Installing in: $SCRIPT_DIR"
echo ""

# Create virtual environment
echo "📝 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip upgraded"
echo ""

# Install requirements
echo "📦 Installing dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements.txt
echo "✅ All dependencies installed"
echo ""

# Create .env file if it doesn't exist
echo "⚙️  Setting up configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Configuration file created (.env)"
    echo "   ⚠️  IMPORTANT: Edit .env and set your F22 device IP address"
else
    echo "✅ Configuration file already exists"
fi
echo ""

# Create startup script
echo "🎯 Creating startup script..."
cat > start_app.sh << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
source venv/bin/activate
python main.py
EOF

chmod +x start_app.sh
echo "✅ Startup script created (start_app.sh)"
echo ""

# Create macOS app launcher using Automator
create_macos_app() {
    echo "🍎 Creating macOS Application Bundle..."
    
    APP_DIR="$HOME/Applications/ZKTeco Attendance Extractor.app"
    CONTENTS_DIR="$APP_DIR/Contents"
    MACOS_DIR="$CONTENTS_DIR/MacOS"
    RESOURCES_DIR="$CONTENTS_DIR/Resources"
    
    # Create directories
    mkdir -p "$MACOS_DIR"
    mkdir -p "$RESOURCES_DIR"
    
    # Create launcher script
    cat > "$MACOS_DIR/launcher.sh" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
source venv/bin/activate
python main.py
EOF
    
    chmod +x "$MACOS_DIR/launcher.sh"
    
    # Create Info.plist
    cat > "$CONTENTS_DIR/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>launcher.sh</string>
    <key>CFBundleIdentifier</key>
    <string>com.zkteco.attendance.extractor</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>ZKTeco Attendance Extractor</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.12</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
</dict>
</plist>
PLIST
    
    echo "✅ macOS app bundle created"
    echo "   Location: $APP_DIR"
}

# Check if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    create_macos_app
else
    echo "ℹ️  macOS app bundle creation skipped (not on macOS)"
fi
echo ""

# Deactivate virtual environment
deactivate

echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "📍 Next Steps:"
echo ""
echo "1️⃣  CONFIGURE DEVICE IP:"
echo "   nano .env"
echo "   Find your F22 device IP in: System Settings → Network → TCP/IP Settings"
echo "   Update: DEVICE_IP=YOUR_DEVICE_IP"
echo ""
echo "2️⃣  RUN THE APPLICATION:"
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   Option A (Easiest - Click to launch):"
    echo "   👉 Applications → ZKTeco Attendance Extractor"
    echo ""
    echo "   Option B (From terminal):"
    echo "   cd \"$SCRIPT_DIR\""
    echo "   ./start_app.sh"
else
    echo "   cd \"$SCRIPT_DIR\""
    echo "   ./start_app.sh"
fi

echo ""
echo "3️⃣  ON FIRST RUN:"
echo "   - Click ⚙️ Settings (top right)"
echo "   - Verify your F22 device IP"
echo "   - Click 'Test Connection'"
echo "   - Go to Sync tab and click '🔄 Sync Now'"
echo ""
echo "=========================================="
echo ""
