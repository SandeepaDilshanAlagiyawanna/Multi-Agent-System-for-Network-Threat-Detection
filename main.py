import time
import threading
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage
import random

class Device:
    def __init__(self, device_type, id):
        self.device_type = device_type
        self.id = id
        self.is_threat = False
        self.security_level = 1
        self.last_threat_time = None

class DeviceAgent(Agent):
    def __init__(self, aid, device, switch_agent):
        super(DeviceAgent, self).__init__(aid=aid)
        self.device = device
        self.switch_agent = switch_agent
        self.threat_detection_interval = 10
        self.is_mitigating = False
        self.mitigation_time = 5

    def on_start(self):
        display_message(self.aid.localname, f"{self.device.device_type} {self.device.id} started.")
        # Register this agent with the switch
        #self.switch_agent.register_device(self.device.device_type, self.device.id, self)
        self.threat_detection_loop()

    def threat_detection_loop(self):
        def run_detection():
            while True:
                if not self.device.is_threat and random.random() < 0.3:
                    self.device.is_threat = True
                    self.device.last_threat_time = time.time()
                    display_message(self.aid.localname, 
                                  f"⚠️ ALERT: Threat detected on {self.device.device_type} {self.device.id}")
                    self.notify_switch()
                    time.sleep(2)  # Add a small delay to slow down the threat detection
                time.sleep(self.threat_detection_interval)

        thread = threading.Thread(target=run_detection)
        thread.daemon = True
        thread.start()

    def notify_switch(self):
        # Directly notify the switch agent of the detected threat
        self.switch_agent.handle_threat(self.device.device_type, self.device.id)

    def start_mitigation(self):
        if not self.is_mitigating:
            self.is_mitigating = True
            
            def mitigate():
                display_message(self.aid.localname, 
                              f"🛡️ Starting threat mitigation on {self.device.device_type} {self.device.id}")
                time.sleep(self.mitigation_time)
                self.device.is_threat = False
                self.is_mitigating = False
                self.switch_agent.report_mitigation(self.device.device_type, self.device.id)
                display_message(self.aid.localname, 
                              f"✅ Threat mitigated on {self.device.device_type} {self.device.id}")

            thread = threading.Thread(target=mitigate)
            thread.daemon = True
            thread.start()

    def increase_security(self):
        # Increase security by one level
        if self.device.security_level < 3:
            self.device.security_level += 1
        display_message(self.aid.localname, 
                      f"⬆️ {self.device.device_type} {self.device.id} security increased to {self.device.security_level}")
    
    def decrease_security(self):
        # Decrease security by one level
        if self.device.security_level > 0:
            self.device.security_level -= 1
        display_message(self.aid.localname, 
                      f"⬇️ {self.device.device_type} {self.device.id} security decreased to {self.device.security_level}")


class SwitchAgent(Agent):
    def __init__(self, aid, agents):
        super(SwitchAgent, self).__init__(aid=aid)
        self.device_agents = {}  # Store device agents by type and ID
        self.active_threats = set()
        self.agents = agents  # Store the list of agents

    def on_start(self):
        display_message(self.aid.localname, "Switch started and ready to handle devices.")

    def register_device(self, device_type, device_id, device_agent):
        # Directly store the device agent
        self.device_agents[(device_type, device_id)] = device_agent
        display_message(self.aid.localname, f"📝 Registered {device_type} {device_id}")

    def handle_threat(self, device_type, device_id):
        threat_id = (device_type, device_id)
        self.active_threats.add(threat_id)

        # Instruct the affected device to start mitigation
        display_message(self.aid.localname, f"🛡️ Instructing {device_type} {device_id} to start mitigation")
        self.notify_device_mitigation(device_type, device_id)
        time.sleep(1)  # Slow down the flow after notifying mitigation

        # Notify other devices to increase security (excluding the device with the threat)
        self.notify_security_increase(device_type, device_id)
        time.sleep(1)  # Slow down after notifying security increase

    def report_mitigation(self, device_type, device_id):
        threat_id = (device_type, device_id)
        self.active_threats.discard(threat_id)
        display_message(self.aid.localname, f"✅ {device_type} {device_id} has mitigated the threat")
        time.sleep(1)  # Add a delay to slow down the reporting process

        # If no active threats, notify all devices to decrease security
        if not self.active_threats:
            self.notify_security_decrease()

    def notify_device_mitigation(self, device_type, device_id):
        # Directly call the device agent to start mitigation
        device_agent = self.device_agents.get((device_type, device_id))
        if device_agent:
            device_agent.start_mitigation()

    def notify_security_increase(self, device_type, device_id):
        # Notify other devices to increase security (except the one with the threat)
        for (other_device_type, other_device_id), device_agent in self.device_agents.items():
            if (other_device_type, other_device_id) != (device_type, device_id):
                display_message(self.aid.localname, f"⬆️ Notifying {other_device_type} {other_device_id} to increase security")
                device_agent.increase_security()
                time.sleep(1)  # Add a delay to slow down the notification of security increase

    def notify_security_decrease(self):
        # Decrease security for all devices if no threats
        for (device_type, device_id), device_agent in self.device_agents.items():
            display_message(self.aid.localname, f"⬇️ Notifying {device_type} {device_id} to decrease security")
            device_agent.decrease_security()
            time.sleep(1)  # Add a delay to slow down the notification of security decrease


def find_free_port():
    """Find a free port to use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def create_network():
    agents = []
    
    switch_port = find_free_port()
    switch_aid = AID(name=f"switch@localhost:{switch_port}")
    switch_agent = SwitchAgent(switch_aid, agents)  # Pass the agents list to the SwitchAgent
    agents.append(switch_agent)
    
    devices = [
        ("Router", 1), ("Laptop", 1), ("Laptop", 2),
        ("Phone", 1), ("Phone", 2)
    ]
    
    for dev_type, dev_id in devices:
        port = find_free_port()
        device = Device(dev_type, dev_id)
        agent = DeviceAgent(AID(name=f"{dev_type.lower()}{dev_id}@localhost:{port}"), device, switch_agent)
        agents.append(agent)  # Ensure the agent is added here
        # Register device with switch
        switch_agent.register_device(dev_type, dev_id, agent)
    
    return agents



def start_network():
    agents = create_network()
    
    def display_status():
        while True:
            print("\n=== Network Status ===")
            for agent in agents:
                if isinstance(agent, DeviceAgent):
                    print(f"{agent.device.device_type} {agent.device.id}:")
                    print(f"  Threat: {agent.device.is_threat}")
                    print(f"  Security Level: {agent.device.security_level}")
            print("===================\n")
            time.sleep(5)  # Adjust this delay to make the status update slower
    
    status_thread = threading.Thread(target=display_status)
    status_thread.daemon = True
    status_thread.start()
    
    start_loop(agents)

if __name__ == "__main__":
    start_network()
