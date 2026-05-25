from app.tianji.engines.qimen_engine import QimenEngine


def test_qimen_engine_missing_event_time():
    result = QimenEngine().analyze()
    assert result["status"] == "missing_event_time"


def test_qimen_engine_basic_output():
    result = QimenEngine().analyze("2026-05-26 21:30", location="Guangzhou", question="是否适合发布", domain="strategy")
    assert result["status"] == "ok"
    assert result["bureau"]["label"]
    assert result["main_palace"]["name"]
    assert result["door"]["name"]
    assert result["star"]["name"]
    assert result["god"]["name"]
    assert result["timing_hint"]
    assert result["risk_hint"]
