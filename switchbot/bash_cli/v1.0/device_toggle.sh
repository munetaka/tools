#!/bin/bash
set -Ceu

readonly SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd ${SCRIPT_DIR}

source ./config.sh

function main() {
    device_id=$1
    curl -X POST "https://api.switch-bot.com/v1.0/devices/${device_id}/commands" \
        -H "Authorization: ${API_TOKEN}" \
        -H 'Content-Type: application/json; charset=utf8' \
        -d '{
            "command": "toggle",
            "parameter": "default",
            "commandType": "command"
        }' \
    | jq .
}

main $*
