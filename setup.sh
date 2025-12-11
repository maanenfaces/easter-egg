#!/usr/bin/env bash

set -e
set -o nounset

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

apt-get update && apt-get install -y git fonts-dejavu-core
pip3 install -r "${script_dir}"/requirements.txt
