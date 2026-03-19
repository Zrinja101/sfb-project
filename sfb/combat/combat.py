from sfb.core.map import HexMap
from sfb.combat.phaser import Phaser


class CombatSystem:

    @staticmethod
    def find_closest_target(ship, targets):
        alive_targets = [t for t in targets if t.alive]
        if not alive_targets:
            return None

        closest = min(
            alive_targets,
            key=lambda t: HexMap.distance(ship.hex, t.hex)
        )
        return closest

    @staticmethod
    def fire_phaser(ship, target, game_map):
        if not target.alive:
            return

        range_to_target = game_map.distance(ship.hex, target.hex)

        damage = Phaser.fire(range_to_target)

        target.take_damage(damage)

        if not target.alive:
            print(f"{target.name} destroyed!")
        else:
            print(f"{target.name} has {target.hp} HP remaining")
