#!/bin/bash

# isort should be applied first to avoid conflict
for file in `find ./ -name "*py"`; do
  isort -l 100 ${file} # use same line length as .style.yapf
done

for file in `find ./ -name "*py"`; do
  yapf -i ${file}
done

pyflakes .
