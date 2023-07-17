#!/bin/bash
set -Ceu

readonly SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd ${SCRIPT_DIR}

source ./config.sh

function main() {
    device_id=$1
    curl -sS -X GET "https://api.switch-bot.com/v1.0/devices/${device_id}/status" \
        -H "Authorization: ${API_TOKEN}" \
        -H 'Content-Type: application/json; charset=utf8' \
    | jq .
}

main $*
