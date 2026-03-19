from sfb.core.map import HexMap
from sfb.core.engine import Engine
from sfb.units.ship import Ship
from sfb.units.drone import Drone


def main():
    game_map = HexMap()

    ship = Ship("Cadet Ship", (0, 0), "A")

    drone1 = Drone("Drone 1", (3, 0))
    drone2 = Drone("Drone 2", (5, -1))

    game_map.add_entity(ship)
    game_map.add_entity(drone1)
    game_map.add_entity(drone2)

    engine = Engine(game_map, ship, [drone1, drone2])

    for _ in range(20):
        engine.step()


if __name__ == "__main__":
    main()
