#!/bin/bash

# stop script on error and print it
set -e
# inform me of undefined variables
set -u
# handle cascading failures well
set -o pipefail


total_size=0

pushd $1 2> /dev/null
for f in ./*
do
    pushd $f > /dev/null
    ffmpeg -r 24 -pattern_type glob -i '*.png' -c:v libx264 out.mp4
    video_size=$(cat out.mp4 | wc -c)
    rm out.mp4
    total_size=$(($total_size + $video_size))
    echo
    echo
    echo "COMPRESSED $f TO SIZE $video_size"
    echo
    echo

    popd 2>/dev/null
done
popd 2> /dev/null
echo
echo
echo "TOTAL SIZE OF COMPRESSED VIDEOS IS $total_size BYTES"
