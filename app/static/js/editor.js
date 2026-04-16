document.addEventListener('DOMContentLoaded', function() {
    var editorDiv = document.getElementById('editor');
    if (editorDiv) {
        var toolbarOptions = [
            [{ 'header': [1, 2, 3, false] }],
            ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
            ['code-block', 'link'],
            ['clean']                                         // remove formatting button
        ];

        // 讀取既有 HTML 內容（用於編輯模式），再初始化 Quill（Quill 初始化會清空 div）
        var existingContent = editorDiv.innerHTML.trim();

        var quill = new Quill('#editor', {
            modules: {
                toolbar: toolbarOptions
            },
            theme: 'snow',
            placeholder: '在此開始記錄您的學習筆記...'
        });

        // 如果有既有內容，注回編輯器
        if (existingContent && existingContent !== '<p><br></p>') {
            quill.clipboard.dangerouslyPasteHTML(existingContent);
        }

        // 提交表單前，將 Quill 生成的 HTML 注入回隱藏的 input
        // 用 closest() 找到包含 hidden-content 的那個 form（避免選到 navbar 的搜尋表單）
        var hiddenInput = document.getElementById('hidden-content');
        var form = hiddenInput ? hiddenInput.closest('form') : null;
        if (form && hiddenInput) {
            form.addEventListener('submit', function(e) {
                var htmlContent = quill.root.innerHTML;
                if (htmlContent === '<p><br></p>') {
                    htmlContent = '';
                }
                hiddenInput.value = htmlContent;
            });
        }
    }
});
