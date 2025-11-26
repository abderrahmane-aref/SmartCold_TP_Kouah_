import random
import time
import requests

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6000

while True:
    capteurs = []

    # Generate 6 sensors
    for i in range(6):
        temperature = round(random.uniform(20, 50), 1)
        humidite = round(random.uniform(40, 90), 1)

        capteurs.append({
            "id": i+1,
            "temperature": temperature,
            "humidite": humidite
        })

    try:
        res = requests.post(f"http://{SERVER_IP}:{SERVER_PORT}/send", json=capteurs)
        if res.status_code == 200:
            print("✔ Sent 6 capteurs")
    except Exception as e:
        print("❌ Error:", e)

    time.sleep(3)
