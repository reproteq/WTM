#!/bin/bash

OUI=$(echo ${1//[:.- ]/} | tr "[a-f]" "[A-F]" | egrep -o "^[0-9A-F]{6}")

cat oui.txt |grep $OUI
