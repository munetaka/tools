#!/bin/bash
set -Ceu

readonly SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd ${SCRIPT_DIR}

source ./config.sh

function main() {
    device_id=$1
    curl -sS -X POST "https://api.switch-bot.com/v1.1/devices/${device_id}/commands" \
        -H "Authorization: ${API_TOKEN}" \
        -H "sign: ${SIGNATURE}" \
        -H "t: ${T}" \
        -H "nonce: ${UUID}" \
        -H 'Content-Type: application/json; charset=utf8' \
        -d '{
            "command": "turnOff",
            "parameter": "default",
            "commandType": "command"
        }' \
    | jq .
}

main $*
