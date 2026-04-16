# 🛣️ 讀書筆記本系統 — 路由設計文件（ROUTES）

> **版本**：v1.0  
> **建立日期**：2026-04-16  
> **狀態**：完成

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| **首頁與搜尋** (`main.py`) |
| 首頁 (科目列表) | GET | `/` | `index.html` | 顯示所有科目列表 |
| 全文搜尋 | GET | `/search` | `search.html` | 全文關鍵字搜尋結果 |
| **科目管理** (`subjects.py`) |
| 建立科目頁面 | GET | `/subjects/create` | `subjects/create.html` | 顯示建立科目表單 |
| 建立科目處理 | POST | `/subjects/create` | — | 儲存新科目，重導向至首頁 |
| 科目詳細頁 | GET | `/subjects/<id>` | `subjects/detail.html` | 顯示科目下所有筆記清單 |
| 刪除科目 | POST | `/subjects/<id>/delete` | — | 刪除科目及其筆記，重導向至首頁 |
| **筆記管理** (`notes.py`) |
| 建立筆記頁面 | GET | `/subjects/<id>/notes/create` | `notes/create.html` | 顯示筆記編輯器表單 |
| 建立筆記處理 | POST | `/subjects/<id>/notes/create` | — | 寫入筆記資料庫，跳轉至科目頁 |
| 筆記詳情頁 | GET | `/notes/<id>` | `notes/view.html` | 唯讀顯示單篇筆記內容 |
| 編輯筆記頁面 | GET | `/notes/<id>/edit` | `notes/edit.html` | 載入現有筆記內容至編輯器 |
| 編輯筆記處理 | POST | `/notes/<id>/edit` | — | 更新筆記內容，重導向回筆記頁 |
| 刪除筆記 | POST | `/notes/<id>/delete` | — | 刪除筆記，重導向回科目頁 |
| 筆記關聯標籤 | POST | `/notes/<id>/tags` | — | 為筆記附加自訂標籤 |
| **統整摘要** (`summary.py`) |
| 產生科目摘要 | GET | `/subjects/<id>/summary` | `notes/summary.html` | 顯示此科目下所有筆記的整合視圖 |
| **筆記匯出** (`export.py`) |
| 匯出 PDF | GET | `/notes/<id>/export/pdf` | — | 產出 PDF 格式並回應下載串流 |
| 匯出 Markdown | GET | `/notes/<id>/export/md`  | — | 產出 Markdown 檔案並下載 |
| **標籤管理** (`tags.py`) |
| 標籤列表 | GET | `/tags` | `tags/list.html` | 列出目前所有系統存在的標籤 |
| 建立新標籤 | POST | `/tags/create` | — | 從表單接收標籤名與顏色並建立 |
| 依標籤篩選 | GET | `/tags/<id>/notes` | `tags/notes_by_tag.html` | 顯示具有該標籤的所有筆記 |
| **共用連結協作** (`share.py`) |
| 產生共用連結 | POST | `/notes/<id>/share` | — | 依據選擇權限產生 UUID token 的連結 |
| 存取共用連結 | GET | `/share/<token>` | `notes/share_view.html` 或是 `notes/share_edit.html` | 有效期限驗證，給予對應權限頁面 |
| 共用編輯儲存 | POST | `/share/<token>/save` | — | 外部使用者送出儲存修改內容 |
| **管理者後台** (`admin.py`) |
| 管理員登入頁 | GET | `/admin/login` | `admin/login.html` | 登入表單 |
| 登入處理 | POST | `/admin/login` | — | 檢查帳密，正確發 session |
| 登出 | POST | `/admin/logout` | — | 清除 admin session，重導至首頁 |
| 後台首頁 | GET | `/admin/dashboard`| `admin/dashboard.html`| 顯示管理面板與總覽 |
| 管理筆記列表 | GET | `/admin/notes` | `admin/notes.html` | 檢視所有筆記、搜尋或執行管理 |
| 強制刪除筆記 | POST | `/admin/notes/<id>/delete`| — | 管理員專用刪除端點 |
| 檢視共用連結 | GET | `/admin/links` | `admin/links.html` | 顯示所有被分享中的連結 |
| 撤銷共用連結 | POST | `/admin/links/<id>/revoke`| — | 使某個 uuid 連結立刻失效 |

---

## 2. 每個路由的詳細說明範例

### 建立科目處理 (`POST /subjects/create`)
- **輸入**：表單中的 `name` 欄位。
- **處理邏輯**：
  檢查 `name` 是否空白。若無，呼叫 `Subject.create(name=name)`。
- **輸出**：重新導向到 `/`。
- **錯誤處理**：如果 `name` 空白，顯示 flash 訊息，並重導向回 GET 表單。

### 存取共用連結 (`GET /share/<token>`)
- **輸入**：URL 參數 `token`。
- **處理邏輯**：
  呼叫 `ShareLink.get_by_token(token)`。確認 token 存在。若無效回傳 404/錯誤頁面。如果存在，取出其對應的 `Note` 物件。依據權限（read/edit）選擇對應的操作環境。
- **輸出**：返回對應權限的 HTML。

*(其餘路由比照上述標準 CRUD 運作。)*

---

## 3. Jinja2 模板清單

皆繼承自 `base.html`，以符合外觀一致性：

- `base.html`：共用版型（ Navbar, 載入 JS/CSS 資源, Footer）。
- `index.html`：首頁、呈現所有 `Subject`。
- `search.html`：輸入搜尋，並顯示查出的 `Note` 列表。
- **科目模組**：
  - `subjects/create.html`
  - `subjects/detail.html`
- **筆記模組**：
  - `notes/create.html`
  - `notes/view.html`
  - `notes/edit.html`
  - `notes/summary.html`
  - `notes/share_view.html` (唯讀分享頁面，可隱藏選單)
  - `notes/share_edit.html` (可編輯分享頁面)
- **標籤模組**：
  - `tags/list.html`
  - `tags/notes_by_tag.html`
- **後台管理**：
  - `admin/login.html`
  - `admin/dashboard.html`
  - `admin/notes.html`
  - `admin/links.html`

---

## 4. 路由骨架程式碼

相關檔案皆建立於 `app/routes/` 目錄下：
- `main.py`
- `subjects.py`
- `notes.py`
- `summary.py`
- `export.py`
- `tags.py`
- `share.py`
- `admin.py`
