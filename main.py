name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
    - uses: actions/checkout@v4

    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install Buildozer Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libssl-dev cmake libffi-dev libltdl-dev
        pip3 install --user --upgrade buildozer cython virtualenv

    - name: Build with Buildozer
      run: |
        export PATH=$PATH:$HOME/.local/bin
        yes | buildozer -v android debug
      continue-on-error: false

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: CryptoBot-APK
        path: bin/*.apk
