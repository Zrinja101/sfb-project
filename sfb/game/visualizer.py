"""
Map visualization for logging and UI output.
"""

from sfb.game.logger import MapSnapshot


class MapVisualizer:
    """Generate text-based or data representations of game map."""

    @staticmethod
    def format_snapshot(snapshot: MapSnapshot) -> str:
        """Format a map snapshot as ASCII art."""
        output = []
        output.append(f"Turn {snapshot.turn}, Impulse {snapshot.impulse} ({snapshot.phase})")
        output.append("-" * 50)

        if not snapshot.entities:
            output.append("No entities on map")
            return "\n".join(output)

        # Find map bounds
        hex_positions = [e['hex'] for e in snapshot.entities if e['hex']]
        if not hex_positions:
            output.append("No entities with hex positions")
            return "\n".join(output)

        min_q = min(h[0] for h in hex_positions)
        max_q = max(h[0] for h in hex_positions)
        min_r = min(h[1] for h in hex_positions)
        max_r = max(h[1] for h in hex_positions)

        # Add padding
        min_q -= 2
        max_q += 2
        min_r -= 2
        max_r += 2

        # Create grid
        grid = {}
        for entity in snapshot.entities:
            if entity['hex']:
                grid[entity['hex']] = entity

        # Display map
        for r in range(min_r, max_r + 1):
            # Offset for hex display
            indent = "  " * (r % 2)
            row = []

            for q in range(min_q, max_q + 1):
                if (q, r) in grid:
                    entity = grid[(q, r)]
                    # Display entity symbol
                    if entity['alive']:
                        symbol = f"[{entity['name'][0]}]"
                    else:
                        symbol = "[X]"
                    row.append(symbol)
                else:
                    row.append("[ ]")

            output.append(indent + " ".join(row))

        # Legend
        output.append("")
        output.append("Legend:")
        for entity in snapshot.entities:
            alive_marker = "✓" if entity['alive'] else "✗"
            facing_str = f" facing {entity['facing']}" if entity['facing'] else ""
            output.append(
                f"  {entity['name'][0]}: {entity['name']} "
                f"at {entity['hex']}{facing_str} "
                f"HP:{entity['hp']} {alive_marker}"
            )

        return "\n".join(output)

    @staticmethod
    def format_all_snapshots(snapshots: list) -> str:
        """Format all snapshots as a sequence."""
        output = []
        output.append("\n" + "=" * 60)
        output.append("MAP SNAPSHOTS")
        output.append("=" * 60)

        for snapshot in snapshots:
            output.append("")
            output.append(MapVisualizer.format_snapshot(snapshot))

        return "\n".join(output)
