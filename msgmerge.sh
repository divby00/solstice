#!/usr/bin/env sh
./makepot.sh
cd locale
msgmerge es.po solstice.pot > merged.po
cd ..
