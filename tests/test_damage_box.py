from sfb.ships.damage_box import DamageBox


def test_destroy_box():

    box = DamageBox("warp")

    assert not box.destroyed

    box.destroy()

    assert box.destroyed
