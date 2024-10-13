document.addEventListener('DOMContentLoaded', function() {
    const participateButtons = document.querySelectorAll('.participate-button');
    participateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const eventId = button.dataset.eventId;
            fetch(`/event/${eventId}/participate/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('イベントに参加しました！');
                    button.disabled = true;
                    button.textContent = '参加済み';
                } else {
                    alert('既に参加済みです。');
                }
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
