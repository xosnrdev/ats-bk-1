#!/bin/bash

case "$1" in
    dev) fastapi dev ;;
    test) pytest ;;
    fmt) ruff format ;;
    check) ruff check ;;
    *) fastapi run ;;
esac