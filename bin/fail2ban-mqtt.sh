#!/usr/bin/env bash

PROG=$(cat <<EOF
BEGIN {
   total = 0
   "date +%s" | getline time
}

/fail2ban\.filter.*Found/ {
    total = total + 1
}

END {
   printf("{\"status\":%d, \"changed\":%s}", total, time)
}
EOF
)

awk "$PROG" /var/log/fail2ban.log | mosquitto_pub -t fail2ban/status -r -s