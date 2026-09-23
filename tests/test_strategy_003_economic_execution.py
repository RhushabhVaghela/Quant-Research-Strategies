from scripts.run_strategy_003_economic_execution import FRICTIONS, STT_RATE, STAMP_RATE, NSE_TX_RATE, GST_RATE
def test_friction_scenarios_are_frozen(): assert list(FRICTIONS)==['fee_floor','low','base','stress']
def test_registered_rates():
    assert STT_RATE==0.00025
    assert STAMP_RATE==0.00003
    assert NSE_TX_RATE==0.0000307
    assert GST_RATE==0.18