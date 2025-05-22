import asyncio
import os
import signal

import almaflow
import almanet

from testing import public

testing_service = almanet.remote_service("net.testing.microservice")


@almaflow.transition(
    public.new_state,
    public.ready_state,
)
async def make_ready(
    payload,
    **kwargs,
):
    almanet.logger.debug(f'{payload._uri_} {payload}')
    return public.ready_state()


_ready_to_exit = asyncio.Event()

@almaflow.observe(
    testing_service,
    public.ready_state,
    public.done_state,
)
async def _on_ready(
    payload,
    **kwargs,
):
    almanet.logger.debug(f'{payload._uri_} {payload}')
    _ready_to_exit.set()
    return public.done_state()


@testing_service.post_join
async def __post_join(session: almanet.Almanet):
    new_state = public.new_state()
    ready_state = await make_ready(new_state)
    almanet.logger.debug(f'{ready_state=}')


async def test_simple():
    almanet.serve_single(
        testing_service,
        almanet.clients.ansqd_tcp_client("localhost:4150"),
        stop_loop_on_exit=False,
    )
    await _ready_to_exit.wait()
    os.kill(os.getpid(), signal.SIGINT)
    await asyncio.sleep(61)
