from app.tianji.orchestrator import TianJiOrchestrator


def test_orchestrator_full_v1_v4_chain():
    state = TianJiOrchestrator().run(
        question="测试天机系统完整链路，适不适合继续开源发布",
        domain="strategy",
        goal="完整链路测试",
        event_time="2026-05-26 22:30",
        location="Guangzhou",
        rounds=3,
        birth_datetime="1998-06-15 14:30",
        gender="male",
    )
    assert state["query"]["domain"] == "strategy"
    assert state["symbolic"]["bagua"]["main"]
    assert state["symbolic"]["iching"]["status"] == "ok"
    assert state["symbolic"]["bazi"]["status"] == "ok"
    assert state["symbolic"]["qimen"]["status"] == "ok"
    assert len(state["future"]["branches"]) == 3
    assert state["simulation"]["agents"]
    assert state["strategy"]["best_action"]
