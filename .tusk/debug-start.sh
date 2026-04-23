#!/usr/bin/env bash
# Diagnostic service-start inside the sandbox. Verifies:
#   - docker.sock visibility (fixed when the resolv.conf guard is lifted)
#   - DNS still resolves (recursive bind should propagate resolv.conf)
#   - /run mount stack (should be just the host's tmpfs, no overmount)
# Always exits 1 so output lands in the startup log buffer and .tusk/logs/.
set +e

echo "=== id ==="
id

echo
echo "=== /proc/self/mountinfo | egrep ' /run| /var' ==="
grep -E " /run| /var" /proc/self/mountinfo || true

echo
echo "=== resolv.conf chain ==="
ls -la /etc/resolv.conf
readlink -f /etc/resolv.conf 2>&1 || true
echo "-- content --"
cat /etc/resolv.conf 2>&1 | head -5

echo
echo "=== docker.sock visible? ==="
ls -la /run/docker.sock 2>&1
ls -la /var/run/docker.sock 2>&1

echo
echo "=== docker ps (if sock visible) ==="
timeout 5 docker ps 2>&1 | head -3
echo "docker ps exit: $?"

echo
echo "=== DNS: getent hosts example.com ==="
getent hosts example.com 2>&1
echo "getent exit: $?"

echo
echo "=== exit 1 ==="
exit 1
