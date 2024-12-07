#!/usr/bin/env bash
uwsgi --https 0.0.0.0:443,evilsite.crt,evilsite.key --master -p 1 -w wsgi:app 