from dataclasses import dataclass

import almaflow


@dataclass
class new_state(almaflow.observable_state): ...


@dataclass
class ready_state(almaflow.observable_state): ...


@dataclass
class done_state(almaflow.observable_state): ...
