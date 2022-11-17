#!/bin/bash

while ! ping -c1 github.com
do
echo "Connecting to github..."
sleep 1
done

cd /home/student334/Desktop/CPSC-334

git pull

hostname -I > raspi/ip.md

cp ~/.bashrc config/.bashrc

git add -A
git commit --allow-empty -m "update ip"
git push
