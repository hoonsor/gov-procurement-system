#!/usr/bin/env python3
"""
主排程程式
定時抓取招標資訊、發送通知、產生文件
"""

import schedule
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# 載入模組
from src.scrapers.fetch_tenders import fetch_tenders, save_tenders, load_tenders, filter_tenders
from src.email.email_notifier import EmailNotifier, check_deadlines

# 設定
CONFIG = {
    "check_interval_hours": 4,  # 檢查間隔（小時）
    "reminder_days": [3, 7],    # 提醒天數
    "email_recipients": ["business@example.com", "sales@example.com"],
    "auto_generate_docs": True,
    "tender_save_path": Path(__file__).parent / "data" / "tenders.json"
}

notifier = EmailNotifier()

def job_fetch_tenders():
    """定時抓取招標資訊"""
    print(f"\n{'='*50}")
    print(f"⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行招標抓取任務")
    print(f"{'='*50}")
    
    try:
        # 抓取新招標
        tenders = fetch_tenders()
        save_tenders(tenders, CONFIG["tender_save_path"])
        
        # 發送通知
        notifier.send_tender_notification(tenders, CONFIG["email_recipients"])
        
        print(f"✅ 招標抓取完成，共 {len(tenders)} 筆")
        return True
    except Exception as e:
        print(f"❌ 招標抓取失敗: {e}")
        return False

def job_check_deadlines():
    """檢查即將截止的招標"""
    print(f"\n{'='*50}")
    print(f"⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行截止檢查任務")
    print(f"{'='*50}")
    
    try:
        tenders = load_tenders(CONFIG["tender_save_path"])
        if not tenders:
            print("⚠️  無招標資料，跳過")
            return
        
        # 檢查各個提醒天數
        for days in CONFIG["reminder_days"]:
            urgent = check_deadlines(tenders, days_threshold=days)
            if urgent:
                print(f"📢  {days}天內截止: {len(urgent)} 筆")
                for t in urgent:
                    notifier.send_reminder(t, CONFIG["email_recipients"])
        
        print(f"✅ 截止檢查完成")
        return True
    except Exception as e:
        print(f"❌ 截止檢查失敗: {e}")
        return False

def job_generate_docs():
    """自動產生投標文件"""
    print(f"\n{'='*50}")
    print(f"⏰ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行文件產生任務")
    print(f"{'='*50}")
    
    try:
        from src.templates.bid_generator import save_bid_document, DEFAULT_COMPANY, DEFAULT_TENDER
        from src.templates.quotation_generator import save_quotation_excel, DEFAULT_LINE_ITEMS
        
        tenders = load_tenders(CONFIG["tender_save_path"])
        if not tenders:
            print("⚠️  無招標資料，跳過")
            return
        
        # 只處理7天內截止的案件
        urgent = check_deadlines(tenders, days_threshold=7)
        
        docs_dir = Path(__file__).parent / "templates"
        generated = []
        
        for t in urgent:
            # 產生投標書
            bid_path = docs_dir / f"投標書_{t['tender_id']}.docx"
            save_bid_document(t, DEFAULT_COMPANY, bid_path)
            
            # 產生估價單
            quote_path = docs_dir / f"估價單_{t['tender_id']}.xlsx"
            save_quotation_excel(t, DEFAULT_LINE_ITEMS, DEFAULT_COMPANY, quote_path)
            
            generated.append({
                "tender_id": t["tender_id"],
                "bid_doc": str(bid_path),
                "quote_doc": str(quote_path)
            })
            
            print(f"  ✅ {t['title']} 文件已產生")
        
        print(f"✅ 文件產生完成，共 {len(generated)} 組")
        return True
    except Exception as e:
        print(f"❌ 文件產生失敗: {e}")
        return False

def job_daily_report():
    """每日報告"""
    print(f"\n{'='*50}")
    print(f"📊 [{datetime.now().strftime('%Y-%m-%d')}] 每日招標報告")
    print(f"{'='*50}")
    
    try:
        tenders = load_tenders(CONFIG["tender_save_path"])
        if not tenders:
            print("⚠️  無招標資料")
            return
        
        # 統計
        total = len(tenders)
        categories = {}
        total_budget = 0
        urgent_count = 0
        
        for t in tenders:
            categories[t["category"]] = categories.get(t["category"], 0) + 1
            total_budget += t["budget"]
            
            deadline = datetime.strptime(t["deadline"], "%Y-%m-%d")
            days_left = (deadline.date() - datetime.now().date()).days
            if days_left <= 7:
                urgent_count += 1
        
        print(f"📈 總招標數: {total}")
        print(f"💰 總預算: NT$ {total_budget:,}")
        print(f"⚠️  7天內截止: {urgent_count}")
        print(f"📂 類別分布:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"    - {cat}: {count}")
        
        print(f"\n📋 即將截止案件:")
        urgent = check_deadlines(tenders, days_threshold=7)
        for t in urgent:
            deadline = datetime.strptime(t["deadline"], "%Y-%m-%d")
            days_left = (deadline.date() - datetime.now().date()).days
            print(f"    [{days_left}天] {t['title']}")
        
        return True
    except Exception as e:
        print(f"❌ 報告產生失敗: {e}")
        return False

def run_scheduler():
    """執行排程器"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║     政府採購招標系統 - 任務排程器                      ║
    ║     Government Procurement Automation System           ║
    ╠══════════════════════════════════════════════════════╣
    ║  功能:                                                 ║
    ║  • 定時抓取政府採購網招標公告                          ║
    ║  • 自動發送郵件通知                                    ║
    ║  • 投標截止提醒                                        ║
    ║  • 自動產生投標文件                                    ║
    ║  • 每日招標報告                                        ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # 排程設定
    # 每4小時抓取一次招標
    schedule.every(CONFIG["check_interval_hours"]).hours.do(job_fetch_tenders)
    
    # 每6小時檢查截止
    schedule.every(6).hours.do(job_check_deadlines)
    
    # 每天早上8點產生文件
    schedule.every().day.at("08:00").do(job_generate_docs)
    
    # 每天晚上8點產生報告
    schedule.every().day.at("20:00").do(job_daily_report)
    
    # 每30分鐘檢查截止
    schedule.every(30).minutes.do(job_check_deadlines)
    
    print("✅ 排程已設定")
    print(f"   • 每 {CONFIG['check_interval_hours']} 小時抓取招標")
    print("   • 每 6 小時檢查截止")
    print("   • 每 30 分鐘快速檢查")
    print("   • 每日 08:00 產生文件")
    print("   • 每日 20:00 產生報告")
    print("\n⏳ 等待執行...")
    print("   按 Ctrl+C 結束程式\n")
    
    # 立即執行一次
    print("\n🚀 系統啟動，先執行初始任務...\n")
    job_fetch_tenders()
    job_daily_report()
    
    # 持續執行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分鐘檢查一次

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\n\n👋 排程器已停止")
        exit(0)