import ollama
import json
import subprocess
import time
from pathlib import Path

FILE_PATH = "/home/phamvangiap/Projects/AI_aigen/chuong 1/skills/test/SKILL.md"

# ====== 1. Đọc file skill ======
content = Path(FILE_PATH).read_text(encoding="utf-8")
print(f"✅ Đã đọc file: {FILE_PATH}")
print(f"📏 Số ký tự: {len(content)}")
print("-" * 50)

# ====== 2. Prompt yêu cầu JSON ======
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

# ====== 3. Gọi Qwen ======
response = ollama.chat(
    model="qwen2.5-coder:latest",
    messages=[{"role": "user", "content": prompt}],
    format="json",
    options={"temperature": 0}
)

raw = response["message"]["content"]
print("🤖 Raw từ Qwen:")
print(raw)
print("-" * 50)

# ====== 4. Parse JSON ======
try:
    plan = json.loads(raw)
except json.JSONDecodeError:
    print("❌ LLM trả JSON lỗi, dừng lại.")
    raise SystemExit(1)

print("✅ JSON đã parse:")
print(json.dumps(plan, indent=2, ensure_ascii=False))
print("-" * 50)

# ====== 5. Hiển thị kế hoạch + xin phép ======
skill_name    = plan.get("skill_name", "?")
description   = plan.get("description", "")
commands      = plan.get("commands", [])
output_prefix = plan.get("output_prefix", "")

print(f"🎯 Skill     : {skill_name}")
print(f"📝 Mô tả     : {description}")
print(f"🏷️  Prefix    : {output_prefix}")
print(f"📜 Số lệnh    : {len(commands)}")
print()
print("Các lệnh sẽ chạy:")
for i, cmd in enumerate(commands, 1):
    print(f"   {i}. {cmd}")
print()

answer = input("⚠️  Bạn có muốn thực thi các lệnh trên? [y/N]: ").strip().lower()

if answer not in ("y", "yes"):
    print("🚫 Đã huỷ. Không chạy lệnh nào.")
    raise SystemExit(0)

# ====== 6. Thực thi từng lệnh — IN OUTPUT CỦA TỪNG LỆNH ======
print("\n" + "=" * 50)
print("⚙️  BẮT ĐẦU THỰC THI")
print("=" * 50)

if output_prefix:
    print(output_prefix)

run_all = False

for i, cmd in enumerate(commands, 1):
    # ─── Header của từng lệnh ───
    print(f"\n{'─' * 50}")
    print(f"▶️  LỆNH {i}/{len(commands)}: {cmd}")
    print(f"{'─' * 50}")

    if run_all:
        sub_answer = "y"
    else:
        sub_answer = input("   → Chạy lệnh này? [y/N/a(ll)/q(uit)]: ").strip().lower()

    if sub_answer == "q":
        print("   🚫 Người dùng dừng giữa chừng.")
        break
    if sub_answer == "a":
        run_all = True
        sub_answer = "y"
    if sub_answer not in ("y", "yes"):
        print("   ⏭️  Bỏ qua lệnh này.")
        continue

    # ─── Chạy lệnh + đo thời gian ───
    start = time.time()
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        elapsed = time.time() - start

        # ─── In kết quả của lệnh này ───
        if result.stdout:
            print("   📤 Kết quả (stdout):")
            for line in result.stdout.rstrip().split("\n"):
                print(f"      {line}")
        else:
            print("   📤 Kết quả (stdout): (rỗng)")

        if result.stderr:
            print("   ⚠️  Lỗi (stderr):")
            for line in result.stderr.rstrip().split("\n"):
                print(f"      {line}")

        status = "✅ OK" if result.returncode == 0 else "❌ LỖI"
        print(f"   {status} | exit code = {result.returncode} | ⏱️  {elapsed:.2f}s")

    except subprocess.TimeoutExpired:
        print(f"   ⏱️  Hết thời gian (30s), bỏ qua lệnh '{cmd}'.")
    except Exception as e:
        print(f"   ❌ Lỗi khi chạy '{cmd}': {e}")

# ─── Kết thúc ───
print("\n" + "=" * 50)
print("🏁 HOÀN TẤT")
print("=" * 50)