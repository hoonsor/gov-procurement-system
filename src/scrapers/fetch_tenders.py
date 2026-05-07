#!/usr/bin/env python3
"""
政府電子採購網爬蟲模組 (模擬系統)
模擬抓取政府招標公告
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# 模擬招標資料
MOCK_TENDERS = [
    {
        "tender_id": "TP-2026-001",
        "title": "校園網路設備更新採購案",
        "agency": "教育部",
        "department": "資訊中心",
        "category": "資訊設備",
        "budget": 2500000,
        "publish_date": "2026-05-01",
        "deadline": "2026-05-25",
        "description": "採購校園網路交換器、路由器及相關設備，包含安裝與保固服務。",
        "requirements": "須具備ISO 27001認證，近三年有類似實績者優先。",
        "contact": "王先生",
        "phone": "02-1234-5678",
        "status": "投標中"
    },
    {
        "tender_id": "TP-2026-002",
        "title": "圖書館自動化系統更新",
        "agency": "文化部",
        "department": "圖書館",
        "category": "資訊服務",
        "budget": 1800000,
        "publish_date": "2026-05-03",
        "deadline": "2026-05-28",
        "description": "引進自動化圖書管理系統，包含軟體授權、硬體設備及教育訓練。",
        "requirements": "須具備圖書館系統建置經驗，通過CMMI Level 3以上認證。",
        "contact": "李小姐",
        "phone": "02-2345-6789",
        "status": "投標中"
    },
    {
        "tender_id": "TP-2026-003",
        "title": "學生宿舍冷氣機採購",
        "agency": "教育部",
        "department": "學務處",
        "category": "電器設備",
        "budget": 3200000,
        "publish_date": "2026-05-05",
        "deadline": "2026-06-01",
        "description": "採購分離式冷氣機200台，包含安裝及五年保固服務。",
        "requirements": "產品須具備節能標章，CSPF值達3.5以上。",
        "contact": "張先生",
        "phone": "03-3456-7890",
        "status": "投標中"
    },
    {
        "tender_id": "TP-2026-004",
        "title": "運動場地設施改善工程",
        "agency": "體育署",
        "department": "設施科",
        "category": "工程類",
        "budget": 4500000,
        "publish_date": "2026-05-06",
        "deadline": "2026-06-05",
        "description": "田徑場跑道翻新、籃球場地更新及照明設備改善。",
        "requirements": "須具備甲級營造業執照，近五年有學校運動場地工程實績。",
        "contact": "陳先生",
        "phone": "04-4567-8901",
        "status": "投標中"
    },
    {
        "tender_id": "TP-2026-005",
        "title": "教學軟體平台建置",
        "agency": "教育部",
        "department": "教務處",
        "category": "資訊服務",
        "budget": 1500000,
        "publish_date": "2026-05-07",
        "deadline": "2026-06-08",
        "description": "建置雲端教學平台，支援線上課程、測驗及學習歷程管理。",
        "requirements": "須具備教育雲端平台建置經驗，通過資安認證。",
        "contact": "林小姐",
        "phone": "05-5678-9012",
        "status": "投標中"
    },
    {
        "tender_id": "TP-2026-006",
        "title": "辦公室文具用品採購",
        "agency": "行政院",
        "department": "總務處",
        "category": "文具類",
        "budget": 500000,
        "publish_date": "2026-05-02",
        "deadline": "2026-05-20",
        "description": "年度文具用品統一採購，包含紙張、筆類、檔案夾等。",
        "requirements": "須為合法立案廠商，具政府採購經驗者優先。",
        "contact": "黃小姐",
        "phone": "06-6789-0123",
        "status": "即將截止"
    },
    {
        "tender_id": "TP-2026-007",
        "title": "監視系統更新採購",
        "agency": "內政部",
        "department": "警政署",
        "category": "安全設備",
        "budget": 2800000,
        "publish_date": "2026-04-28",
        "deadline": "2026-05-18",
        "description": "校園安全監視系統更新，採用IP Camera數位方案。",
        "requirements": "須具備安控系統建置丙級以上認證。",
        "contact": "劉先生",
        "phone": "07-7890-1234",
        "status": "即將截止"
    },
    {
        "tender_id": "TP-2026-008",
        "title": "環境清潔服務採購",
        "agency": "環境部",
        "department": "清潔隊",
        "category": "服務類",
        "budget": 1200000,
        "publish_date": "2026-05-04",
        "deadline": "2026-06-02",
        "description": "環境清潔打蠟、垃圾清運及資源回收服務。",
        "requirements": "須具備環境清潔服務業登記，員工須受過專業訓練。",
        "contact": "周小姐",
        "phone": "08-8901-2345",
        "status": "投標中"
    }
]

def fetch_tenders():
    """模擬從政府採購網抓取招標公告"""
    print("📡 正在抓取政府電子採購網招標公告...")
    
    # 模擬網路延遲
    import time
    time.sleep(0.5)
    
    tenders = []
    for tender in MOCK_TENDERS:
        tenders.append({
            **tender,
            "fetch_time": datetime.now().isoformat()
        })
    
    print(f"✅ 已抓取 {len(tenders)} 筆招標公告")
    return tenders

def save_tenders(tenders, filepath=None):
    """儲存招標資料到JSON檔案"""
    if filepath is None:
        filepath = Path(__file__).parent.parent / "data" / "tenders.json"
    
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tenders, f, ensure_ascii=False, indent=2)
    
    print(f"💾 已儲存招標資料至: {filepath}")
    return filepath

def load_tenders(filepath=None):
    """讀取招標資料"""
    if filepath is None:
        filepath = Path(__file__).parent.parent / "data" / "tenders.json"
    
    filepath = Path(filepath)
    if not filepath.exists():
        return None
    
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

def filter_tenders(tenders, keyword=None, category=None, min_budget=None, status=None):
    """過濾招標資料"""
    results = tenders
    
    if keyword:
        results = [t for t in results if keyword.lower() in t["title"].lower() 
                   or keyword in t.get("description", "")]
    
    if category:
        results = [t for t in results if t["category"] == category]
    
    if min_budget:
        results = [t for t in results if t["budget"] >= min_budget]
    
    if status:
        results = [t for t in results if t["status"] == status]
    
    return results

if __name__ == "__main__":
    tenders = fetch_tenders()
    save_tenders(tenders)
    
    print("\n📋 招標公告列表:")
    for t in tenders:
        print(f"  [{t['tender_id']}] {t['title']} - 預算: {t['budget']:,}元 - 截止: {t['deadline']}")