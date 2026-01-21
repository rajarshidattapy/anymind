from anymind import Agent

# Initialize agent with wallet address for authentication
agent = Agent(
    agent_id="custom-b06c4cf5",
    chat_id="d8b52085-73b8-4263-8b29-ef9f0c73c220",
    wallet_address="0x90df1528054FFccA5faE38EC6447f1557168620E",
    base_url="http://localhost:8000"
)

# Send a message to the agent
# The message is saved to chat history and memory is automatically updated
response = agent.chat("Hello, what is this chat about?")

print(response)