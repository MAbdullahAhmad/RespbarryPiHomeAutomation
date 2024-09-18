#!/bin/bash

# Function to get the current IP address
get_ip() {
    ip=$(ip -o -4 addr show wlan0 | awk '{print $4}' | cut -d'/' -f1)
    if [ -z "$ip" ]; then
        ip=$(ip -o -4 addr show wlp2s0 | awk '{print $4}' | cut -d'/' -f1)
    fi
    echo "$ip"
}

# Get current IP and define network range
CURRENT_IP=$(get_ip)
NETWORK_BASE=$(echo $CURRENT_IP | cut -d'.' -f1-3)
NETWORK_RANGE="$NETWORK_BASE.0/24"

# Scan the network for active IPs by pinging
echo "Pinging all devices on the network $NETWORK_RANGE..."
nmap -sn $NETWORK_RANGE -oG - | grep "Status: Up" | awk '{print $2}' > active_ips.txt

echo "Pinging completed. Active IPs found:"
cat active_ips.txt

# Create a results table header
echo -e "\nIP Address\tPort 3000\tPort 8000"
echo "------------------------------------------"

# Initialize results file
> scan_results.txt

# Check each IP for open ports and HTTP responses
while read -r ip; do
    PORT_3000_STATUS="❌"
    PORT_8000_STATUS="❌"

    # Check if port 3000 is open and serving HTTP
    if nc -z -w 1 $ip 3000; then
        if curl -s --head --request GET "http://$ip:3000" | grep "200 OK" > /dev/null; then
            PORT_3000_STATUS="✔️"
        fi
    fi

    # Check if port 8000 is open and serving /sync
    if nc -z -w 1 $ip 8000; then
        if curl -s --head --request GET "http://$ip:8000/sync" | grep "200 OK" > /dev/null; then
            PORT_8000_STATUS="✔️"
        fi
    fi

    # Print and save the results
    echo -e "$ip\t$PORT_3000_STATUS\t$PORT_8000_STATUS"
    echo -e "$ip\t$PORT_3000_STATUS\t$PORT_8000_STATUS" >> scan_results.txt
done < active_ips.txt

# Clean up
rm -f active_ips.txt

echo -e "\nScan completed. Results saved to scan_results.txt"
