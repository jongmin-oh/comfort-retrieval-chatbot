#!/bin/sh
gunicorn manage:app -c gunicorn.conf.py