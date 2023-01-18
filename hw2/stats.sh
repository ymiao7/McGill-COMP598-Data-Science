#!/bin/bash

grep "" $1 | wc -l
head -n 1 $1
tail -n 10000 $1 | grep -i "potus" | wc -l
sed -n 101,201p $1 | grep "fake" | wc -l
