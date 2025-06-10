import serial, json,  os, sys, threading, time, shutil, colorama
import serial.tools.list_ports
from datetime import datetime

CONFIG_FILE = "config.json"

def clear_lines(n):
    for _ in range(n):
        sys.stdout.write("\033[K")  # Clear line
        sys.stdout.write("\033[1A")  # Move up
    sys.stdout.write("\033[K")  # Clear final line
    sys.stdout.flush()

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def select_serial_port():
    ports = list_serial_ports()
    if not ports:
        print("No serial ports found.")
        input("Press any key to continue...")
        sys.exit(1)

    print("Available serial ports:")
    printed_lines = 1

    for i, port in enumerate(ports):
        print(f"{i + 1}: {port}")
        printed_lines += 1

    choice = int(input("Select port number: "))
    printed_lines += 1  
    
    clear_lines(printed_lines)

    print(f"Selected port: {ports[choice - 1]}")
    return ports[choice - 1]


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("No config file found in directory. -config.json")
        configfileformat = r"""
    Expected config file format:
        [{
            "name": "Default Preset",
            "baudrate": 921600,
            "stopbits": 1,
            "bytesize": 8,
            "parity": "N",
            "xonxoff": false,
            "rtscts": false
        },
        ....]
        """
        print(configfileformat)
        return None

    with open(CONFIG_FILE, 'r') as f:
        configs = json.load(f)

    if not isinstance(configs, list):
        print("Config file must contain a list of presets.")
        return None

    print("Available configurations:")
    printed_lines = 1
    for i, cfg in enumerate(configs):
        label = cfg.get("name", f"Preset {i + 1}")
        print(f"{i + 1}: {label}")
        printed_lines += 1

    selected = int(input("Select configuration: "))
    printed_lines += 1

    clear_lines(printed_lines)
    selectedconfig = configs[selected - 1]
    print(f"Selected configuration: {selectedconfig.get("name", "Unnamed Preset")}")
    return selectedconfig

def prompt_for_config():
    print("Enter serial port configuration manually:")
    questions = [
        "Baudrate: ",
        "Stop bits (1, 1.5, 2): ",
        "Data bits (5, 6, 7, 8): ",
        "Parity (N, E, O, M, S): ",
        "Software flow control (xon/xoff)? (y/n): ",
        "Hardware flow control (RTS/CTS)? (y/n): "
    ]

    answers = []
    for q in questions:
        answers.append(input(q))

    printed_lines = len(questions) + 1

    clear_lines(printed_lines)

    cfg = {
        "baudrate": int(answers[0]),
        "stopbits": float(answers[1]),
        "bytesize": int(answers[2]),
        "parity": answers[3].upper(),
        "xonxoff": answers[4].lower() == 'y',
        "rtscts": answers[5].lower() == 'y'
    }

    print("Manual configuration selected:")
    print(json.dumps(cfg, indent=4))
    return cfg

def get_output_filename(config):
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return f"output_{config.get("name", "Unnamed")}_{now}.bin"

def start_logging(ser, output_file, stop_flag):
    total_bytes = 0
    with open(output_file, 'wb') as f:
        while not stop_flag["stop"]:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting)
                f.write(data)
                f.flush()
                total_bytes += len(data)
                sys.stdout.write(f"\r\033[1;31mTotal written: {total_bytes} bytes\033[0m")
                sys.stdout.flush()
            else:
                time.sleep(0.05)

def keyboard_listener(stop_flag):
    input("\nPress Enter to stop recording...\n")
    stop_flag["stop"] = True

def main():
    colorama.init()
    asciart = r"""
    __  __  ______ _  __ __                               
   / / / / / ____/| |/ // /   ____  ____ _____ ____  _____
  / /_/ / / __/   |   // /   / __ \/ __ `/ __ `/ _ \/ ___/
 / __  / / /____ /   |/ /___/ /_/ / /_/ / /_/ /  __/ /    
/_/ /_(_)_____(_)_/|_/_____/\____/\__, /\__, /\___/_/     
                                 /____//____/                    
v1.1.0 - Serial Port Data Logger
Created by Husamettin Eken
    """
    print(asciart)
    port = select_serial_port()

    config = load_config()
    if config is None:
        config = prompt_for_config()

    try:
        ser = serial.Serial(
            port=port,
            baudrate=config["baudrate"],
            stopbits=float(config["stopbits"]),
            bytesize=int(config["bytesize"]),
            parity=config["parity"],
            xonxoff=config["xonxoff"],
            rtscts=config["rtscts"],
            timeout=0.1
        )
        ser.set_buffer_size(rx_size = 61440, tx_size = 61440)
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        return

    output_file = get_output_filename(config)
    print(f"Recording to: {output_file}")

    stop_flag = {"stop": False}
    read_thread = threading.Thread(target=start_logging, args=(ser, output_file, stop_flag))
    input_thread = threading.Thread(target=keyboard_listener, args=(stop_flag,))

    read_thread.start()
    input_thread.start()

    input_thread.join()
    read_thread.join()

    ser.close()
    print("\nRecording stopped. Serial port closed.")
    input("Press any key to continue...")
    colorama.deinit()

if __name__ == "__main__":
    main()