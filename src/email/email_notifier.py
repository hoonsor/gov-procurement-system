#!/usr/bin/env python3
"""
Email 通知模組
自動發送招標資訊及投標提醒
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from pathlib import Path

# 模擬發送（實際環境需設定 SMTP）
MOCK_MODE = True

class EmailNotifier:
    def __init__(self, smtp_config=None):
        """初始化郵件發送器"""
        self.smtp_config = smtp_config or {
            "server": "smtp.gmail.com",
            "port": 587,
            "username": "your-email@gmail.com",
            "password": "your-app-password"
        }
        self.mock_mode = MOCK_MODE
    
    def send_tender_notification(self, tenders, recipients):
        """發送招標通知郵件"""
        subject = f"📢 政府採購招標公告 {datetime.now().strftime('%Y/%m/%d')}"
        
        body = self._build_tender_email_body(tenders)
        
        return self._send_email(recipients, subject, body)
    
    def send_reminder(self, tender, recipients):
        """發送投標截止提醒"""
        deadline = datetime.strptime(tender["deadline"], "%Y-%m-%d")
        days_left = (deadline - datetime.now().date()).days
        
        subject = f"⚠️ 投標提醒：{tender['title']} ({days_left}天後截止)"
        
        body = f"""
<h2>投標截止提醒</h2>
<p>親愛的業務團隊：</p>
<p>有一個採購案即將截止投標，請注意：</p>

<table style="border-collapse: collapse; width: 100%;">
<tr style="background-color: #f2f2f2;">
    <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">項目</th>
    <th style="padding: 10px; border: 1px solid #ddd;">內容</th>
</tr>
<tr>
    <td style="padding: 10px; border: 1px solid #ddd;">採購案號</td>
    <td style="padding: 10px; border: 1px solid #ddd;">{tender['tender_id']}</td>
</tr>
<tr>
    <td style="padding: 10px; border: 1px solid #ddd;">採購名稱</td>
    <td style="padding: 10px; border: 1px solid #ddd;">{tender['title']}</td>
</tr>
<tr>
    <td style="padding: 10px; border: 1px solid #ddd;">預算金額</td>
    <td style="padding: 10px; border: 1px solid #ddd;">NT$ {tender['budget']:,}</td>
</tr>
<tr>
    <td style="padding: 10px; border: 1px solid #ddd;">截止日期</td>
    <td style="padding: 10px; border: 1px solid #ddd; color: red; font-weight: bold;">{tender['deadline']} ({days_left}天)</td>
</tr>
<tr>
    <td style="padding: 10px; border: 1px solid #ddd;">機關</td>
    <td style="padding: 10px; border: 1px solid #ddd;">{tender['agency']} / {tender['department']}</td>
</tr>
<tr>
    <td style="padding: 10px; border: 1px solid #ddd;">聯絡人</td>
    <td style="padding: 10px; border: 1px solid #ddd;">{tender['contact']} ({tender['phone']})</td>
</tr>
</table>

<h3>📋 投標說明</h3>
<p>{tender.get('description', '請查閱完整投標文件。')}</p>

<p style="color: #666;">此郵件由系統自動發送，請勿回覆。</p>
"""
        
        return self._send_email(recipients, subject, body)
    
    def send_bid_document(self, doc_path, recipients, tender_info):
        """發送投標文件"""
        subject = f"📎 投標文件：{tender_info['title']}"
        
        body = f"""
<h2>投標文件已準備完成</h2>
<p>採購案號：{tender_info['tender_id']}</p>
<p>採購名稱：{tender_info['title']}</p>
<p>投標金額：NT$ {tender_info.get('bid_amount', 0):,}</p>
<p>投標截止：{tender_info['deadline']}</p>

<p>附件已隨郵件寄出，請檢視後按時投標。</p>
"""
        
        attachments = [doc_path] if isinstance(doc_path, (str, Path)) else doc_path
        
        return self._send_email(recipients, subject, body, attachments)
    
    def _build_tender_email_body(self, tenders):
        """建構招標通知郵件內容"""
        html = """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<h2>📢 政府採購招標公告</h2>
<p>以下是今日最新招標資訊：</p>
"""
        
        for t in tenders:
            deadline = datetime.strptime(t["deadline"], "%Y-%m-%d")
            days_left = (deadline - datetime.now().date()).days
            
            status_color = "red" if days_left <= 7 else ("orange" if days_left <= 14 else "green")
            
            html += f"""
<hr>
<h3 style="color: #2c5aa0;">{t['title']}</h3>
<table style="border-collapse: collapse; width: 100%; max-width: 600px;">
<tr><td style="padding: 5px;"><strong>案號：</strong></td><td>{t['tender_id']}</td></tr>
<tr><td style="padding: 5px;"><strong>機關：</strong></td><td>{t['agency']} / {t['department']}</td></tr>
<tr><td style="padding: 5px;"><strong>預算：</strong></td><td>NT$ {t['budget']:,}</td></tr>
<tr><td style="padding: 5px;"><strong>截止：</strong></td><td style="color: {status_color};">{t['deadline']} ({days_left}天)</td></tr>
<tr><td style="padding: 5px;"><strong>分類：</strong></td><td>{t['category']}</td></tr>
</table>
<p style="color: #666; font-size: 14px;">{t.get('description', '')}</p>
"""
        
        html += """
<hr>
<p style="color: #999; font-size: 12px;">
此郵件由系統自動發送，如有任何問題請聯絡管理員。<br>
如不再收到此類通知，請回覆告知。
</p>
</body>
</html>
"""
        
        return html
    
    def _send_email(self, recipients, subject, body_html, attachments=None):
        """發送郵件"""
        if self.mock_mode:
            return self._mock_send(recipients, subject, body_html, attachments)
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_config['username']
            msg['To'] = ', '.join(recipients) if isinstance(recipients, list) else recipients
            
            msg.attach(MIMEText(body_html, 'html', 'utf-8'))
            
            # 附加檔案
            if attachments:
                for file_path in attachments:
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment', 
                                  filename=Path(file_path).name.encode('utf-8'))
                    msg.attach(part)
            
            # 發送郵件
            with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.smtp_config['username'], self.smtp_config['password'])
                server.send_message(msg)
            
            print(f"✅ 郵件已發送至: {recipients}")
            return True
            
        except Exception as e:
            print(f"❌ 郵件發送失敗: {e}")
            return False
    
    def _mock_send(self, recipients, subject, body_html, attachments):
        """模擬發送郵件"""
        print("="*60)
        print("📧 [MOCK MODE] 模擬發送郵件")
        print(f"   收件人: {recipients}")
        print(f"   主題: {subject}")
        print("-"*60)
        print("郵件內容預覽（純文字版本）:")
        # 簡化顯示
        import re
        text = re.sub('<[^>]+>', '', body_html)[:500]
        print(text[:300] + "..." if len(text) > 300 else text)
        print("="*60)
        return True

def check_deadlines(tenders, days_threshold=7):
    """檢查即將截止的招標"""
    urgent = []
    
    for t in tenders:
        deadline = datetime.strptime(t["deadline"], "%Y-%m-%d")
        days_left = (deadline - datetime.now().date()).days
        
        if 0 <= days_left <= days_threshold:
            urgent.append({**t, "days_left": days_left})
    
    return sorted(urgent, key=lambda x: x["days_left"])

# 測試
if __name__ == "__main__":
    from pathlib import Path
    
    # 測試招標通知
    sample_tenders = [
        {
            "tender_id": "TP-2026-001",
            "title": "校園網路設備更新採購案",
            "agency": "教育部",
            "department": "資訊中心",
            "budget": 2500000,
            "deadline": "2026-05-25",
            "description": "採購網路設備及安裝服務"
        },
        {
            "tender_id": "TP-2026-006",
            "title": "辦公室文具用品採購",
            "agency": "行政院",
            "department": "總務處",
            "budget": 500000,
            "deadline": "2026-05-20",
            "description": "年度文具採購"
        }
    ]
    
    notifier = EmailNotifier()
    
    print("\n測試1: 發送招標通知")
    notifier.send_tender_notification(sample_tenders, ["business@example.com"])
    
    print("\n測試2: 發送截止提醒")
    notifier.send_reminder(sample_tenders[0], ["sales@example.com"])
    
    print("\n測試3: 檢查即將截止案件")
    urgent = check_deadlines(sample_tenders, days_threshold=14)
    print(f"即將截止案件數: {len(urgent)}")
    for t in urgent:
        print(f"  [{t['days_left']}天] {t['title']}")