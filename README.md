# Government Procurement Automation System
# 政府採購文件自動化系統

> 自動抓取政府電子採購網招標公告，產生投標文件，發送Email通知

## 功能特色

- 📡 **爬蟲抓取** - 自動抓取政府招標公告（模擬模式）
- 📄 **投標書產生** - 自動產生Word格式投標書
- 📊 **估價單產生** - 自動產生Excel格式估價單
- 📧 **Email通知** - 自動發送招標及截止提醒
- 🌐 **招標列表網站** - 互動式招標公告查詢系統
- ⏰ **任務排程** - 自動化定時執行各項任務

## 安裝需求

```bash
pip install -r requirements.txt
```

## 專案結構

```
gov-procurement-system/
├── src/
│   ├── scrapers/
│   │   └── fetch_tenders.py      # 招標爬蟲
│   ├── templates/
│   │   ├── bid_generator.py      # 投標書產生器
│   │   └── quotation_generator.py # 估價單產生器
│   ├── email/
│   │   └── email_notifier.py     # Email通知模組
│   ├── website/
│   │   └── index.html            # 招標列表網站
│   └── scheduler.py               # 任務排程主程式
├── data/                         # 招標資料儲存
├── templates/                    # 產生的文件
├── docs/                         # 文件目錄
└── requirements.txt              # Python依賴
```

## 使用方式

### 1. 抓取招標資料

```bash
python src/scrapers/fetch_tenders.py
```

### 2. 產生投標文件

```bash
# 產生投標書
python src/templates/bid_generator.py

# 產生估價單
python src/templates/quotation_generator.py
```

### 3. 執行排程器

```bash
python src/scheduler.py
```

### 4. 查看招標網站

直接用瀏覽器開啟 `src/website/index.html`

## 說明

本系統為**模擬系統**，資料為Mock Data，不會實際連線到政府採購網。

如需實際串接政府電子採購網，需申請GCB金鑰並使用其API介面。

## 技術棧

- **Python 3.8+**
- **python-docx** - Word文件產生
- **openpyxl** - Excel檔案產生
- **schedule** - 任務排程
- **Bootstrap 5** - 前端網站

## License

MIT License