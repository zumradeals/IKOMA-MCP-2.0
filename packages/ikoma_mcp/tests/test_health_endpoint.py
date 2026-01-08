import http.client
import json
import multiprocessing
import time
import sys
import os

# Add src to path to be able to import ikoma_mcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from ikoma_mcp.gateway.main import main

def run_server():
    os.environ["IKOMA_GATEWAY_PORT"] = "9001"
    main()

def test_health():
    p = multiprocessing.Process(target=run_server)
    p.start()
    time.sleep(2)  # Wait for server to start

    try:
        conn = http.client.HTTPConnection("127.0.0.1", 9001)
        
        # Test /health
        conn.request("GET", "/health")
        r1 = conn.getresponse()
        data1 = json.loads(r1.read().decode())
        print(f"GET /health: {r1.status} {data1}")
        assert r1.status == 200
        assert data1["status"] == "ok"
        
        # Test /
        conn.request("GET", "/")
        r2 = conn.getresponse()
        data2 = json.loads(r2.read().decode())
        print(f"GET /: {r2.status} {data2}")
        assert r2.status == 200
        assert data2["status"] == "ok"

        print("Tests passed successfully!")
    finally:
        p.terminate()
        p.join()

if __name__ == "__main__":
    test_health()
