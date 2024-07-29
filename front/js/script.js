document.addEventListener('DOMContentLoaded', function() {
  console.log("DOM fully loaded and parsed");

  let ws;  // Declare WebSocket variable outside to manage single instance

  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
      event.preventDefault();
      console.log("Form submitted");

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      console.log("Email:", email);
      console.log("Password:", password);

      fetch('http://localhost:10000/service/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      })
      .then(response => {
        console.log("Response status:", response.status);
        return response.json();
      })
      .then(data => {
        console.log("Response data:", data);
        if (data.access_token && data.refresh_token) {
          console.log("Access token and refresh token found in response");

          // Append tokens to URL and redirect
          const queryParams = new URLSearchParams({
            access_token: data.access_token,
            refresh_token: data.refresh_token
          }).toString();

          console.log("Redirecting to create_chat.html with tokens in URL");
          window.location.href = `create_chat.html?${queryParams}`;
        } else {
          document.getElementById('message').textContent = 'Login failed: Tokens not found in response!';
          console.error('Tokens not found in response:', data);
        }
      })
      .catch(error => {
        document.getElementById('message').textContent = 'An error occurred!';
        console.error('Error:', error);
      });
    });
  }

  const createChatForm = document.getElementById('createChatForm');
  if (createChatForm) {
    createChatForm.addEventListener('submit', function(event) {
      event.preventDefault();

      const chat_name = document.getElementById('chat_name').value;
      const access_token = sessionStorage.getItem('access_token');
      console.log("Access Token from sessionStorage:", access_token);

      if (access_token) {
        fetch('http://localhost:10000/service/api/v1/chats', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access_token}`
          },
          body: JSON.stringify({ chat_name })
        })
        .then(response => response.json())
        .then(data => {
          console.log("Response data:", data);
          if (data.id && data.user_id) {
            sessionStorage.setItem('chat_id', data.id);
            sessionStorage.setItem('user_id', data.user_id);
            initializeWebSocket(data.id, data.user_id);  // Initialize WebSocket as soon as the chat is created
            window.location.href = `chat.html?chat_id=${data.id}`;  // Redirect to Chat page
          } else {
            document.getElementById('message').textContent = 'Failed to create chat!';
          }
        })
        .catch(error => {
          document.getElementById('message').textContent = 'An error occurred!';
          console.error('Error:', error);
        });
      } else {
        document.getElementById('message').textContent = 'Access token not found in sessionStorage!';
        console.error('Access token not found in sessionStorage');
      }
    });
  }

  function initializeWebSocket(chat_id, user_id) {
    const wsUrl = `ws://localhost:10000/service/api/v1/websockets/${chat_id}/${user_id}`;
    console.log("WebSocket URL:", wsUrl);
    
    // Only initialize WebSocket if it does not already exist
    if (!ws || ws.readyState === WebSocket.CLOSED) {
      ws = new WebSocket(wsUrl);

      ws.onopen = function() {
        console.log("WebSocket connection opened");
      };

      ws.onmessage = function(event) {
        console.log("WebSocket message received:", event.data);
        const chatWindow = document.getElementById('chatWindow');
        let messageData;

        try {
          messageData = JSON.parse(event.data);

          // Check if messageData.message is a JSON string and parse it if necessary
          if (typeof messageData.message === 'string') {
            try {
              messageData.message = JSON.parse(messageData.message);
            } catch (error) {
              console.warn("Failed to parse nested message data:", error);
            }
          }
        } catch (error) {
          console.error("Failed to parse message data:", error);
          return;
        }

        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message');

        if (messageData.user_id === 1) {
          messageElement.classList.add('ai-message');
        } else {
          messageElement.classList.add('user-message');
        }

        const userIcon = document.createElement('div');
        userIcon.classList.add('user-icon');

        if (messageData.user_id === 1) {
          userIcon.innerHTML = '<i class="fas fa-robot"></i>';
        } else {
          userIcon.innerHTML = '<i class="fas fa-user"></i>';
        }

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');

        const userIdSpan = document.createElement('span');
        userIdSpan.classList.add('user-id');
        userIdSpan.textContent = `User ${messageData.user_id}`;

        const roomIdSpan = document.createElement('span');
        roomIdSpan.classList.add('room-id');
        roomIdSpan.textContent = `(Room ${messageData.chat_id || messageData.id})`;

        const messageText = document.createElement('div');
        messageText.textContent = messageData.message.message || messageData.message;

        // messageContent.appendChild(userIdSpan);
        // messageContent.appendChild(roomIdSpan);
        messageContent.appendChild(messageText);

        messageElement.appendChild(userIcon);
        messageElement.appendChild(messageContent);

        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
      };

      ws.onerror = function(error) {
        console.error('WebSocket Error:', error);
      };

      ws.onclose = function(event) {
        console.log("WebSocket connection closed:", event);
      };
    }
  }

  const chatForm = document.getElementById('chatForm');
  if (chatForm) {
    chatForm.addEventListener('submit', function(event) {
      event.preventDefault();

      const message = document.getElementById('message').value;
      const chat_id = sessionStorage.getItem('chat_id');
      const user_id = sessionStorage.getItem('user_id');
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        initializeWebSocket(chat_id, user_id);
      }

      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ user_id, chat_id, message }));
      } else {
        ws.addEventListener('open', () => ws.send(JSON.stringify({ user_id, chat_id, message })));
      }

      document.getElementById('message').value = '';
    });
  }
});
