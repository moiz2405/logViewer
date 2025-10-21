#!/bin/bash
# Script to start both sentry and myApp backends

# Start sentry backend in the background
cd "$(dirname "$0")/sentry"
bash run_server.sh &

# Start myApp backend in the foreground
cd ../myApp
bash start_server.sh

wait
