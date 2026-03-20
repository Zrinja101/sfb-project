from sfb.dac.dac import DAC
from sfb.core.dice import Dice
from sfb.core.ship import Ship


def test_dac_select_row_and_once():
    table = [[{"id": "x", "type": "PHASER", "once": True}]] * 11
    dac = DAC(table, Dice(seed=42))

    dac.new_volley()
    ship = Ship({"PHASER": 1, "A_HULL": 0})

    first = dac.resolve_hit(ship)
    assert first == "PHASER"

    second = dac.resolve_hit(ship)
    assert second is None
