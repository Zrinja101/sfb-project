"""
YAML loading utilities.
"""

import yaml
from typing import List, Dict


def load_dac_table(path: str) -> List[List[Dict]]:
    """
    Load DAC table from YAML file.

    Args:
        path (str): Path to YAML file

    Returns:
        List[List[Dict]]: DAC table
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    rows = sorted(data["dac"]["rows"], key=lambda r: r["row"])
    return [row["entries"] for row in rows]
