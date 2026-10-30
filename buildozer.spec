[app]
title = CryptoBot
package.name = cryptobot
package.domain = org.crypto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0.0

requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

# වැදගත්ම නිවැරදි කිරීම: ස්වයංක්‍රීය බාගත කිරීම් අක්‍රිය කර Workflow එකෙන් එන Paths ලබා ගැනීම
android.api = 33
android.minapi = 21
android.sdk_path = %(ANDROID_SDK_PATH)s
android.ndk_path = %(ANDROID_NDK_PATH)s
android.skip_setup = True

android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
