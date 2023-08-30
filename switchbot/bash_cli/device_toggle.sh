#!/bin/bash
#
# refs:
#   https://github.com/OpenWonderLabs/SwitchBotAPI#send-device-control-commands
#   https://github.com/OpenWonderLabs/SwitchBotAPI#plug-mini-jp-2
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
  curl -X POST "https://api.switch-bot.com/v1.1/devices/${device_id}/commands" \
    -H "Authorization: ${API_TOKEN}" \
    -H "sign: ${SIGNATURE}" \
    -H "t: ${T}" \
    -H "nonce: ${UUID}" \
    -H 'Content-Type: application/json; charset=utf8' \
    -d '{
            "command": "toggle",
            "parameter": "default",
            "commandType": "command"
        }' |
    jq .
}

main "$*"
