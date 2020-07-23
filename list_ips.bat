@echo off
echo Server
docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" facial_gesture_recognition