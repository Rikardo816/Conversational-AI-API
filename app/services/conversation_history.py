# from langchain_community.chat_message_histories import RedisChatMessageHistory

# def get_message_history(session_id: str) -> RedisChatMessageHistory:
#     return RedisChatMessageHistory(session_id=session_id, url="redis://redis:6379/0")

# def save_message(session_id: str, message: str):
#     history = get_message_history(session_id)
#     history.add_message(content=message)

# def get_messages(session_id: str):
#     history = get_message_history(session_id)
#     return history.load_messages()

