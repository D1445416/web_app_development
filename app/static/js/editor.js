document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('editor')) {
        var toolbarOptions = [
            [{ 'header': [1, 2, 3, false] }],
            ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
            ['code-block', 'link'],
            ['clean']                                         // remove formatting button
        ];

        var quill = new Quill('#editor', {
            modules: {
                toolbar: toolbarOptions
            },
            theme: 'snow',
            placeholder: '在此開始記錄您的學習筆記...'
        });

        // 提交表單前，將 Quill 生成的 HTML 注入回隱藏的 textarea
        var form = document.querySelector('form');
        var hiddenInput = document.getElementById('hidden-content');
        if (form && hiddenInput) {
            form.onsubmit = function() {
                var htmlContent = quill.root.innerHTML;
                if (htmlContent === '<p><br></p>') {
                    htmlContent = '';
                }
                hiddenInput.value = htmlContent;
                return true;
            };
        }
    }
});
