#!/bin/bash

# This file simulates the secure-boot function in the RO-IoT architecture.
# It works by deleting the IoT application process container and re-creating it
# with a clean image

# I am using a custom image I created with a dockerfile (app-env), so that the IoT 
# application is automatically injected and started in the container upon creation 

docker stop appEnv
docker rm appEnv
docker run --device /dev/gpiomem -d -t --name appEnv app-env:Dockerfile
