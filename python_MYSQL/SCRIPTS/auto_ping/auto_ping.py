import os
import sys
import json
import subprocess
import time
from typing import Callable
import re
from datetime import datetime, timezone
import pygame
LIST_TO_PING = ["google.com", "Youtube.com", "facebook.com"]
path = os.path.join(os.getcwd(), "autoping.json")
failed_path = os.path.join(os.getcwd(), "failures.json")
syren_path = os.path.join(os.getcwd(),"sirenmeme.wav")
pygame.init()
mysound = pygame.mixer.Sound(syren_path)

def pingingsites() -> list:
    results = []
    for site in LIST_TO_PING:
        if sys.platform == "linux":
            result = subprocess.getoutput(f"ping {site} -c 1")
        else:
            result = subprocess.getoutput(f"ping {site} -n 1")
        results.append(result)
    return results


def parse_ping_output(output: str) -> dict:
    if "Temporary failure" in output or "could not find" in output:
        return {"status": "unreachable", "latency_ms": None, "packet_loss": "100%"}

    latency = re.search(r"time=([\d.]+) ms", output)
    loss = re.search(r"([\d]+)% packet loss", output)

    return {
        "status": "reachable",
        "latency_ms": float(latency.group(1)) if latency else None,
        "packet_loss": loss.group(0) if loss else None,
    }

def alert(failed_sites: list) -> None:
    if not failed_sites:
        return
    print(f"⚠ Unreachable sites: {', '.join(failed_sites)}")
    
    if sys.platform == "linux":
        mysound.play()
    else:
        import winsound
        winsound.Beep(1000, 500)   

def check_for_failures(result: dict) -> list:
    failed = []
    for site, data in result.items():
        if data["status"] == "unreachable":
            failed.append(site)
    return failed

def write_failures(failed_sites: list) -> None:
    if not failed_sites:
        return
    
    if os.path.exists(failed_path):
        with open(failed_path, "r") as f:
            existing = json.load(f)
    else:
        existing = {}
    
    timestamp = datetime.now(timezone.utc).isoformat()
    existing[timestamp] = failed_sites
    
    with open(failed_path, "w") as f:
        json.dump(existing, f, indent=4)

def operate() -> dict:
    results = pingingsites()      
    
    data = {}
    for site, result in zip(LIST_TO_PING, results):
        parsed = parse_ping_output(result)  
        data[site] = parsed                 
    
    return data

def write_file(result_json: dict) -> None:
    if os.path.exists(path):
        with open(path, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    
    existing_data[time.asctime()] = result_json

    with open(path, "w") as f:
        json.dump(existing_data, f, indent=4)


def delaywrapper(func: Callable, delaysecs: int = 4) -> None:
    try:
        while True:
            result = func()
            write_file(result)
            
            failed = check_for_failures(result)
            write_failures(failed)
            alert(failed)
            
            time.sleep(delaysecs)
    except KeyboardInterrupt:
        print("\nStopped.")

def main() -> None:
    delaywrapper(operate, 3)


if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) <= 1:
        raise Exception("wrong number of arguments")

    LIST_TO_PING += arguments[1:]
    main()