content = '''[app]

title = KidWatch
package.name = kidwatch
package.domain = org.kidwatch

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,java,ttf

version = 0.1

requirements = python3,kivy==2.3.0,pyjnius,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf,pillow

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,POST_NOTIFICATIONS,FOREGROUND_SERVICE,FOREGROUND_SERVICE_DATA_SYNC

services = KidService:service.py

android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.copy_libs = 1

android.add_src = src

android.extra_manifest_xml = 
    <service
        android:name="org.kidwatch.NotificationService"
        android:permission="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE"
        android:exported="true">
        <intent-filter>
            <action android:name="android.service.notification.NotificationListenerService" />
        </intent-filter>
    </service>

[buildozer]
log_level = 2
warn_on_root = 0
'''

with open("buildozer.spec", "w") as f:
    f.write(content)

print("buildozer.spec created successfully!")