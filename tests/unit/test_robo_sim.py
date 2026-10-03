from shared.robo_x_sim import SimulatedRobot
def test_sim():
    r = SimulatedRobot()
    assert r.status()["battery_pct"] > 0
