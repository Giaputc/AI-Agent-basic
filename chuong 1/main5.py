import ollama
import json
from pathlib import Path

FILE_PATH = "/home/phamvangiap/Projects/AI_aigen/chuong 1/skills/test/SKILL.md"

# 1. Đọc file
content = Path(FILE_PATH).read_text(encoding="utf-8")
print(f"✅ Đã đọc file: {FILE_PATH}")
print(f"📏 Số ký tự: {len(content)}")
print("-" * 50)

# 2. Prompt rõ ràng, chỉ yêu cầu JSON
prompt = f"""Đọc skill sau:

{content}

Trả về DUY NHẤT một JSON theo schema:
{{
  "skill_name": "<tên skill>",
  "description": "<mô tả>",
  "commands": ["<lệnh 1>", "<lệnh 2>"],
  "output_prefix": "<chuỗi in trước output>"
}}

CHỈ TRẢ VỀ JSON, KHÔNG GIẢI THÍCH, KHÔNG DÙNG MARKDOWN."""

# 3. ⚡ QUAN TRỌNG: format="json"
response = ollama.chat(
    model="qwen2.5-coder:latest",
    messages=[{"role": "user", "content": prompt}],
    format="json",              # 👈 BẮT BUỘC PHẢI CÓ
    options={"temperature": 0}  # 0 để ổn định
)

# 4. In raw + parse
raw = response["message"]["content"]
print("🤖 Raw từ Qwen:")
print(raw)
print("-" * 50)

result = json.loads(raw)
print("✅ JSON đã parse:")
print(json.dumps(result, indent=2, ensure_ascii=False))