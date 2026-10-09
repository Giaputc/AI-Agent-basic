from ollama import chat

response = chat(
    model="qwen2.5-coder:latest",
    messages=[
        {
            "role": "system",
            "content": (
                "Bạn là trợ lý lập trình, trả lời ngắn gọn. "
                "Người dùng tên là Giáp, hãy xưng hô phù hợp."
            ),
        },
        {"role": "user", "content": "Tôi tên là gì?"},
    ],
)

print(response["message"]["content"])