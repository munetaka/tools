#!/bin/bash
set -Ceu

readonly SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd ${SCRIPT_DIR}

source ./config.sh

case ${1} in
    list)
        ./device_list.sh
	;;
    on)
        ./device_on.sh ${2}
	;;
    off)
        ./device_off.sh ${2}
	;;
    toggle)
        ./device_toggle.sh ${2}
	;;
    status)
        ./device_status.sh ${2}
	;;
    *)
esac
