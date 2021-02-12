"""
Print received SIGTERM & SIGINT signals
"""
import asyncio
import signal
from functools import partial
import sys
from simpervisor import atexitasync

def _handle_sigterm(number, received_signum):
    # Print the received signum so we know our handler was called
    print("handler {} received".format(number), int(received_signum), flush=True)

handlercount = int(sys.argv[1])
for i in range(handlercount):
    atexitasync.add_handler(partial(_handle_sigterm, i))

loop = asyncio.get_event_loop()
try:
    loop.run_forever()
finally:
    # Cleanup properly so we get a clean exit
    try:
        remaining_tasks = asyncio.all_tasks(loop=loop)
    except AttributeError:
        # asyncio.all_tasks was added in 3. Provides reverse compatability.
        remaining_tasks = asyncio.Task.all_tasks(loop=loop)
    loop.run_until_complete(asyncio.gather(*remaining_tasks))
    loop.close()
