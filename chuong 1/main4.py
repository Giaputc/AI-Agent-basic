import ollama
from pathlib import Path

FILE_PATH = "/home/phamvangiap/Projects/AI_aigen/chuong 1/skills/test/SKILL.md"

# 1. Đọc file
content = Path(FILE_PATH).read_text(encoding="utf-8")
print(f"✅ Đã đọc file: {FILE_PATH}")
print(f"📏 Số ký tự: {len(content)}")
print("-" * 50)

# 2. Gửi cho Qwen
response = ollama.chat(
    model="qwen2.5-coder:latest",
    messages=[
        {
            "role": "user",
            "content": (
                "Đọc skill sau và thực hiện:\n\n"
                f"{content}"
            )
        }
    ]
)

# 3. In kết quả
print("🤖 Qwen trả lời:")
print(response["message"]["content"])