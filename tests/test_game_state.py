from sfb.game.state import GameState, GameStep


def test_game_state_advance_steps():
    state = GameState()
    assert state.turn == 1
    assert state.impulse == 1
    assert state.step == GameStep.MOVE_SHIPS

    state.next_step()
    assert state.step == GameStep.MOVE_SEEKING_WEAPONS

    state.next_step()
    assert state.step == GameStep.FIRE_WEAPONS

    state.next_step()
    assert state.step == GameStep.DAMAGE

    state.next_step()
    assert state.step == GameStep.MOVE_SHIPS
    assert state.impulse == 2


def test_game_state_impulse_rollover():
    state = GameState(1, 8)
    for _ in range(4):
        state.next_step()
    assert state.turn == 2
    assert state.impulse == 1
