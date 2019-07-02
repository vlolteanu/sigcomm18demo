iptables -t nat -N SIXTYSOCKS
iptables -t mangle -N SIXTYSOCKS
iptables -t mangle -N SIXTYSOCKS_MARK

iptables -t nat -A SIXTYSOCKS -p tcp -m owner --uid-owner proxyme -j REDIRECT --to-ports 12345

iptables -t nat -A OUTPUT -p tcp -j SIXTYSOCKS
iptables -t mangle -A PREROUTING -j SIXTYSOCKS
iptables -t mangle -A OUTPUT -j SIXTYSOCKS_MARK

