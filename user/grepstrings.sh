#!/bin/bash

# Store the file in which strings will be printed
file="strings.txt"

# Store the list of strings which will be grep'ed
list="list.txt"

# Print the strings of the file
echo "Printing the strings in the file $file:"
cat $file

# Grep the strings from the list
echo "Printing the strings from the list $list:"
grep -f $list $file
