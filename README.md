# Modbus TCP CLI Tool Documentation

An interactive, professional-grade terminal utility for managing Modbus TCP server communications. This tool features a robust, class-based architecture and a polished interface using the `Rich` library.

**License:** MIT  
**Version:** 1.0

## 🛠 Prerequisites

Ensure you have Python 3.7+ installed. The tool depends on two primary libraries:

* **pyModbusTCP**: The core engine for protocol communication.
* **rich**: Provides the advanced terminal UI, status spinners, and tables.

### Installation

Install the required dependencies using pip:

```bash
pip install pyModbusTCP rich
```

## 🚀 Getting Started

Launch the tool by running the script:

```bash
python modbus_cli.py
```

### 1. Connection & Setup

1. **Server Configuration**: The tool will prompt for the **IP/DNS** and **Port**.
2. **Auto-Retry Logic**: If the server is offline, the tool uses a "status spinner" and will attempt to reconnect up to **5 times** (configurable) before timing out.
3. **Persistent Session**: Once connected, the session remains open until you manually quit.

## 📋 Features & Usage

### Read Holding Registers

* **Function**: Reads multiple sequential registers.
* **Data Visualization**: Displays a table containing:
  * **Offset**: Relative position from the start address.
  * **Address**: The absolute Modbus register address.
  * **Value (Dec)**: The integer value.
  * **Value (Hex)**: The hexadecimal representation (e.g., `0x00FF`).

### Write Single Register

* **Function**: Sends a specific integer value to a target register.
* **Validation**: Checks for success immediately.
* **Smart Error Mapping**: If the write fails, the tool translates Modbus Exception codes (only 01 and 03) into human-readable descriptions.

### Quit

* Type `q` or press `Ctrl+C` to close the socket connection safely and exit the application.

---

## ⚠️ Advanced Error Handling

The application maps internal Modbus codes to clear terminal messages:

| Code | Type | User-Friendly Message |
| :--- | :--- | :--- |
| **01** | Illegal Function | Server does not support the requested operation. |
| **03** | Illegal Data Value | The value is outside the allowed range for this register. |
| **00** | Timeout/Offline | The server is unreachable or the network is interrupted. |

---

## ⚙️ Configuration Variables

You can adjust these constants at the top of the `modbus_cli.py` file:

* `DEFAULT_IP`: The IP address pre-filled in the prompt.
* `UNIT_ID`: The Modbus Unit ID (Slave ID), typically set to `1`.
* `MAX_RETRIES`: Number of connection attempts before giving up.
* `RETRY_DELAY`: Seconds to wait between connection attempts.

---

## 📄 License

This project is licensed under the **MIT License**.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that the proper notice is included.
