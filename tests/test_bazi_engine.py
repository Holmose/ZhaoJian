from app.tianji.engines.bazi_engine import BaziEngine


def test_bazi_engine_missing_birth_datetime():
    result = BaziEngine().analyze()
    assert result["status"] == "missing_birth_datetime"


def test_bazi_engine_basic_output():
    result = BaziEngine().analyze("1998-06-15 14:30", gender="male", location="Guangzhou")
    assert result["status"] == "ok"
    assert set(result["pillars"].keys()) == {"year", "month", "day", "hour"}
    assert result["day_master"]["stem"]
    assert len(result["five_element_balance"]) == 5
    assert result["personality_bias"]
    assert result["risk_pattern"]
