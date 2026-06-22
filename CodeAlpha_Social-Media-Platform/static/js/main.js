// ===== CSRF helper =====
function getCsrf() {
    return window.CSRF_TOKEN ||
        document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
        document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
}

// ===== Like =====
document.addEventListener('click', function (e) {
    const btn = e.target.closest('.like-btn');
    if (!btn) return;
    const postId = btn.dataset.postId;
    const csrf = btn.dataset.csrf || getCsrf();

    fetch(`/post/${postId}/like/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' },
    })
        .then(r => r.json())
        .then(data => {
            if (data.liked !== undefined) {
                btn.classList.toggle('liked', data.liked);
                btn.innerHTML = data.liked
                    ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg> Unlike`
                    : `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg> Like`;
                const counter = document.getElementById(`likes-count-${postId}`);
                if (counter) counter.textContent = data.count;
            }
        })
        .catch(console.error);
});

// ===== Comments Toggle =====
document.addEventListener('click', function (e) {
    const btn = e.target.closest('.comment-toggle-btn');
    if (!btn) return;
    const postId = btn.dataset.postId;
    const section = document.getElementById(`comments-${postId}`);
    if (section) {
        const isOpen = section.style.display !== 'none';
        section.style.display = isOpen ? 'none' : 'block';
        if (!isOpen) section.querySelector('.comment-input')?.focus();
    }
});

// ===== Submit Comment =====
document.addEventListener('submit', function (e) {
    const form = e.target.closest('.comment-form');
    if (!form) return;
    e.preventDefault();

    const postId = form.dataset.postId;
    const csrf = form.dataset.csrf || getCsrf();
    const input = form.querySelector('.comment-input');
    const content = input.value.trim();
    if (!content) return;

    fetch(`/post/${postId}/comment/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `content=${encodeURIComponent(content)}`,
    })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                input.value = '';
                const list = document.getElementById(`comments-list-${postId}`);
                const noComments = document.getElementById(`no-comments-${postId}`);
                if (noComments) noComments.remove();

                const html = `
                <div class="comment" id="comment-${data.comment_id}">
                    <a href="/profile/${data.author}/"><img src="${data.author_avatar}" alt="${data.author}" class="avatar avatar-xs"></a>
                    <div class="comment-body">
                        <div class="comment-header">
                            <a href="/profile/${data.author}/" class="comment-author">${data.author}</a>
                            <span class="comment-time">just now</span>
                            <button class="btn-delete-comment" data-comment-id="${data.comment_id}" data-post-id="${postId}" data-csrf="${csrf}">×</button>
                        </div>
                        <p class="comment-text">${escapeHtml(data.content)}</p>
                    </div>
                </div>`;
                list.insertAdjacentHTML('beforeend', html);
                const counter = document.getElementById(`comments-count-${postId}`);
                if (counter) counter.textContent = data.count;
                list.scrollTop = list.scrollHeight;
            }
        })
        .catch(console.error);
});

// ===== Delete Comment =====
document.addEventListener('click', function (e) {
    const btn = e.target.closest('.btn-delete-comment');
    if (!btn) return;
    const commentId = btn.dataset.commentId;
    const postId = btn.dataset.postId;
    const csrf = btn.dataset.csrf || getCsrf();

    if (!confirm('Delete this comment?')) return;

    fetch(`/comment/${commentId}/delete/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' },
    })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`comment-${commentId}`)?.remove();
                const counter = document.getElementById(`comments-count-${postId}`);
                if (counter) counter.textContent = data.count;
            }
        })
        .catch(console.error);
});

// ===== Follow/Unfollow =====
document.addEventListener('click', function (e) {
    const btn = e.target.closest('.follow-btn');
    if (!btn) return;
    const username = btn.dataset.username;
    const csrf = btn.dataset.csrf || getCsrf();

    fetch(`/profile/${username}/follow/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' },
    })
        .then(r => r.json())
        .then(data => {
            if (data.following !== undefined) {
                btn.textContent = data.following ? 'Following' : 'Follow';
                btn.classList.toggle('btn-primary', !data.following);
                btn.classList.toggle('btn-outline', data.following);

                const followersEl = document.getElementById('followers-count');
                if (followersEl) followersEl.textContent = data.followers_count;
            }
        })
        .catch(console.error);
});

// ===== Post Composer Toggle =====
const composerToggle = document.getElementById('composerToggle');
const composerBody = document.getElementById('composerBody');
if (composerToggle && composerBody) {
    composerToggle.addEventListener('click', () => {
        const open = composerBody.style.display !== 'none';
        composerBody.style.display = open ? 'none' : 'block';
        if (!open) document.getElementById('postContent')?.focus();
    });
}

// ===== Image file name preview =====
const postImage = document.getElementById('postImage');
if (postImage) {
    postImage.addEventListener('change', () => {
        const nameEl = document.getElementById('imageFileName');
        if (nameEl) nameEl.textContent = postImage.files[0]?.name || '';
    });
}

// ===== Dropdown menus =====
function toggleMenu(btn) {
    const menu = btn.nextElementSibling;
    menu.classList.toggle('open');
}

document.addEventListener('click', function (e) {
    if (!e.target.closest('.post-actions-menu')) {
        document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
    }
});

// ===== Modals =====
function toggleModal(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = el.style.display === 'none' ? 'flex' : 'none';
}

function closeModal(e, id) {
    if (e.target.classList.contains('modal-overlay')) toggleModal(id);
}

// ===== Auto-dismiss alerts =====
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        alert.style.transition = 'opacity 0.5s';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    }, 4000);
});

// ===== Escape HTML helper =====
function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// ===== Real-time Notification System =====
(function () {
    if (!window.NOTIF_UNREAD_URL) return; // Only runs when logged in

    const badge = document.getElementById('notifBadge');
    const toastContainer = document.getElementById('toastContainer');
    // Track IDs we have already toasted so repeat polls don't re-show them
    const seen = new Set();

    const ICONS = {
        like: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>`,
        comment: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18z"/></svg>`,
        follow: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>`,
    };

    function showToast(n) {
        if (!toastContainer) return;
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `
            <img class="toast-avatar" src="${n.sender_avatar}" alt="${n.sender}">
            <div class="toast-body">
                <div class="toast-msg">${escapeHtml(n.message)}</div>
                <div class="toast-time">${n.time}</div>
            </div>
            <div class="toast-icon ${n.type}">${ICONS[n.type] || ''}</div>
            <button class="toast-close" aria-label="Dismiss">&times;</button>`;

        toast.querySelector('.toast-close').addEventListener('click', () => dismissToast(toast));
        toastContainer.appendChild(toast);

        // Auto-dismiss after 5 s
        setTimeout(() => dismissToast(toast), 5000);
    }

    function dismissToast(toast) {
        if (!toast.parentNode) return;
        toast.classList.add('toast-out');
        setTimeout(() => toast.remove(), 300);
    }

    function updateBadge(count) {
        if (!badge) return;
        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }

    function poll() {
        fetch(window.NOTIF_UNREAD_URL, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
        })
            .then(r => r.json())
            .then(data => {
                updateBadge(data.count);

                // If we're on the notifications page, mark all read immediately
                if (window.IS_NOTIF_PAGE && data.count > 0) {
                    fetch(window.NOTIF_MARK_READ_URL, {
                        method: 'POST',
                        headers: { 'X-CSRFToken': getCsrf(), 'X-Requested-With': 'XMLHttpRequest' },
                    });
                    return;
                }

                // Show a toast for each new notification
                data.notifications.forEach(n => {
                    if (!seen.has(n.id)) {
                        seen.add(n.id);
                        showToast(n);
                    }
                });
            })
            .catch(() => {}); // silently ignore network errors
    }

    // First poll after 2 s (page just loaded), then every 10 s
    setTimeout(poll, 2000);
    setInterval(poll, 10000);

    // When the user clicks the bell, mark all as read and clear the badge
    document.getElementById('notifBellLink')?.addEventListener('click', () => {
        fetch(window.NOTIF_MARK_READ_URL, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrf(), 'X-Requested-With': 'XMLHttpRequest' },
        });
        updateBadge(0);
    });
})();
