#!/bin/bash

cd /home/student334/Desktop/CPSC-334

echo "entering directory:" > log.txt
pwd >> log.txt

echo "saving ip address: " >> log.txt
hostname -I >> log.txt

hostname -I >> raspi/ip.md

echo "pushing to git..." >> log.txt
git add raspi/ip.md
git commit --allow-empty -m "update ip"
git push

echo "script was successfully triggered by $(whoami)" > log.txt

cd -
