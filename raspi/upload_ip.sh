#!/bin/bash

cd /home/student334/Desktop/CPSC-334

git pull

hostname -I > raspi/ip.md

git add raspi/ip.md
git commit -m "update ip"
git push
