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

def get_output_filename(config,file_count=""):
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    base_name = config.get("name", "Unnamed").replace(" ", "_")
    return f"{base_name}{file_count}_{now}.bin"

def start_logging(ser, config, stop_flag, auto_split=False, timeout_seconds=None, use_auto_cnt=False):
    total_bytes = 0
    file_count = 1
    last_data_time = None  # Başlangıçta veri gelmedi

    def get_new_file():
        if use_auto_cnt:
            filename = get_output_filename(config, f"_{file_count}")
        else:
            filename = get_output_filename(config, "")
        f = open(filename, 'wb')
        print(f"\nRecording to: {filename}")
        return f

    current_file = get_new_file()

    while not stop_flag["stop"]:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            current_file.write(data)
            current_file.flush()
            total_bytes += len(data)
            last_data_time = time.time()
            sys.stdout.write(f"\r\033[1;31mTotal written: {total_bytes} bytes\033[0m")
            sys.stdout.flush()
        else:
            time.sleep(0.05)

        if auto_split and timeout_seconds and last_data_time is not None:
            if (time.time() - last_data_time) > timeout_seconds:
                current_file.close()
                file_count += 1
                current_file = get_new_file()
                total_bytes = 0
                last_data_time = None

    current_file.close()

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
v2.0.0 - Serial Port Data Logger
Created by Husamettin Eken
    """
    print(asciart)

    port = select_serial_port()
    config = load_config()
    if config is None:
        config = prompt_for_config()

    use_auto_stop = input("Enable auto-start/stop recording based on data timeout? (y/n): ").lower().strip() == 'y'
    timeout_seconds = None
    if use_auto_stop:
        try:
            timeout_seconds = float(input("Enter timeout duration in seconds (when no data is received): ").strip())
        except ValueError:
            print("Invalid input. Using default timeout of 3 seconds.")
            timeout_seconds = 3.0
    use_auto_cnt = False
    if use_auto_stop:
        use_auto_cnt = input("Include a counter in the filename for auto-split recordings (y/n): ").lower().strip() == 'y'   

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
        ser.set_buffer_size(rx_size=61440, tx_size=61440)
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        return

    stop_flag = {"stop": False}
    read_thread = threading.Thread(
        target=start_logging,
        args=(ser, config, stop_flag, use_auto_stop, timeout_seconds,use_auto_cnt)
    )
    input_thread = threading.Thread(target=keyboard_listener, args=(stop_flag,))

    input_thread.start()
    read_thread.start()
    
    input_thread.join()
    read_thread.join()

    ser.close()
    print("\nRecording stopped. Serial port closed.")
    input("Press Enter to exit...")
    colorama.deinit()

if __name__ == "__main__":
    main()