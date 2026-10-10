import time
import json
import urllib.request
import os
from pyjnius import autoclass, PythonJavaClass, java_method

PythonService = autoclass('org.kivy.android.PythonService')
BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
IntentFilter = autoclass('android.content.IntentFilter')

# সার্ভার ইউআরএল (আপনার Django Domain বা local IP)
SERVER_URL = "http://127.0.0.1:8000/api/upload-notification/"
CONFIG_FILE = "device_config.json"

def get_device_key():
    """সেভ করা Device Key পড়ার জন্য"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f).get("device_key", "")
    except Exception as e:
        print("Error reading config:", e)
    return ""

def send_to_django(app_name, sender, text):
    device_key = get_device_key()
    if not device_key:
        print("No Device Key found. Skipping send.")
        return

    payload = {
        "device_key": device_key,
        "app_name": app_name,
        "sender": sender,
        "text": text
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            SERVER_URL, 
            data=data, 
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("Successfully sent to Django:", resp.status)
    except Exception as e:
        print("Failed to send notification:", e)

# Java Broadcast গ্রহণের জন্য Class
class NotificationBroadcastReceiver(PythonJavaClass):
    __javainterfaces__ = ['android/content/BroadcastReceiver']
    __javacontext__ = 'app'

    @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
    def onReceive(self, context, intent):
        package_name = intent.getStringExtra("package") or ""
        title = intent.getStringExtra("title") or ""
        text = intent.getStringExtra("text") or ""
        
        print(f"[Service Captured]: {package_name} -> {title}: {text}")
        send_to_django(app_name=package_name, sender=title, text=text)

if __name__ == '__main__':
    service = PythonService.mService
    
    receiver = NotificationBroadcastReceiver()
    intent_filter = IntentFilter("org.kidwatch.NOTIFICATION_RECEIVED")
    service.registerReceiver(receiver, intent_filter)
    
    print("Background Service Running...")
    
    while True:
        time.sleep(1)