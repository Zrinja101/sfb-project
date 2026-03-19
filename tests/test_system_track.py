from sfb.ships.system_track import SystemTrack


def test_destroy_boxes():

    track = SystemTrack("warp", 3)

    assert track.remaining() == 3

    track.destroy_box()
    track.destroy_box()

    assert track.remaining() == 1
