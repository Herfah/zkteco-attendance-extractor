# 🚀 Quick Start Guide - 3 Minutes Setup

## One-Command Installation (Plug & Play)

### Step 1: Download & Install
Open Terminal and paste this single command:

```bash
cd ~/Downloads && git clone https://github.com/Herfah/zkteco-attendance-extractor.git && cd zkteco-attendance-extractor && bash install.sh
```

That's it! The installer will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create macOS app bundle
- ✅ Set up configuration files

### Step 2: Configure Your Device IP (2 minutes)

1. **Find your F22 device IP:**
   - On F22 device: Press Menu → System Settings → Network → TCP/IP Settings
   - Write down the IP (e.g., `192.168.1.201`)

2. **Update configuration:**
   ```bash
   nano ~/.env
   ```
   Change:
   ```
   DEVICE_IP=192.168.1.201
   ```
   Save: Press `Ctrl + X`, then `Y`, then `Enter`

### Step 3: Launch the App

**Option A - Click to Launch (Easiest):**
- Open Finder → Applications
- Double-click **"ZKTeco Attendance Extractor"**

**Option B - From Terminal:**
```bash
cd ~/zkteco-attendance-extractor
./start_app.sh
```

---

## First Time Use

1. ✅ App opens → Click **⚙️ Settings** (top right)
2. ✅ Verify your F22 device IP
3. ✅ Click **"Test Connection"** (should show success)
4. ✅ Click **Save**
5. ✅ Go to **Sync** tab
6. ✅ Click **"🔄 Sync Now"**
7. ✅ Wait for completion
8. ✅ Check **View Data** tab to see your attendance records

---

## That's All! 🎉

Your app is now ready to:
- 📥 Sync attendance data from F22
- 📊 View and filter records
- 📤 Export to CSV or Excel
- 🔄 Schedule automatic syncs

---

## Troubleshooting

### ❌ "Python not found"
```bash
# Install Python from: https://www.python.org/downloads/
# Then re-run the installer
```

### ❌ App won't launch
```bash
cd ~/zkteco-attendance-extractor
source venv/bin/activate
python main.py
```

### ❌ Can't connect to device
- Verify F22 IP address (check device menu)
- Ensure MacBook is on same WiFi network
- Check firewall allows port 4370
- Try: `ping 192.168.1.201` (replace with your IP)

### ❌ Permission denied on install
```bash
chmod +x install.sh
bash install.sh
```

---

## File Locations

| What | Where |
|------|-------|
| App | `~/Applications/ZKTeco Attendance Extractor.app` |
| Database | `~/.zkteco/attendance.db` |
| Exports | `~/Documents/ZKTeco_Exports/` |
| Config | `~/zkteco-attendance-extractor/.env` |

---

## Uninstall

To remove the application:
```bash
# Delete app from Applications
rm -rf ~/Applications/"ZKTeco Attendance Extractor.app"

# Optional: Delete database and configuration
rm -rf ~/.zkteco
```

---

## Need Help?

1. Check troubleshooting above
2. Read full README.md
3. Open issue on GitHub

**Enjoy! 🎯**
