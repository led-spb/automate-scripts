#!/bin/sh

(echo Top 10 IP with failed logins & (awk '/fail2ban\.filter/ && / Found/ {print $8}' /var/log/fail2ban.log | sort | uniq -c | sort -n -r | head)) | $(dirname $0)/notify
#awk '/fail2ban\.filter/ && / Found/ {print $8}' /var/log/fail2ban.log | bin\ip-stat fail2ban