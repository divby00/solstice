#!/usr/bin/env sh
cd locale
msgfmt es.po
mv messages.mo es_ES/LC_MESSAGES/solstice.mo
cd ..
