from sfb.core.dice import Dice
from sfb.core.ship import Ship
from sfb.dac.dac import DAC
from sfb.io.yaml_loader import load_dac_table


def main():
    dice = Dice()

    table = load_dac_table("sfb/data/dac/standard_dac.yaml")

    ship = Ship({
        "CARGO": 2,
        "F_HULL": 1,
        "BATTERY": 1
    })

    dac = DAC(table, dice)
    dac.new_volley()

    for _ in range(5):
        print(dac.resolve_hit(ship))


if __name__ == "__main__":
    main()
