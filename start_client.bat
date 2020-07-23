@echo off
for /f %%i in ('docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" facial_gesture_recognition') do set SIP=%%i
echo facial server ip is %SIP%
python client/client.py -s 127.0.0.1 40000