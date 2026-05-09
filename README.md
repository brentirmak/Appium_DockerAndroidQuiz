# Appium_Docker
This repo is for an Appium script that run against a configuration on Docker Desktop (budtmo/docker-android:emulator_13.0)
| Service                               | Purpose                   | Default Port |
| ------------------------------------- | ------------------------- | ------------ |
| Android Emulator                      | Virtual Android 13 device | internal     |
| ADB                                   | Android debugging bridge  | `5555`       |
| Appium (optional in some tags/setups) | Mobile test automation    | `4723`       |
| noVNC                                 | Browser desktop access    | `6080`       |
| VNC server                            | Remote desktop backend    | `5900`       |
| X11 / XFCE desktop                    | Linux GUI environment     | internal     |
