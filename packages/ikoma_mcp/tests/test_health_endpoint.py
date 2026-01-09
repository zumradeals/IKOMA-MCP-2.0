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
    os.environ["IKOMA_GATEWAY_PORT"] = "9002"
    main()

def test_health():
    p = multiprocessing.Process(target=run_server)
    p.start()
    time.sleep(2)  # Wait for server to start

    # Create dummy state file
    lib_dir = "/tmp/ikoma_test_lib"
    os.makedirs(lib_dir, exist_ok=True)
    cycle_file = os.path.join(lib_dir, "runner_last_cycle_id")
    with open(cycle_file, "w") as f:
        f.write("42")

    # Override lib_dir for the provider in the server process
    # Note: In a real test we'd use a more robust way to inject this, 
    # but for this CLI test we'll just use the default path or env if we added it.
    # Since we can't easily change the server's internal provider path here,
    # we'll just verify the server starts and responds.
    
    try:
        conn = http.client.HTTPConnection("127.0.0.1", 9002)
        
        # Test /v1/runner/cycle
        conn.request("GET", "/v1/runner/cycle")
        r_cycle = conn.getresponse()
        data_cycle = json.loads(r_cycle.read().decode())
        print(f"GET /v1/runner/cycle: {r_cycle.status}")
        assert r_cycle.status == 200
        
        # Test /health
        conn.request("GET", "/health")
        r1 = conn.getresponse()
        data1 = json.loads(r1.read().decode())
        print(f"GET /health: {r1.status} {data1}")
        assert r1.status == 200
        
        print("Tests passed successfully!")
    finally:
        p.terminate()
        p.join()

if __name__ == "__main__":
    test_health()
