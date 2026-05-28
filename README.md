<b>Background</b>
This repo is for an Appium script that run against a configuration on Docker Desktop (budtmo/docker-android:emulator_13.0)<br>

The commonly used ports for budtmo/docker-android are: <br>
6080 — noVNC web interface (the browser UI at http://localhost:6080)<br> 
5554 — Android emulator console port <br>
5555 — ADB (Android Debug Bridge) connection port<br> 
4723 — Appium server (only needed if you're using Appium for test automation<br> 

<b>*** STEPS TO SETUP ENVIRONMENT ***</b> 
1) Go to folder C:\DockerProjects> <br>
NOTE: Use the budtmo/docker-android image. It contains the Android OS, an Emulator, and Appium all pre-configured in one container.<br> 

2) Inside the folder run the following:  <br>
docker run -d --name android-container --privileged --device /dev/kvm:/dev/kvm -p 5554:5554 -p 5555:5555 -p 4723:4723 -p 6080:6080 -v C:\DockerProjects\app:/root/tmp -e DEVICE="Samsung Galaxy S10" -e APPIUM=true -e WEB_VNC=true budtmo/docker-android:emulator_13.0<br> 

Map the local apk file on C drive to the docker container --- docker cp C:\DockerProjects\app\bitbar-sample-app.apk android-container:/home/androidusr/bitbar-sample-app.apk <br>

3) Wait for 2 min (if Mobile Emulator doesn't show up at http://localhost:6080/; restart container)

