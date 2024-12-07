#!/usr/bin/env bash
uwsgi --https 0.0.0.0:443,secureblog.crt,secureblog.key --master -p 1 -w wsgi:app 