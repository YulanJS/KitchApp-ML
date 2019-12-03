#!/bin/bash

root="$1"

echo "Flattening folders under $root"
cd "$root"
pwd
for folder in `ls -d -- */`; do
	cd "$folder"
	find . -mindepth 2 -type f -exec mv -t . -n '{}' +
	find . -mindepth 1 -type d -empty -delete
	cd ..
done
echo "Done!"
