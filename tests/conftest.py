import pytest
from sfb.core.map import HexMap
from sfb.core.dice import Dice


@pytest.fixture
def hexmap():
    return HexMap()


@pytest.fixture
def seeded_dice():
    return Dice(seed=1234)
