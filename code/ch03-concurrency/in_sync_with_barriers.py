import asyncio


def main():
    print("Running game loop!")
    print()
    asyncio.run(game_loop())


async def game_loop():
    barrier = asyncio.Barrier(3)

    while True:
        print('/////////////// FRAME START ////////////////////////', flush=True)
        async with asyncio.TaskGroup() as tg:
            tg.create_task(compute_physics(barrier))
            tg.create_task(get_input(barrier))
            tg.create_task(render_scene(barrier))

        print(r'\\\\\\\\\\\\\\\\\\\\\\ FRAME END \\\\\\\\\\\\\\')
        print()


async def render_scene(b: asyncio.Barrier):
    print("Rendering scene!")
    # Simulate work ;)
    await asyncio.sleep(1.5)

    await b.wait()

    # Clean up work after all tasks are done.
    print("Rendering done.")
    await asyncio.sleep(.25)


async def compute_physics(b: asyncio.Barrier):
    print("Computing physics!")
    await asyncio.sleep(.75)

    await b.wait()

    print("Physics done.")
    await asyncio.sleep(.25)


async def get_input(b: asyncio.Barrier):
    print("Getting input!")
    await asyncio.sleep(1)

    await b.wait()

    print("Input done.")
    await asyncio.sleep(.25)


if __name__ == '__main__':
    main()
