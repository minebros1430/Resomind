[app]
title = ResoMind
package.name = resomind
package.domain = org.alhajji
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy,kivymd,numpy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.2.1
fullscreen = 0
android.permissions = INTERNET, MODIFY_AUDIO_SETTINGS
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True
[buildozer]
log_level = 2
warn_on_root = 1
