#!/bin/bash
#
# refs:
#   https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-list
#   https://github.com/OpenWonderLabs/SwitchBotAPI#plug-mini-jp
set -Ceu

SCRIPT_DIR=$(
  cd "$(dirname "$0")"
  pwd
)
readonly SCRIPT_DIR
cd "${SCRIPT_DIR}"

source ./config.sh

function main() {
  curl -sS -X GET 'https://api.switch-bot.com/v1.1/devices' \
    -H "Authorization: ${API_TOKEN}" \
    -H "sign: ${SIGNATURE}" \
    -H "t: ${T}" \
    -H "nonce: ${UUID}" \
    -H 'Content-Type: application/json; charset=utf8' |
    jq .
}

main
