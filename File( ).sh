#!/bin/bash
if [ -f $1 ]
then
    echo "The filetype of $1 is $(file $1)"
else
    echo "File not found!"
fi
