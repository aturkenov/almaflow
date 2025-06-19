import asyncio
import os
import signal

import almaflow
import almanet

from testing import public

testing_service = almanet.remote_service("net.testing.microservice")


def log_state(state: almaflow.observable_state):
    almanet.logger.debug(f'{state._uri_}: {state.model_dump_json()}')


@almaflow.transition(
    str,
    public.new_state,
)
async def create(
    payload: str,
    **kwargs,
):
    return public.new_state(foo=payload)


@almaflow.observe(
    testing_service,
    public.new_state,
    public.ready_state,
)
async def make_ready(
    payload: public.new_state,
    **kwargs,
):
    log_state(payload)
    payload.foo = f"{payload.foo} is ready"
    payload._next_delay_seconds_ = 3


_ready_to_exit = asyncio.Event()

@almaflow.observe(
    testing_service,
    public.ready_state,
    public.done_state,
)
async def _on_ready(
    payload: public.ready_state,
    **kwargs,
):
    log_state(payload)
    _ready_to_exit.set()


@testing_service.post_join
async def __post_join(session: almanet.Almanet):
    new_state = await create("test")
    log_state(new_state)


async def test_simple():
    almanet.serve_single(
        almanet.clients.ansqd_tcp_client("localhost:4150"),
        testing_service,
        stop_loop_on_exit=False,
    )
    await _ready_to_exit.wait()
    os.kill(os.getpid(), signal.SIGINT)
    await asyncio.sleep(1)
