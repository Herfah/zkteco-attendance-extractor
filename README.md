# ZKTeco Attendance Extractor

A cross-platform desktop GUI application to extract and manage attendance data from ZKTeco F22 biometric devices on macOS (and Linux/Windows).

## Features

✅ **Real-time Sync** - Pull attendance records from your ZKTeco F22 device  
✅ **Local Database** - SQLite database for secure data storage  
✅ **Advanced Filtering** - Filter by date range and user ID  
✅ **Multiple Export Formats** - CSV, Excel, and summary reports  
✅ **Device Management** - View device information and test connections  
✅ **Cross-platform** - Works on macOS, Linux, and Windows  

## Requirements

- Python 3.7+
- macOS 10.12+ / Linux / Windows
- ZKTeco F22 device on the same network
- Network access to device IP (TCP port 4370 by default)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Herfah/zkteco-attendance-extractor.git
cd zkteco-attendance-extractor
```

### 2. Create virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure device settings

```bash
cp .env.example .env
# Edit .env with your device IP and port
```

### 5. Run the application

```bash
python main.py
```

## Usage

### Finding Your Device IP

1. On your ZKTeco F22 device, go to **System Settings**
2. Navigate to **Network** → **TCP/IP Settings**
3. Note the IP address (e.g., `192.168.1.201`)

### Syncing Data

1. Open the application and go to the **Sync** tab
2. Click **"Sync Now"** button
3. The app will connect to your device and download all attendance records
4. Records are automatically saved to the local database

### Viewing Data

1. Go to the **View Data** tab
2. Set date range or user ID filter
3. Click **Apply Filter** to see matching records

### Exporting Data

1. Go to the **Export** tab
2. Choose export format:
   - **CSV** - Plain text format, easy to import
   - **Excel** - Full formatting with multiple sheets
   - **Summary Report** - Daily attendance overview
3. Click the appropriate export button
4. Files are saved to `~/Documents/ZKTeco_Exports/`

### Device Settings

1. Click **⚙️ Settings** button in the top-right
2. Configure:
   - Device IP address
   - Port (default: 4370)
   - Connection timeout
3. Click **Test Connection** to verify
4. Click **Save** to apply changes

## Database Location

- **macOS/Linux**: `~/.zkteco/attendance.db`
- **Windows**: `C:\Users\<YourUsername>\.zkteco\attendance.db`

## Export Location

- **All Platforms**: `~/Documents/ZKTeco_Exports/`

## Troubleshooting

### Connection Issues

**Problem**: "Failed to connect to device"

**Solutions**:
- Verify device IP is correct (check device display menu)
- Ensure MacBook is on same network as device
- Check firewall - allow port 4370 (TCP)
- Restart device if necessary
- Test with: `ping 192.168.1.201` (replace with your device IP)

### No Records Found

**Problem**: Sync completes but no records are saved

**Solutions**:
- Ensure device has attendance data
- Check device has TCP/IP enabled
- Verify user IDs exist on device
- Try disabling/enabling device from settings

### Database Errors

**Problem**: "SQLite database is locked"

**Solutions**:
- Close all instances of the application
- Delete corrupted database and restart (data will be re-synced)
  ```bash
  rm ~/.zkteco/attendance.db
  ```

## Configuration

Edit `.env` file to customize:

```env
# Device IP and port
DEVICE_IP=192.168.1.201
DEVICE_PORT=4370
DEVICE_TIMEOUT=5

# Auto-sync interval in minutes
AUTO_SYNC_INTERVAL=30
```

## File Structure

```
zkteco-attendance-extractor/
├── main.py                 # Main GUI application
├── config.py              # Configuration settings
├── database.py            # SQLite database handler
├── zk_device.py          # ZKTeco device communication
├── export_handler.py      # Data export functionality
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Development

To contribute or modify:

```bash
# Install in development mode
pip install -e .

# Run tests (when added)
python -m pytest
```

## Supported Devices

This application has been tested with:
- ✅ ZKTeco F22
- ✅ ZKTeco F18 (likely compatible)
- ✅ Most devices supporting ZKTeco push/pull protocol

Other ZKTeco devices may work but are untested.

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review device settings and network connectivity
3. Check application logs in terminal
4. Open an issue on GitHub

## Security Notes

⚠️ **Important**:
- Database contains sensitive attendance data - keep `.zkteco/` directory private
- Use strong network credentials for your ZKTeco device
- Don't share `.env` file with credentials
- Regular database backups are recommended

## Roadmap

Planned features:
- [ ] Automated scheduling (sync every N minutes)
- [ ] Multi-device support
- [ ] Email reports
- [ ] Web dashboard
- [ ] Cloud backup
- [ ] Biometric data extraction

## Changelog

### v1.0.0 (2026-09-14)
- Initial release
- Sync, view, and export functionality
- SQLite database
- CSV/Excel export
