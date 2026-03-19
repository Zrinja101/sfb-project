from sfb.core.ship import Ship
from sfb.core.dice import Dice
from sfb.dac.dac import DAC
from sfb.io.yaml_loader import load_dac_table


def test_full_flow():
    dice = Dice(seed=1)

    table = load_dac_table("sfb/data/dac/standard_dac.yaml")

    ship = Ship({
        "CARGO": 2,
        "F_HULL": 1,
        "BATTERY": 1
    })

    dac = DAC(table, dice)
    dac.new_volley()

    results = [dac.resolve_hit(ship) for _ in range(4)]

    assert results[0] == "CARGO"

def test_once_per_volley_cell_level():
    class FixedDice(Dice):
        def __init__(self, fixed_roll):
            self.fixed_roll = fixed_roll

        def roll_2d6(self):
            return self.fixed_roll
    ship = Ship({"PROBE": 2, "A_HULL": 5})

    table = load_dac_table("sfb/data/dac/standard_dac.yaml")
    dac = DAC(table, FixedDice(7))
    dac.new_volley()

    first = dac.resolve_hit(ship)
    second = dac.resolve_hit(ship)

    assert first == "PROBE"
    assert second != "PROBE"  # shifted, even though probe still exists