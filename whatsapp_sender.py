# whatsapp_sender.py

import random
from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = 'ACdf28ffd182ba57facb1dd76a48c8e97'
AUTH_TOKEN = 'c83be459bc8d1d195543062768a2d63'

FROM_WHATSAPP = 'whatsapp:+14155238886'
TO_WHATSAPP = 'whatsapp:+91709390832'  # 

def send_random_location():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    lat = f"17.52{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
    lon = f"78.36{random.randint(1000, 9999)}{random.randint(1000, 9999)}"

    body = f"📍 Device Location (simulated):\nLatitude: {lat}\nLongitude: {lon}"

    message = client.messages.create(
        from_=FROM_WHATSAPP,
        body=body,
        to=TO_WHATSAPP
    )

    print("✅ WhatsApp location message sent!")




# Wait for key input for 5 seconds
print("⌨️  Press 's' within 5 seconds to send WhatsApp location...", end=' ', flush=True)
i, o, e = select.select([sys.stdin], [], [], 5)
if i:
    key = sys.stdin.readline().strip()
    if key == 's':
        send_random_location()
    else:
        print("Invalid key pressed. Skipping WhatsApp send.")
else:
    print("\n⌛ No input. Continuing main loop...")
import sys
import select
from whatsapp_sender import send_random_location
