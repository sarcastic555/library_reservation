#!/bin/bash

find ./ -name "*py" | xargs yapf -i
find ./ -name "*py" | xargs isort
pyflakes .
