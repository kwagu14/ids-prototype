#!/bin/bash

# This file simulates the secure-boot function in the RO-IoT architecture.
# It works by deleting the IoT application process container and re-creating it
# with a clean image

# I am using a custom image I created with a dockerfile (app-env), so that the IoT 
# application is automatically injected and started in the container upon creation 

echo "[FROM SECURE-BOOT] Beginning secure boot process"
docker stop appEnv
echo "[FROM SECURE-BOOT] Stopped the application environment"
docker rm appEnv
echo "[FROM SECURE-BOOT] Removed the app environment"
docker run --device /dev/gpiomem -d -t --name appEnv app-env-clean:Dockerfile
echo "[FROM SECURE-BOOT] Completed re-imaging of app environment"
