document.addEventListener('DOMContentLoaded', () => {
    const toggle      = document.getElementById('chat-toggle');
    const popup       = document.getElementById('chat-popup');
    const closeBtn    = document.getElementById('close-btn');
    const chatMessages= document.getElementById('chat-messages');
    const userInput   = document.getElementById('user-input');
    const sendButton  = document.getElementById('send-button');
    const unreadBadge = document.getElementById('unread-badge');

    let isOpen = false;

    /* ── Open / Close ───────────────────────────────────── */
    const openChat = () => {
        isOpen = true;
        popup.classList.add('is-open');
        popup.setAttribute('aria-hidden', 'false');
        toggle.classList.add('is-open');
        unreadBadge.style.display = 'none';
        setTimeout(() => userInput.focus(), 220);
        scrollToBottom();
    };

    const closeChat = () => {
        isOpen = false;
        popup.classList.remove('is-open');
        popup.setAttribute('aria-hidden', 'true');
        toggle.classList.remove('is-open');
    };

    toggle.addEventListener('click', () => isOpen ? closeChat() : openChat());
    closeBtn.addEventListener('click', closeChat);

    /* ── Helpers ────────────────────────────────────────── */
    const scrollToBottom = () => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const getCurrentTime = () => {
        const n = new Date();
        return `${n.getHours().toString().padStart(2,'0')}:${n.getMinutes().toString().padStart(2,'0')}`;
    };

    /* ── Format text ────────────────────────────────────── */
    const formatText = (text) => {
        const lines = text.split('\n');
        let html = '';
        let inList = false;

        lines.forEach(line => {
            const t = line.trim();
            if (t.startsWith('* ') || t.startsWith('- ') || t.startsWith('• ')) {
                if (!inList) { html += '<ul>'; inList = true; }
                html += `<li>${t.substring(2).trim()}</li>`;
            } else if (t === '') {
                if (inList) { html += '</ul>'; inList = false; }
            } else {
                if (inList) { html += '</ul>'; inList = false; }
                html += `<p>${t}</p>`;
            }
        });
        if (inList) html += '</ul>';
        return html;
    };

    /* ── Append message ─────────────────────────────────── */
    const appendMessage = (text, sender, isError = false) => {
        const div = document.createElement('div');
        div.classList.add('message', `${sender}-message`);
        if (isError) div.classList.add('error-message');

        const content = document.createElement('div');
        content.classList.add('message-content');

        const hasMarkers = /(\* |- |• )/.test(text);
        if (hasMarkers) {
            content.innerHTML = formatText(text);
        } else {
            const p = document.createElement('p');
            p.textContent = text;
            content.appendChild(p);
        }

        const time = document.createElement('span');
        time.classList.add('message-time');
        time.textContent = getCurrentTime();
        content.appendChild(time);

        div.appendChild(content);
        chatMessages.appendChild(div);
        scrollToBottom();
    };

    /* ── Typing indicator ───────────────────────────────── */
    const showTyping = () => {
        const div = document.createElement('div');
        div.id = 'typing-indicator';
        div.classList.add('message', 'bot-message', 'typing-indicator');

        const content = document.createElement('div');
        content.classList.add('message-content');

        const dots = document.createElement('div');
        dots.classList.add('typing-dots');
        for (let i = 0; i < 3; i++) dots.appendChild(document.createElement('span'));

        content.appendChild(dots);
        div.appendChild(content);
        chatMessages.appendChild(div);
        scrollToBottom();
        return div;
    };

    const removeTyping = (el) => { if (el && el.parentNode) el.parentNode.removeChild(el); };

    /* ── Send message ───────────────────────────────────── */
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(message, 'user');
        userInput.value = '';
        sendButton.disabled = true;

        const typingEl = showTyping();

        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            removeTyping(typingEl);

            if (res.ok) {
                const data = await res.json();
                appendMessage(data.response, 'bot');
            } else {
                const err = await res.json().catch(() => ({}));
                appendMessage(err.response || 'Something went wrong. Please try again.', 'bot', true);
            }
        } catch {
            removeTyping(typingEl);
            appendMessage('Network error. Please try again.', 'bot', true);
        } finally {
            sendButton.disabled = false;
            userInput.focus();
        }
    };

    /* ── Suggestion chips ───────────────────────────────── */
    chatMessages.addEventListener('click', (e) => {
        if (!e.target.classList.contains('suggestion-btn')) return;
        const map = {
            'Our Services':  'What services does Paramount Intelligence offer?',
            'Meet the Team': 'Who are the team members at Paramount Intelligence?',
            'About Us':      'Tell me about Paramount Intelligence company'
        };
        const query = map[e.target.textContent.trim()] || e.target.textContent.trim();
        userInput.value = query;
        sendMessage();
    });

    /* ── Events ─────────────────────────────────────────── */
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

    scrollToBottom();
});
