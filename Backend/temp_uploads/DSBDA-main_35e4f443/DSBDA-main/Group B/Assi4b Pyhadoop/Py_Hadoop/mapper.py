#!usr/bin/env python3
import sys
import io

input_stream = io.TextIOWrapper(sys.stdin.buffer)

for line in input_stream:
	words = line.strip().split()
	for word in words:
		print(f"{word}\t1")
