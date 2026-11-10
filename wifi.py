import time
from pywifi import PyWiFi, const

def scan_wifi_devices():
    wifi = PyWiFi()
    interfaces = wifi.interfaces()

    if not interfaces:
        print("No Wi-Fi adapter found!")
        return

    interface = interfaces[0]

    print("\nScanning nearby Wi-Fi networks...")
    interface.scan()
    time.sleep(5)

    results = interface.scan_results()

    print("\n========== NEARBY WIFI NETWORKS ==========\n")

    for i, network in enumerate(results, start=1):
        print(f"Device Number : {i}")
        print(f"SSID          : {network.ssid}")
        print(f"BSSID         : {network.bssid}")
        print(f"Signal Strength: {network.signal} dBm")
        print(f"Security      : {network.akm}")
        print("-" * 4)

if __name__ == "__main__":
    scan_wifi_devices()
