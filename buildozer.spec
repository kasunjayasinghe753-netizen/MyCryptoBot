[app]
title = CryptoBot
package.name = cryptobot
package.domain = org.crypto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0.0

# Android පද්ධතියට ගැලපෙන ලෙස සීමා කරන ලද requirements
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

# GitHub Actions පරිසරයට හොඳින්ම ගැළපෙන API සංස්කරණ
android.api = 33
android.minapi = 21
android.ndk_path = 
android.sdk_path = 
android.clear_manifest = False
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
