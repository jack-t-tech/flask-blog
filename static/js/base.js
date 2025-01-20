// フラッシュメッセージを3秒後に非表示にする
document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach((message) => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500); // フェードアウト後に完全に削除
        }, 3000); // 3秒後に実行
    });
});