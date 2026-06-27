#!/bin/bash
# Script to run missed hours for a periodic task scheduled hourly from 00:00 to 09:00 UTC.
# Usage: ./run_missed_hours.sh <wrapper_script>
# Example: ./run_missed_hours.sh /home/workspace/run_void_daily.sh

WRAPPER_SCRIPT="$1"
if [ -z "$WRAPPER_SCRIPT" ]; then
    echo "Usage: $0 <wrapper_script>"
    exit 1
fi

if [ ! -x "$WRAPPER_SCRIPT" ]; then
    echo "Error: Wrapper script not found or not executable: $WRAPPER_SCRIPT"
    exit 1
fi

current_epoch=$(date -u +%s)
run_count=0
for H in {0..9}; do
    # Calculate epoch for today at H:00:00 UTC
    target_epoch=$(TZ=UTC date -d "today ${H}:00:00" +%s)
    if [ $current_epoch -gt $target_epoch ]; then
        "$WRAPPER_SCRIPT" >/dev/null 2>&1
        run_count=$((run_count + 1))
    fi
done
echo "Ran $run_count times for missed hours"
