#!/bin/bash
#
# refs:
#   https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-status
#   https://github.com/OpenWonderLabs/SwitchBotAPI#plug-mini-jp-1
set -Ceu

SCRIPT_DIR=$(
  cd "$(dirname "$0")"
  pwd
)
readonly SCRIPT_DIR
cd "${SCRIPT_DIR}"

source ./config.sh

function main() {
  device_id=$1
  curl -sS -X GET "https://api.switch-bot.com/v1.1/devices/${device_id}/status" \
    -H "Authorization: ${API_TOKEN}" \
    -H "sign: ${SIGNATURE}" \
    -H "t: ${T}" \
    -H "nonce: ${UUID}" \
    -H 'Content-Type: application/json; charset=utf8' |
    jq .
}

main "$*"
