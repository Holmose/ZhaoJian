from app.tianji.engines.iching_engine import IChingEngine


def test_iching_engine_returns_transition():
    engine = IChingEngine()
    result = engine.analyze("这个项目还没完成，未来是否适合继续扩张", "strategy", "2026-05-26 22:10")
    assert result["status"] == "ok"
    assert result["primary_hexagram"]["name"]
    assert result["changed_hexagram"]["name"]
    assert result["changing_lines"]
    assert "transition" in result
    assert "action_hint" in result
