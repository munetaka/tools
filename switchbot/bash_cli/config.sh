#!/bin/bash
set -Ceu

readonly API_TOKEN=''
readonly API_SECRET=''
readonly T=$(gdate +%s%3N)
readonly UUID=$(uuidgen)
readonly SIGNATURE=$(echo -n "${API_TOKEN}${T}${UUID}" | openssl dgst -sha256 -hmac "${API_SECRET}" -binary | base64)
