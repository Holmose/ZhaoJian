"""Test RelationshipEngine V5"""
import json, sys
sys.path.insert(0, "backend/app")
from zhaojian.engines.relationship_engine import RelationshipEngine

def test_basic():
    engine = RelationshipEngine()
    result = engine.analyze(
        question="我和女朋友经常吵架，她慢性子我急性子，吵完她说我不理解她",
        conflict_type="性格冲突",
        party_a_desc="我：急性子，凡事想立刻解决，说话急",
        party_b_desc="她：慢性子，爱安静，总说先放一放",
        conflict_event="每次吵架我都觉得她在拖后腿，她觉得我太急躁",
        duration="半年"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))

def test_ying():
    engine = RelationshipEngine()
    result = engine.analyze(
        question="我急的时候她愿意陪我慢一点，她能接住我的情绪",
        conflict_type="磨合困难",
        party_a_desc="急性子",
        party_b_desc="慢性子",
        conflict_event="我急的时候说陪我快两步，她愿意配合",
        duration="三个月"
    )
    print("\n=== 应命测试 ===")
    print(json.dumps(result["ying_di"], ensure_ascii=False, indent=2))
    print(json.dumps(result["verdict"], ensure_ascii=False, indent=2))
    print(json.dumps(result["paths"][0], ensure_ascii=False, indent=2))

def test_di():
    engine = RelationshipEngine()
    result = engine.analyze(
        question="我好好说她却说你急，各走各的，不一致",
        conflict_type="性格冲突",
        party_a_desc="急性子",
        party_b_desc="慢性子",
        conflict_event="你好好说她却说你急，让她陪快两步她说我急你去",
        duration="一年"
    )
    print("\n=== 敌命测试 ===")
    print(json.dumps(result["ying_di"], ensure_ascii=False, indent=2))
    print(json.dumps(result["verdict"], ensure_ascii=False, indent=2))
    print(json.dumps(result["paths"][2], ensure_ascii=False, indent=2))

def test_compromise():
    engine = RelationshipEngine()
    result = engine.analyze(
        question="每次都是我让，她在拒绝接住我",
        conflict_type="冷淡冷却",
        party_a_desc="我总是让步",
        party_b_desc="她从不改变",
        conflict_event="我又忍了，让步了半年，每次吵架翻旧账，我觉得不公平",
        duration="半年"
    )
    print("\n=== 让步测试 ===")
    print(json.dumps(result["acceptance"], ensure_ascii=False, indent=2))
    print(json.dumps(result["direction"], ensure_ascii=False, indent=2))
    print(json.dumps(result["inscription"]["acceptance_judge"], ensure_ascii=False))

if __name__ == "__main__":
    test_basic()
    test_ying()
    test_di()
    test_compromise()
    print("\nAll tests passed!")