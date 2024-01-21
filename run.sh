#!/bin/bash
gunicorn manage:app -c gunicorn.conf.py