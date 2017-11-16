#!/bin/bash

find ./ -name '*.py' | entr -c py.test -v

