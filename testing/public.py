import almaflow


class new_state(almaflow.observable_state):
    foo: str


class ready_state(new_state): ...


class done_state(ready_state): ...
