#!/bin/bash

cd /home/student334/Desktop/CPSC-334
if ! git diff-index --quiet HEAD --; then
	git add ip.md
	git commit -m "update ip"
	git push
fi
cd -

echo "script was triggered by ${whoami}" > log.txt
$ip_address >> log.txt
