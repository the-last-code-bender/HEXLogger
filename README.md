# H.E.XLogger
## Serial Port Data Logger

A simple yet effective Python-based serial port data logger.  
This tool allows users to record raw binary data from a selected serial port to a timestamped file, using either configuration presets or manual serial settings.

---

## 🔧 Features

- Lists and selects available serial ports
- Supports multiple saved configuration presets (`config.json`)
- Manual serial configuration mode
- Option to enable **automatic start/stop logging** based on data timeout
- Option to include a **counter in output filename** for auto-split mode
- Saves data to `ConfigName_001_YYYY_MM_DD_HH_MM_SS.bin` (if counter enabled) or `ConfigName_YYYY_MM_DD_HH_MM_SS.bin`
- **Waits for first data** before starting timeout tracking (improved auto-split behavior)
- Real-time byte count display
- Clean and minimal terminal UI
- Color-coded terminal output (via `colorama`)
- Cross-platform compatible (tested on Windows)

---

## 📦 Requirements

- Python 3.7+
- [PySerial](https://pypi.org/project/pyserial/)
- [Colorama](https://pypi.org/project/colorama/)

Install dependencies:
```bash
pip install -r requirements.txt
```