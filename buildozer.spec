[app]
title = CryptoBot
package.name = cryptobot
package.domain = org.crypto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0.0

# වැදගත්: Kivy සමඟ සැබෑ බිල්ඩ් එකට අවශ්‍ය dependencies
requirements = python3,kivy==2.3.0,pillow

orientation = portrait
fullscreen = 0

# Android SDK සහ NDK API සංස්කරණ (GitHub Actions වලට ගැලපෙන ලෙස)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
