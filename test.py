from fastmcp import Client
import subprocess

# start server
proc = subprocess.Popen(
    ["python", "server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

client = Client(proc.stdin, proc.stdout)

# test tool
result = client.call_tool("get_all_tenants", {})

print(result)