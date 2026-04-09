# 📊 讀書筆記本系統 — 流程圖文件（FLOWCHART）

> **版本**：v1.0  
> **建立日期**：2026-04-09  
> **參考文件**：docs/PRD.md v1.0、docs/ARCHITECTURE.md v1.0

---

## 1. 使用者流程圖（User Flow）

描述不同角色（學生、共用者、管理者）從進入網站到完成操作的完整路徑。

### 1.1 學生主要操作流程

```mermaid
flowchart LR
    Start([🌐 開啟網站]) --> Home[首頁\n科目列表]

    Home --> |新增科目| SubjectCreate[填寫科目名稱]
    SubjectCreate --> SubjectSaved[科目已建立]
    SubjectSaved --> Home

    Home --> |選擇科目| SubjectDetail[科目頁面\n筆記列表]

    SubjectDetail --> |新增筆記| NoteCreate[填寫標題 + 富文字編輯]
    NoteCreate --> |儲存| NoteSaved[筆記已建立]
    NoteSaved --> SubjectDetail

    SubjectDetail --> |點擊筆記| NoteView[閱讀筆記]
    NoteView --> |編輯| NoteEdit[編輯模式]
    NoteEdit --> |儲存| NoteView
    NoteView --> |產生共用連結| ShareCreate{設定權限}
    ShareCreate --> |可編輯| ShareLinkEdit[產生可編輯連結]
    ShareCreate --> |唯讀| ShareLinkRead[產生唯讀連結]

    SubjectDetail --> |統整摘要| Summary[摘要頁面\n各筆記標題 + 要點]

    Home --> |搜尋關鍵字| Search[搜尋頁面]
    Search --> |點擊結果| NoteView

    NoteView --> |加標籤| TagManage[標籤管理]
    TagManage --> |篩選| TagFilter[依標籤瀏覽筆記]

    NoteView --> |匯出| Export{選擇格式}
    Export --> |PDF| ExportPDF[下載 PDF]
    Export --> |Markdown| ExportMD[下載 .md 檔]
```

---

### 1.2 共用者（無帳號）操作流程

```mermaid
flowchart LR
    ShareURL([📎 收到共用連結]) --> TokenCheck{Token 驗證}
    TokenCheck --> |無效 / 已過期| ErrorPage[錯誤頁面\n連結已失效]
    TokenCheck --> |有效| PermCheck{權限判斷}
    PermCheck --> |唯讀| ReadOnly[閱讀筆記\n無編輯按鈕]
    PermCheck --> |可編輯| EditMode[進入編輯模式]
    EditMode --> |修改並儲存| SaveNote[POST 更新筆記]
    SaveNote --> EditMode
```

---

### 1.3 管理者操作流程

```mermaid
flowchart LR
    AdminURL([🔐 進入 /admin/login]) --> LoginForm[輸入管理者密碼]
    LoginForm --> AuthCheck{密碼驗證}
    AuthCheck --> |失敗| LoginFail[顯示錯誤訊息]
    LoginFail --> LoginForm
    AuthCheck --> |成功| Dashboard[管理後台首頁]

    Dashboard --> ManageNotes[瀏覽所有筆記列表]
    ManageNotes --> |刪除筆記| ConfirmDelete{確認刪除？}
    ConfirmDelete --> |確定| NoteDeleted[筆記已刪除]
    ConfirmDelete --> |取消| ManageNotes

    Dashboard --> ManageLinks[管理共用連結列表]
    ManageLinks --> |撤銷連結| LinkRevoked[連結已撤銷]

    Dashboard --> |登出| Logout([結束管理工作階段])
```

---

## 2. 系統序列圖（Sequence Diagram）

描述使用者操作到資料庫存取的完整技術流程。

### 2.1 新增筆記

```mermaid
sequenceDiagram
    actor Student as 👤 學生
    participant Browser as 瀏覽器
    participant Flask as Flask Route\nnotes.py
    participant Model as Note Model\napp/models/note.py
    participant DB as SQLite\ninstance/database.db

    Student->>Browser: 點擊「新增筆記」
    Browser->>Flask: GET /subjects/{id}/notes/create
    Flask->>Browser: 回傳 notes/create.html（含 Quill 編輯器）

    Student->>Browser: 輸入標題與內容，點擊「儲存」
    Browser->>Flask: POST /subjects/{id}/notes
    Flask->>Model: Note(title, content, subject_id)
    Model->>DB: INSERT INTO notes (title, content, subject_id, created_at)
    DB-->>Model: 新筆記 ID
    Model-->>Flask: note 物件
    Flask-->>Browser: redirect → /notes/{id}
    Browser->>Flask: GET /notes/{id}
    Flask-->>Browser: 渲染 notes/view.html
```

---

### 2.2 產生共用連結

```mermaid
sequenceDiagram
    actor Student as 👤 學生
    participant Browser as 瀏覽器
    participant Flask as Flask Route\nshare.py
    participant Model as ShareLink Model
    participant DB as SQLite

    Student->>Browser: 點擊「產生共用連結」+ 選擇權限
    Browser->>Flask: POST /notes/{id}/share\n{ permission: "edit" }
    Flask->>Model: ShareLink(note_id, token=uuid4(), permission)
    Model->>DB: INSERT INTO share_links (note_id, token, permission, created_at)
    DB-->>Model: 成功
    Model-->>Flask: token
    Flask-->>Browser: 回傳分享網址\n/share/{token}
    Browser->>Student: 顯示可複製的連結
```

---

### 2.3 共用者透過連結編輯

```mermaid
sequenceDiagram
    actor Guest as 👥 共用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\nshare.py
    participant Model as ShareLink + Note Model
    participant DB as SQLite

    Guest->>Browser: 開啟 /share/{token}
    Browser->>Flask: GET /share/{token}
    Flask->>DB: SELECT * FROM share_links WHERE token = ?
    DB-->>Flask: ShareLink 資料（permission, note_id）

    alt Token 無效或過期
        Flask-->>Browser: 渲染 error.html（連結失效）
    else Token 有效
        Flask->>DB: SELECT * FROM notes WHERE id = note_id
        DB-->>Flask: 筆記資料
        Flask-->>Browser: 渲染 notes/edit.html 或 notes/view.html
    end

    Guest->>Browser: 修改內容並儲存
    Browser->>Flask: POST /share/{token}/save\n{ content: "..." }
    Flask->>DB: UPDATE notes SET content = ? WHERE id = ?
    DB-->>Flask: 成功
    Flask-->>Browser: redirect → GET /share/{token}
```

---

### 2.4 全文搜尋

```mermaid
sequenceDiagram
    actor Student as 👤 學生
    participant Browser as 瀏覽器
    participant Flask as Flask Route\nmain.py
    participant DB as SQLite

    Student->>Browser: 在搜尋框輸入關鍵字並送出
    Browser->>Flask: GET /search?q=關鍵字&subject_id=（可選）
    Flask->>DB: SELECT * FROM notes\nWHERE content LIKE '%關鍵字%'\nOR title LIKE '%關鍵字%'
    DB-->>Flask: 符合的筆記列表
    Flask-->>Browser: 渲染 search.html\n（含關鍵字高亮）
```

---

### 2.5 管理者登入與刪除筆記

```mermaid
sequenceDiagram
    actor Admin as 🔐 管理者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\nadmin.py
    participant DB as SQLite

    Admin->>Browser: 輸入密碼並送出
    Browser->>Flask: POST /admin/login\n{ password: "..." }
    Flask->>DB: SELECT password_hash FROM admins
    DB-->>Flask: password_hash
    Flask->>Flask: check_password_hash(hash, password)

    alt 密碼正確
        Flask->>Flask: session["is_admin"] = True
        Flask-->>Browser: redirect → /admin/dashboard
    else 密碼錯誤
        Flask-->>Browser: 回傳登入頁 + 錯誤訊息
    end

    Admin->>Browser: 點擊「刪除筆記」
    Browser->>Flask: POST /admin/notes/{id}/delete
    Flask->>Flask: 檢查 session["is_admin"]
    Flask->>DB: DELETE FROM notes WHERE id = ?
    DB-->>Flask: 成功
    Flask-->>Browser: redirect → /admin/notes
```

---

## 3. 功能清單對照表

| 功能 | 說明 | URL 路徑 | HTTP 方法 |
|------|------|----------|-----------|
| 首頁 | 顯示所有科目列表 | `/` | GET |
| 新增科目 | 填寫科目名稱並建立 | `/subjects/create` | GET / POST |
| 科目詳細頁 | 顯示科目下所有筆記 | `/subjects/<id>` | GET |
| 刪除科目 | 刪除指定科目 | `/subjects/<id>/delete` | POST |
| 新增筆記 | 富文字編輯並建立筆記 | `/subjects/<id>/notes/create` | GET / POST |
| 閱讀筆記 | 顯示筆記內容（唯讀） | `/notes/<id>` | GET |
| 編輯筆記 | 修改筆記內容 | `/notes/<id>/edit` | GET / POST |
| 刪除筆記 | 刪除指定筆記 | `/notes/<id>/delete` | POST |
| 統整摘要 | 顯示科目下筆記摘要 | `/subjects/<id>/summary` | GET |
| 全文搜尋 | 關鍵字搜尋所有筆記 | `/search?q=<keyword>` | GET |
| 標籤列表 | 顯示所有標籤 | `/tags` | GET |
| 新增標籤 | 建立自訂標籤 | `/tags/create` | POST |
| 筆記加標籤 | 為筆記指定標籤 | `/notes/<id>/tags` | POST |
| 依標籤篩選 | 顯示特定標籤的筆記 | `/tags/<id>/notes` | GET |
| 產生共用連結 | 建立 UUID 分享連結 | `/notes/<id>/share` | POST |
| 共用連結存取 | 透過 Token 開啟筆記 | `/share/<token>` | GET |
| 共用連結儲存 | 透過 Token 儲存編輯 | `/share/<token>/save` | POST |
| 匯出 PDF | 下載筆記 PDF | `/notes/<id>/export/pdf` | GET |
| 匯出 Markdown | 下載筆記 .md | `/notes/<id>/export/md` | GET |
| 管理者登入 | 驗證管理者密碼 | `/admin/login` | GET / POST |
| 管理者後台 | 管理者儀表板 | `/admin/dashboard` | GET |
| 管理筆記列表 | 瀏覽所有筆記 | `/admin/notes` | GET |
| 管理者刪除筆記 | 強制刪除任意筆記 | `/admin/notes/<id>/delete` | POST |
| 管理共用連結 | 查看 / 撤銷共用連結 | `/admin/links` | GET |
| 撤銷共用連結 | 停用指定 Token | `/admin/links/<id>/revoke` | POST |
| 管理者登出 | 清除管理 Session | `/admin/logout` | POST |

---

*本文件由 Antigravity AI 輔助產出，Mermaid 圖可直接在 GitHub / Notion 預覽渲染。*
