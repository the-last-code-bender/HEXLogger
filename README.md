# H.E.XLogger
## Serial Port Data Logger

A simple yet effective Python-based serial port data logger.  
This tool allows users to record raw binary data from a selected serial port to a timestamped file, using a selected configuration preset or manual settings.

---

## 🔧 Features

- Lists available serial ports
- Supports multiple saved configuration presets (`config.json`)
- Manual serial configuration mode
- Saves data to `output_YYYY_MM_DD_HH_MM_SS.bin`
- Clean and minimal terminal UI
- Real-time byte count display
- Cross-platform compatible (tested on Windows)
- Color-coded terminal output (via `colorama`)

---

## 📦 Requirements

- Python 3.7+
- [PySerial](https://pypi.org/project/pyserial/)
- [Colorama](https://pypi.org/project/colorama/)

Install dependencies:
```bash
pip install -r requirements.txt
```