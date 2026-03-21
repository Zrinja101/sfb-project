"""
Combat operations including target selection and weapon firing.
"""

from sfb.core.map import HexMap
from sfb.combat.phaser import Phaser
from sfb.combat.arc import can_fire_at


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
    def fire_phaser(ship, target, game_map, phaser=None):
        """
        Fire a phaser at a target using the nearest-range table.

        Args:
            ship: Attacking ship.
            target: Target entity with take_damage and hp attributes.
            game_map: HexMap instance to calculate distance.
            phaser: Optional Phaser instance for deterministic testing.
        """
        if not target.alive:
            return

        phaser_instance = phaser or Phaser("sfb/data/weapons/phaser_1.yaml")

        # Check firing arc
        if not can_fire_at(ship.hex, ship.facing, target.hex, phaser_instance.arcs):
            print(f"Cannot fire: target not in firing arc")
            return

        range_to_target = game_map.distance(ship.hex, target.hex)

        damage = phaser_instance.fire(range_to_target)

        target.take_damage(damage)

        if not target.alive:
            print(f"{target.name} destroyed!")
        else:
            print(f"{target.name} has {target.hp} HP remaining")
