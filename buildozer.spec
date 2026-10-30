[app]
title = CryptoBot
package.name = cryptobot
package.domain = org.crypto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0.0

requirements = python3,kivy==2.3.0
android.gradle_dependencies = 
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE
orientation = portrait
fullscreen = 0

# කිසිදු පිටස්තර Path එකක් නැති පිරිසිදු Android බිල්ඩ් සැකසුම
android.api = 33
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
