# H.E.XLogger
## Serial Port Data Logger

A simple yet effective Python-based serial port data logger.  
This tool allows users to record raw binary data from a selected serial port to a timestamped file, using either configuration presets or manual serial settings.

## 🔧 Features

- Lists and selects available serial ports
- Supports multiple saved configuration presets (`config_HEXLogger.json`)
- Manual serial configuration mode
- Option to enable **automatic start/stop logging** based on data timeout
- Option to include a **counter in output filename** for auto-split mode
- Saves data to `ConfigName-YYYY_MM_DD_HH_MM_SS-Data1.bin` (if counter enabled) or `ConfigName-YYYY_MM_DD_HH_MM_SS.bin`
- **Waits for first data** before starting timeout tracking (improved auto-split behavior)
- Real-time byte count display
- Clean and minimal terminal UI
- Color-coded terminal output (via `colorama`)
- Cross-platform compatible (tested on Windows)



## 📦 Requirements

- Python 3.7+
- [PySerial](https://pypi.org/project/pyserial/)
- [Colorama](https://pypi.org/project/colorama/)

Install dependencies:
```bash
pip install -r requirements.txt
```
--- 
# HEXArchiver 
## File Organizer for HEXLogger

`HEXArchiver` is a companion utility to [HEXLogger](#) that automatically **organizes recorded binary files** based on their configuration name and timestamp.

### 📂 What it does

This tool scans the current directory for `.bin` files produced by HEXLogger and arranges them into a structured folder hierarchy:

``` cpp
DATA/
└── ConfigName/
    └── YYYY_MM_DD/
        └── ConfigName-YYYY_MM_DD_HH_MM_SS[-optional].bin
```

✅ **Supported filename format examples**:
- `MyConfig-2025_06_14_10_15_30.bin`
- `SensorA-2025_06_13_08_00_00-Data1.bin`
- `SensorA-2025_06_13_08_00_00-Data1-fail.bin`
- `Config_X-2025_06_12_09_30_00_retry.bin`
- _(any suffix after timestamp is accepted)_

⚠ Files that **do not match** the expected pattern will be skipped.

### ▶ Usage

Place `HEXArchiver.py` in the same folder as your HEXLogger output files, and run:

```bash
python HEXArchiver.py
```


