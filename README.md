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

The commonly used ports for budtmo/docker-android are: 
6080 — noVNC web interface (the browser UI at http://localhost:6080) 
5554 — Android emulator console port 
5555 — ADB (Android Debug Bridge) connection port 
4723 — Appium server (only needed if you're using Appium for test automation 

*** STEPS TO SETUP ENVIRONMENT *** 
1) Go to folder C:\DockerProjects> 
NOTE: Use the budtmo/docker-android image. It contains the Android OS, an Emulator, and Appium all pre-configured in one container. 

2) Inside the folder run the following:  
docker run -d --name android-container --privileged --device /dev/kvm:/dev/kvm -p 5554:5554 -p 5555:5555 -p 4723:4723 -p 6080:6080 -v C:\DockerProjects\app:/root/tmp -e DEVICE="Samsung Galaxy S10" -e APPIUM=true -e WEB_VNC=true budtmo/docker-android:emulator_13.0 

Map the local apk file on C drive to the docker container --- docker cp C:\DockerProjects\app\bitbar-sample-app.apk android-container:/home/androidusr/bitbar-sample-app.apk 

3) Wait for 2 min (if Mobile Emulator doesn't show up at http://localhost:6080/; restart container) 

