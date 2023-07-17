#!/bin/bash

# ref: https://elinux.org/RPi_HardwareHistory

model=$(tr -d '\0' < /proc/device-tree/model)
echo ${model}

if [[ "${model}" =~ "4 Model B" ]]; then
    echo "this model is Raspi 4 Model B."
elif [[ "${model}" =~ "3 Model B" ]]; then
    echo "this model is Raspi 3 Model B."
else
    echo "this model is unkown."
fi
