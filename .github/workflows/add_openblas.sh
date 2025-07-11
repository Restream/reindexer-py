#!/bin/bash

OPENBLAS_SRC="/usr/lib64/libopenblas.so"
WHL_FILES=$(ls dist/*.whl)
while IFS= read -r whl_file; do
  unzip "$whl_file" -d unpacked
  cp "$OPENBLAS_SRC" "unpacked/pyreindexer.libs/libopenblas.so"
  cd unpacked
  zip -r "../$whl_file" .
  cd ..
  rm -rf unpacked
done <<< "$WHL_FILES"