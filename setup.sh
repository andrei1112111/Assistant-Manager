#!/bin/bash

if command python -v
then
    echo "Complete"
    exit 0
fi
if command python -v
then
    echo "Something went wrong"
    exit 0
fi
