#!/bin/bash
#
# manage switchbot plug.
# ref: https://github.com/OpenWonderLabs/SwitchBotAPI
set -Ceu

SCRIPT_DIR=$(
  cd "$(dirname "$0")"
  pwd
)
readonly SCRIPT_DIR
cd "${SCRIPT_DIR}"

source ./config.sh

function usage() {
  echo 'usage: ./cli.sh [list|on|off|toggle|status]'
}

if [ $# = 0 ]; then
  usage
  exit 1
fi

case ${1} in
  list)
    ./device_list.sh
    ;;
  on)
    device_id=${2}
    ./device_on.sh "${device_id}"
    ;;
  off)
    device_id=${2}
    ./device_off.sh "${device_id}"
    ;;
  toggle)
    device_id=${2}
    ./device_toggle.sh "${device_id}"
    ;;
  status)
    device_id=${2}
    ./device_status.sh "${device_id}"
    ;;
  *)
    usage
    ;;
esac
