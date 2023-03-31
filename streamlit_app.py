import streamlit.components.v1 as components
import json

def chatbot_component(bot_name, conversation, placeholder="Type a message"):
    component_func = components.declare_component(
        "chatbot",
        bot_name=bot_name,
        conversation=conversation,
        placeholder=placeholder,
        key=None,
    )
    return component_func

def chatbot_frontend(bot_name, conversation, placeholder):
    chat_html = f"""
        <div class="chat-container">
            <div class="chat-header">{bot_name}</div>
            <div class="chat-messages">
        """
    for message in conversation:
        if message[0] == "user":
            chat_html += f"""
                <div class="chat-message user">
                    <div class="chat-message-content">{message[1]}</div>
                </div>
            """
        elif message[0] == "bot":
            chat_html += f"""
                <div class="chat-message bot">
                    <div class="chat-message-content">{message[1]}</div>
                </div>
            """
    chat_html += """
            </div>
            <form id="chat-form">
                <input id="chat-input" type="text" placeholder="{placeholder}" autocomplete="off">
                <button type="submit" id="chat-submit">Send</button>
            </form>
        </div>
    """

    chat_js = f"""
        const componentId = "{components.get_id(allow_unsafe=True)}";
        const botName = "{bot_name}";
        const conversation = {json.dumps(conversation)};
        const placeholder = "{placeholder}";

        function renderConversation(conversation) {{
            const chatContainer = $(".chat-messages");
            chatContainer.html("");
            conversation.forEach((message) => {{
                const messageElement = $(
                    `<div class="chat-message ${message[0]}">
                        <div class="chat-message-content">${{message[1]}}</div>
                    </div>`
                );
                chatContainer.append(messageElement);
            }});
            chatContainer.scrollTop(chatContainer[0].scrollHeight);
        }}

        $(document).ready(() => {{
            renderConversation(conversation);
            $("#chat-form").on("submit", (event) => {{
                event.preventDefault();
                const userMessage = $("#chat-input").val();
                if (userMessage) {{
                    const messageElement = $(
                        `<div class="chat-message user">
                            <div class="chat-message-content">${{userMessage}}</div>
                        </div>`
                    );
                    $(".chat-messages").append(messageElement);
                    $.post(
                        `component/${componentId}/update`,
                        {{ userMessage: userMessage }},
                        (componentValue) => {{
                            renderConversation(componentValue.conversation);
                        }}
                    );
                    $("#chat-input").val("");
                }}
            }});
            $("#chat-input").on("keydown", (event) => {{
                if (event.keyCode === 13) {{
                    event.preventDefault();
                    $("#chat-submit").click();
                }}
            }});
            $("#chat-input").focus();
        }});
    """

    return chat_html, chat_js
