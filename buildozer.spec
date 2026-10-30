[app]
title = CryptoBot
package.name = cryptobot
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 1

# (⚠️ වැදගත්) Buildozer හිරවීම වැළැක්වීමට Android SDK බලපත්‍ර ස්වයංක්‍රීයව පිළිගැනීම
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
