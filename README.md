# **Multi-Agent System for Network Threat Detection**

This project simulates a **Multi-Agent-System-for-Network-Threat-Detection** using the PADE framework. It represents a network of devices (e.g., routers, laptops, phones) and a central switch agent. The agents collaborate to detect threats, mitigate them, and dynamically manage security levels across the network.

---

## **Table of Contents**
1. [Overview](#overview)
2. [System Components](#system-components)
3. [Features](#features)
4. [Technologies Used](#technologies-used)
5. [Installation and Setup](#installation-and-setup)
6. [Usage Instructions](#usage-instructions)
7. [Future Scope](#future-scope)
8. [License](#license)

---

## **Overview**

The **Cyber Threat Detection and Mitigation System** is designed to:
- Simulate a network of interconnected devices, each represented as an autonomous agent.
- Detect and mitigate cyber threats dynamically.
- Adjust security levels based on network conditions to prevent potential risks.

The system demonstrates how a central switch agent and multiple device agents can work collaboratively to ensure network security.

---

## **System Components**

1. **Switch Agent**:
   - Coordinates the network.
   - Handles threat notifications and manages security adjustments.
   - Ensures seamless communication between device agents.

2. **Device Agents**:
   - Represent individual devices (e.g., routers, laptops, and phones).
   - Autonomously detect threats and report them to the switch.
   - Respond to security adjustments and execute mitigation strategies.

3. **Devices**:
   - Simulated entities with properties like:
     - Device type (e.g., Router, Laptop).
     - Unique ID.
     - Threat status and security level.

---

## **Features**

- **Threat Detection**:
  - Device agents randomly detect threats and notify the switch agent.
  - Each device simulates real-world vulnerabilities.

- **Threat Mitigation**:
  - Devices autonomously execute mitigation strategies when instructed by the switch.
  - Mitigation is simulated with configurable time delays.

- **Dynamic Security Adjustment**:
  - During threats:
    - Security levels are increased across unaffected devices.
  - Post-mitigation:
    - Security levels return to normal.

- **Real-Time Monitoring**:
  - The system continuously displays the network status, showing:
    - Active threats.
    - Security levels of each device.

- **Asynchronous Execution**:
  - Multiple threads simulate concurrent device behaviors and interactions.

---

## **Technologies Used**

- **Programming Language**: Python
- **Framework**: PADE (Platform for Agents Development and Execution)
- **Threading**: For concurrent threat detection, mitigation, and monitoring.

---

## **Installation and Setup**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SandeepaDilshanAlagiyawanna/Multi-Agent-System-for-Network-Threat-Detection.git
   cd Multi-Agent-System-for-Network-Threat-Detection
   ```

2. **Install Dependencies**:
   Ensure Python 3.x is installed, then run:
   ```bash
   pip install pade
   ```

3. **Run the System**:
   ```bash
   python main.py
   ```

---

## **Usage Instructions**

1. **Start the System**:
   - Run the `main.py` file to initialize the agents and the switch.

2. **Monitor the Network**:
   - The terminal displays:
     - Threat notifications.
     - Security level adjustments.
     - Threat mitigation updates.

3. **Simulated Actions**:
   - Threat detection occurs at random intervals.
   - The switch agent coordinates mitigation and adjusts security levels dynamically.

---

## **Future Scope**

- **Integration with Real IoT Networks**:
  - Extend the simulation to interact with actual IoT devices for real-world applications.

- **Enhanced Threat Detection**:
  - Use machine learning models to improve detection accuracy.

- **Dynamic Network Expansion**:
  - Allow devices to join or leave the network dynamically during runtime.

- **Visualization Dashboard**:
  - Build a graphical interface to display network status and interactions visually. (Visualization folder includes HTML script, Just load in a Live Server or Run it.)

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

## **Contributing**

Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes and push the branch.
4. Submit a pull request.
