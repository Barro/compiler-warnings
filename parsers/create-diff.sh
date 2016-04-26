#!/bin/bash

set -euo pipefail

diff -Naur "$1" "$2" | egrep "^[\-+]-" | sort
