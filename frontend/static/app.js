document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatHistory = document.getElementById('chat-history');
    const gcStandardToggle = document.getElementById('gc-standard');
    
    // Config targeting the agent engine (running on 8000 ideally)
    const AGENT_URL = 'http://localhost:8000/chat';

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = chatInput.value.trim();
        if(!message) return;
        
        // Check if there is extra context
        const standardPreference = gcStandardToggle.value;
        const enrichedMessage = `[Standard Applied: ${standardPreference}] ${message}`;

        // Add user message to UI
        addMessageToUI('user', message);
        chatInput.value = '';
        
        // Create an empty agent message space
        const assistantMessageEl = createMessageSpace('system');
        const contentDiv = assistantMessageEl.querySelector('.message-content');
        
        // Add typing indicator
        contentDiv.innerHTML = `<div class="typing-indicator"><span></span><span></span><span></span></div>`;
        
        try {
            await streamResponse(enrichedMessage, contentDiv);
        } catch (error) {
            console.error('Streaming error:', error);
            contentDiv.innerHTML = `<p style="color: var(--danger)">Connection to Local Agent failed. Is the server running?</p>`;
        }
    });
    
    const doubleCheckBtn = document.getElementById('double-check-btn');
    if (doubleCheckBtn) {
        doubleCheckBtn.addEventListener('click', async () => {
            const standardPreference = gcStandardToggle.value;
            const prompt = `[Standard Applied: ${standardPreference}] Please ask me a critical, specific pre-task planning verification question to make sure I am not missing any hazards. Do not explain yourself, just ask the question directly.`;
            
            // Create an empty agent message space without creating a user message space first
            const assistantMessageEl = createMessageSpace('system');
            const contentDiv = assistantMessageEl.querySelector('.message-content');
            
            // Add typing indicator
            contentDiv.innerHTML = `<div class="typing-indicator"><span></span><span></span><span></span></div>`;
            
            try {
                await streamResponse(prompt, contentDiv);
            } catch (error) {
                console.error('Streaming error:', error);
                contentDiv.innerHTML = `<p style="color: var(--danger)">Connection to Local Agent failed. Is the server running?</p>`;
            }
        });
    }

    function addMessageToUI(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}-msg`;
        
        const avatarIcon = role === 'user' ? 'fa-user' : 'fa-robot';
        
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fas ${avatarIcon}"></i></div>
            <div class="message-content">
                <p>${escapeHTML(text)}</p>
            </div>
        `;
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
    }

    function createMessageSpace(role) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}-msg`;
        const avatarIcon = role === 'user' ? 'fa-user' : 'fa-robot';
        
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fas ${avatarIcon}"></i></div>
            <div class="message-content"></div>
        `;
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
        return msgDiv;
    }

    async function streamResponse(message, contentElement) {
        // Prepare request
        const response = await fetch(AGENT_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: "demo-session-mortenson"
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let accumulatedText = "";
        let firstDataReceived = false;
        let textContainer = null;
        
        while (true) {
            const {done, value} = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, {stream: true});
            // SSE chunks can be large and contain multiple data: lines
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const dataStr = line.substring(6);
                    if (!dataStr) continue;
                    
                    try {
                        const data = JSON.parse(dataStr);
                        
                        // Clear the typing indicator only once real data arrives
                        if (!firstDataReceived) {
                            firstDataReceived = true;
                            contentElement.innerHTML = '';
                            textContainer = document.createElement('div');
                            contentElement.appendChild(textContainer);
                        }
                        
                        if (data.text) {
                            accumulatedText += data.text;
                            textContainer.innerHTML = marked.parse(accumulatedText);
                            scrollToBottom();
                        } else if (data.tool_calls) {
                            // Example tool execution tracing
                            const toolsDiv = document.createElement('div');
                            toolsDiv.className = 'tool-call';
                            toolsDiv.innerHTML = `<i class="fas fa-cog fa-spin"></i> Executing: ${data.tool_calls.join(', ')}`;
                            contentElement.insertBefore(toolsDiv, textContainer);
                            scrollToBottom();
                        } else if (data.error) {
                            textContainer.innerHTML += `<br><br><span style="color:var(--danger)">Error: ${data.error}</span>`;
                            scrollToBottom();
                        }
                    } catch (e) {
                         console.warn("JSON parse error on streaming chunk", e);
                    }
                }
            }
        }
        
        // Failsafe in case stream ended without any data
        if (!firstDataReceived) {
            contentElement.innerHTML = `<p style="color: var(--text-secondary)"><em>Agent generated an empty response.</em></p>`;
        }
        
        // If markdown contains codeblocks for plans, maybe hook them up to the document overlay
        // Implementation for Document rendering could go here
    }

    function scrollToBottom() {
        chatHistory.scrollTo({
            top: chatHistory.scrollHeight,
            behavior: 'smooth'
        });
    }

    // Escape basic html tags
    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag])
        );
    }
    
    // Make test prompt helper available globally
    window.sendTestPrompt = function(text) {
        chatInput.value = text;
        const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
        chatForm.dispatchEvent(submitEvent);
    };
});
