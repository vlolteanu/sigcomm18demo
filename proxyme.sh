iptables -t nat -N SHADOWSOCKS
iptables -t mangle -N SHADOWSOCKS
iptables -t mangle -N SHADOWSOCKS_MARK

iptables -t nat -A SHADOWSOCKS -p tcp -m owner --uid-owner proxyme -j REDIRECT --to-ports 12345

iptables -t nat -A OUTPUT -p tcp -j SHADOWSOCKS
iptables -t mangle -A PREROUTING -j SHADOWSOCKS
iptables -t mangle -A OUTPUT -j SHADOWSOCKS_MARK

