# test_quen.py
from ollama import chat

def run(num_ctx, filler_words=10):
    secret = "MAU_XANH_12345"
    filler = "không"* filler_words

    # Chôn secret ở GIỮA
    prompt = f"{filler}\nMã bí mật là: {secret}\n{filler}\n\nMã bí mật là gì?"

    opts = {"num_ctx": num_ctx} if num_ctx else {}
    resp = chat(
        model="qwen2.5-coder:latest",
        messages=[{"role": "user", "content": prompt}],
        options=opts,
    )
    ans = resp["message"]["content"]
    ok = secret in ans

    print(f"num_ctx={str(num_ctx):>7} | "
          f"prompt={resp['prompt_eval_count']:>5} tok | "
          f"{'✅ NHỚ' if ok else '❌ QUÊN'} | → {ans[:60]!r}")


print("=== Chôn secret ở GIỮA, test num_ctx ===\n")

run(4096)


