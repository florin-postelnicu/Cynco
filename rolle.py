
import asyncio

# definition of a corutine

async def corutine_1():
    print("corutine_1 is active on the event loop")

    print("corutibe_1 yielding control. Going to be blocked for 7 seconds")

    await asyncio.sleep(4)
    print("coruntine_1 resumeed. corutine_1 exiting")

# definition of a corutine
async def corutine_2():
    print("corutine_2 is active on the event loop")
    print("corutin_2 yielding control. Going to be blocked for 5  seconds")

    await asyncio.sleep(5)

    print("corutine_2 resumed. corutine_2 exiting")

# this is the event loop
loop = asyncio.get_event_loop()

# schedule both corutines to run on th event loop

loop.run_until_complete(asyncio.gather(corutine_1(), corutine_2()))
