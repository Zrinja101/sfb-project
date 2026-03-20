import tempfile
from pathlib import Path
from sfb.utils.loader import load_yaml
from sfb.io.yaml_loader import load_dac_table


def test_load_yaml_and_dac_table():
    # check generic loader with temporary YAML
    temp = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
    try:
        temp.write("dac:\n  rows:\n    - row: 2\n      entries: []\n")
        temp.flush()
        temp.close()

        cfg = load_yaml(temp.name)
        assert "dac" in cfg

        table = load_dac_table(temp.name)
        assert table == [[]]
    finally:
        Path(temp.name).unlink()
