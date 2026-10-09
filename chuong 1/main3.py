# extract_info.py
from ollama import chat
from pydantic import BaseModel, Field
from typing import List, Optional

class Person(BaseModel):
    name: str = Field(description="Tên người")
    age: int = Field(ge=0, le=150, description="Tuổi")
    city: str = Field(description="Thành phố")
    skills: List[str] = Field(default_factory=list, description="Kỹ năng")
    email: Optional[str] = Field(None, description="Email nếu có")

def extract_person(text: str) -> Person:
    schema = Person.model_json_schema()

    resp = chat(
        model="qwen2.5-coder:latest",
        messages=[{
            "role": "user",
            "content": f"Trích xuất thông tin từ câu sau:\n\n{text}"
        }],
        format=schema,
        options={"temperature": 0},
    )

    return Person.model_validate_json(resp["message"]["content"])


if __name__ == "__main__":
    text = "tên tôi là Anh phạm văn Giáp, 25 tuổi, sống ở Hà Nội,có skill Python dev,email giap123@gmail.com"
    person = extract_person(text)
    print(person)
    # → Person(name='Giáp', age=25, city='Hà Nội', skills=['Python'], email='giap@example.com')

    print(f"\nTên: {person.name}")
    print(f"Tuổi: {person.age}")
    print(f"Skills: {', '.join(person.skills)}")
    print(f"Tuổi: {person.email}")