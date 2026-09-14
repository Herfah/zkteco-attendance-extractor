# Complete Installation & Setup Guide

## Table of Contents
1. [Automatic Installation (Recommended)](#automatic-installation-recommended)
2. [Manual Installation](#manual-installation)
3. [First Time Setup](#first-time-setup)
4. [Running the App](#running-the-app)
5. [Updating](#updating)
6. [Uninstalling](#uninstalling)
7. [Troubleshooting](#troubleshooting)

---

## Automatic Installation (Recommended)

### One-Command Setup

Copy and paste this in Terminal:

```bash
cd ~/Downloads && git clone https://github.com/Herfah/zkteco-attendance-extractor.git && cd zkteco-attendance-extractor && bash install.sh
```

### What the installer does:
✅ Verifies Python 3.7+ is installed  
✅ Creates isolated Python environment  
✅ Installs all dependencies  
✅ Sets up configuration files  
✅ Creates macOS app bundle (if on Mac)  
✅ Creates launch scripts  

**Time needed:** ~2-3 minutes (depends on internet speed)

---

## Manual Installation

If you prefer to install step-by-step:

### Step 1: Clone Repository
```bash
git clone https://github.com/Herfah/zkteco-attendance-extractor.git
cd zkteco-attendance-extractor
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Settings
```bash
cp .env.example .env
# Edit .env with your F22 device IP
nano .env
```

---

## First Time Setup

### 1. Find Your F22 Device IP

On the F22 device:
1. Press **Menu** button
2. Navigate to **System Settings**
3. Select **Network**
4. Select **TCP/IP Settings**
5. Write down the **IP Address** (e.g., `192.168.1.201`)

### 2. Update Configuration

```bash
nano .env
```

Change this line:
```
DEVICE_IP=192.168.1.201  # Replace with your actual IP
```

Save: Press `Ctrl + X`, then `Y`, then `Enter`

### 3. Test Connection

```bash
# Verify device is reachable
ping 192.168.1.201  # Replace with your IP
```

Should see responses like `64 bytes from 192.168.1.201`

---

## Running the App

### macOS - Click to Launch (Easiest)

1. Open **Finder**
2. Go to **Applications**
3. Double-click **"ZKTeco Attendance Extractor"**

### macOS/Linux/Windows - From Terminal

```bash
cd ~/zkteco-attendance-extractor
./start_app.sh
```

Or simply:
```bash
bash ~/zkteco-attendance-extractor/run.sh
```

### macOS - Create Spotlight Shortcut

After installing, the app appears in Spotlight:
1. Press `Cmd + Space`
2. Type "ZKTeco"
3. Press `Enter`

---

## Updating

To update to the latest version:

```bash
cd ~/zkteco-attendance-extractor
bash update.sh
```

The update script will:
✅ Check for new versions  
✅ Download latest code  
✅ Update dependencies  
✅ Preserve your database and settings  

---

## Uninstalling

### Option 1: Keep Data (Recommended)

Kill only the app, keep database and exports:

```bash
bash ~/zkteco-attendance-extractor/uninstall.sh
```

Choose to keep:
- ✅ Database (`~/.zkteco/attendance.db`)
- ✅ Exports (`~/Documents/ZKTeco_Exports/`)
- Remove: App and source code

### Option 2: Complete Removal

Delete everything:

```bash
# Remove app
rm -rf ~/Applications/"ZKTeco Attendance Extractor.app"

# Remove database
rm -rf ~/.zkteco

# Remove exports
rm -rf ~/Documents/ZKTeco_Exports

# Remove source code
rm -rf ~/zkteco-attendance-extractor
```

---

## Troubleshooting

### Python Issues

**Problem:** `Python 3 not found`

**Solution:**
```bash
# Install Python from https://www.python.org/downloads/
# Then run installer again:
bash install.sh
```

**Check version:**
```bash
python3 --version
# Should show: Python 3.7 or higher
```

### Connection Issues

**Problem:** "Failed to connect to device"

**Solutions:**
```bash
# 1. Verify device IP is correct
ping 192.168.1.201  # Replace with your IP

# 2. Check firewall allows port 4370
# macOS: System Preferences → Security & Privacy → Firewall

# 3. Restart device
# Power off F22 for 30 seconds, then power on

# 4. Update .env with correct IP
nano .env
DEVICE_IP=YOUR_CORRECT_IP
```

### No Records Found

**Problem:** Sync completes but no attendance records appear

**Solutions:**
1. Verify F22 device has attendance data
2. Check device has TCP/IP enabled
3. Confirm users exist on device
4. Try manual sync from app

### Database Locked

**Problem:** "SQLite database is locked"

**Solution:**
```bash
# Close all app instances
# Then reset database (will be re-synced on next run):
rm ~/.zkteco/attendance.db
```

### Permission Denied

**Problem:** `Permission denied` when running scripts

**Solution:**
```bash
chmod +x install.sh
chmod +x uninstall.sh
chmod +x update.sh
bash install.sh
```

### M1/M2 Mac Issues

**Problem:** PyQt5 installation fails on Apple Silicon

**Solution:**
```bash
# Install Miniforge from: https://github.com/conda-forge/miniforge
conda create -n zkteco python=3.10
conda activate zkteco
pip install -r requirements.txt
python main.py
```

---

## System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| Python | 3.7 | 3.9+ |
| macOS | 10.12 | 11.0+ |
| RAM | 512 MB | 2 GB |
| Disk Space | 500 MB | 2 GB |
| Network | 1 Mbps | 10 Mbps |

---

## File Locations

| Item | Location |
|------|----------|
| App Bundle | `~/Applications/ZKTeco Attendance Extractor.app` |
| Source Code | `~/zkteco-attendance-extractor/` |
| Database | `~/.zkteco/attendance.db` |
| Configuration | `~/zkteco-attendance-extractor/.env` |
| Exports | `~/Documents/ZKTeco_Exports/` |
| App Data | `~/.zkteco/` |

---

## Scripts Reference

```bash
# Install/Setup
bash install.sh

# Run the app
./start_app.sh
# or
bash run.sh

# Check for updates
bash update.sh

# Uninstall
bash uninstall.sh
```

---

## Need Help?

1. **Read QUICK_START.md** for basic setup
2. **Check troubleshooting section above**
3. **Review terminal output** for error messages
4. **Open issue** on [GitHub](https://github.com/Herfah/zkteco-attendance-extractor/issues)

---

## Support

For issues or questions:
- 📖 Check this installation guide
- 🔍 Review troubleshooting section
- 🐛 Open issue on GitHub
- 📧 Contact: Check GitHub repository

**Happy syncing! 🎉**