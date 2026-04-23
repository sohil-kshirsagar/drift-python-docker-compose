#!/usr/bin/env bash
# Diagnostic service-start. Dumps what's visible/blocked under the sandbox,
# then exits non-zero so the drift run reports (and we can read the output
# via the startup log buffer).
set +e
echo "=== whoami / id ==="
whoami
id

echo
echo "=== env | relevant ==="
env | grep -E '^(DOCKER|PATH|HOME|USER|UID|XDG|TMPDIR)=' | sort

echo
echo "=== mount | head ==="
mount | head -20

echo
echo "=== ls -la /var/run /run ==="
ls -la /var/run 2>&1 | head
ls -la /run 2>&1 | head

echo
echo "=== /var/run/docker.sock stat ==="
ls -la /var/run/docker.sock 2>&1
ls -la /run/docker.sock 2>&1
stat /var/run/docker.sock 2>&1 || true

echo
echo "=== which docker / docker version ==="
which docker
docker version --format '{{.Client.Version}}' 2>&1 | head -1

echo
echo "=== docker ps (reads /var/run/docker.sock) ==="
docker ps 2>&1 | head -5
echo "docker ps exit: $?"

echo
echo "=== raw connect to /var/run/docker.sock via python ==="
python3 - <<'PY' 2>&1
import socket, os, sys
for p in ("/var/run/docker.sock", "/run/docker.sock"):
    print(f"-- {p} --")
    print(" exists:", os.path.exists(p))
    try:
        print(" stat:", os.stat(p))
    except Exception as e:
        print(" stat err:", e)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        s.connect(p)
        print(" connect: OK")
        s.sendall(b"GET /_ping HTTP/1.0\r\n\r\n")
        data = s.recv(4096)
        print(" reply:", data[:200])
    except Exception as e:
        print(" connect err:", type(e).__name__, e)
    finally:
        s.close()
PY

echo
echo "=== exit 1 to signal service-start failed (expected) ==="
exit 1
