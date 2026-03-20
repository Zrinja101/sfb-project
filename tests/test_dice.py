from sfb.core.dice import Dice


def test_dice_seed_determinism():
    d1 = Dice(seed=123)
    d2 = Dice(seed=123)

    assert d1.d6() == d2.d6()
    assert d1.roll_2d6() == d2.roll_2d6()


def test_dice_range():
    dice = Dice()
    for _ in range(50):
        value = dice.roll_2d6()
        assert 2 <= value <= 12
