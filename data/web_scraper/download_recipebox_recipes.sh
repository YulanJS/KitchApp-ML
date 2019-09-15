#!/bin/bash

OUT_DIR=recipebox

if ls | grep -q "$OUT_DIR"/recipes.zip; then
	echo recipes.zip already downloaded
else
	mkdir -p "$OUT_DIR"
	wget https://storage.googleapis.com/recipe-box/recipes_raw.zip -O "$OUT_DIR"/recipes.zip
fi
unzip recipebox/recipes.zip -d "$OUT_DIR"
