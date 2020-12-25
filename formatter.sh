#!/bin/bash

# isort should be applied first to avoid conflict
for file in `find ./ -name "*py"`; do
  isort ${file}
done

for file in `find ./ -name "*py"`; do
  yapf -i ${file}
done

pyflakes .
