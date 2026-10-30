[app]
title = CryptoBot
package.name = cryptobot
package.domain = org.crypto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0.0

# වැදගත් වෙනස: Python සංස්කරණය ස්ථාවර 3.11 එකකට සීමා කිරීම සහ Kivy නිවැරදිව ලබා දීම
requirements = python3==3.11.9,kivy==2.3.0

orientation = portrait
fullscreen = 0

# GitHub Actions සඳහා වඩාත්ම ගැලපෙන ස්ථාවර Android API සංස්කරණ
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
