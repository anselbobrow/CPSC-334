#!/bin/bash

cd /home/student334/Desktop/CPSC-334
if ! git diff-index --quiet HEAD --; then
	git add raspi/ip.md
	git commit -m "update ip"
	git push
fi
cd -

echo "script was triggered by `whoami`" > /home/student334/Desktop/log.txt
hostname -I >> log.txt
