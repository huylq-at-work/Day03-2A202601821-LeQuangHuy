"""
🔌 MULTI-PROVIDER LLM ADAPTER (OpenAI, Gemini, Anthropic, OpenRouter & Offline Mock)
Hỗ trợ chuyển đổi linh hoạt giữa các nhà cung cấp AI chỉ bằng cách đổi biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho tất cả các LLM Provider"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-2.5-flash"
        
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env!"
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(
                model=self.model_name,
                contents=contents
            )
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (GPT-4o, GPT-3.5-turbo, etc.)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"
        
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env!"
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude Provider (Claude 3.5 Sonnet, Claude 3 Haiku)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "claude-3-haiku-20240307"
        
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_anthropic_api_key_here":
            return "[Anthropic Error]: Chưa cấu hình ANTHROPIC_API_KEY trong file .env!"
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            kwargs = {
                "model": self.model_name,
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            }
            if system_prompt:
                kwargs["system"] = system_prompt
                
            response = client.messages.create(**kwargs)
            return response.content[0].text
        except Exception as e:
            return f"[Anthropic Exception]: {str(e)}"


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter Provider (Hỗ trợ gọi mọi model qua OpenRouter API)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "google/gemini-2.5-flash"
        
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            return "[OpenRouter Error]: Chưa cấu hình OPENROUTER_API_KEY trong file .env!"
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model_name,
                "messages": messages
            }
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
            if res.status_code == 200:
                data = res.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"[OpenRouter API Error {res.status_code}]: {res.text}"
        except Exception as e:
            return f"[OpenRouter Exception]: {str(e)}"


class MockProvider(BaseLLMProvider):
    """
    Offline Mock Provider — chạy demo không cần API key.

    KHÔNG phải LLM thật: đây là máy trạng thái mô phỏng đúng giao thức ReAct,
    quyết định bước kế tiếp dựa trên số Observation đã có trong history.
    Đủ để demo vòng lặp và giao diện khi chưa có key, nhưng bài nộp nên
    chạy bằng provider thật (gemini/openai/anthropic) mới đúng tinh thần.
    """

    model_name = "Offline Mock (mô phỏng ReAct)"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        import re as _re

        # Chatbot baseline: không có tool, trả lời chung chung như LLM không tra cứu được
        if "Thought:" not in (system_prompt or ""):
            return ("Mình chưa tra cứu được hồ sơ hay danh mục khóa học thực tế nên chỉ "
                    "tư vấn chung được thôi. Bạn nên cân nhắc ngân sách, lịch rảnh và "
                    "trình độ hiện tại trước khi chọn khóa nhé.")

        quan_sat = _re.findall(r"Observation:\s*(.+)", prompt)
        sdt = _re.search(r"\b0\d{9}\b", prompt)
        sdt = sdt.group(0) if sdt else None

        # Gặp lỗi thì dừng, không đoán bừa — đúng quy tắc trong prompt
        if quan_sat and quan_sat[-1].strip().upper().startswith("LỖI"):
            return ("Thought: Công cụ báo lỗi, mình không được bịa dữ liệu.\n"
                    "Final Answer: Xin lỗi bạn, mình không tìm thấy thông tin này trong "
                    "hệ thống. Bạn kiểm tra lại số điện thoại hoặc tên khóa học giúp mình nhé.")

        if not sdt:
            return ("Thought: Câu hỏi không có số điện thoại nên mình không tra hồ sơ được.\n"
                    "Final Answer: Bạn cho mình xin số điện thoại đã đăng ký để mình tra "
                    "hồ sơ và gợi ý khóa phù hợp nhé.")

        if len(quan_sat) == 0:
            return (f"Thought: Mình cần xem hồ sơ học viên trước để biết ngân sách và trình độ.\n"
                    f"Action: get_learner[{sdt}]")

        if len(quan_sat) == 1:
            hs = quan_sat[0]
            mt = _re.search(r"mục tiêu:\s*([^;]+)", hs)
            ns = _re.search(r"ngân sách:\s*([\d.,]+)", hs)
            chu_de = mt.group(1).split(",")[0].strip() if mt else "AI"
            gia = ns.group(1).replace(",", "").replace(".", "") if ns else "5000000"
            return (f"Thought: Học viên quan tâm {chu_de}, ngân sách {gia}đ. "
                    f"Mình tìm khóa phù hợp trong tầm giá này.\n"
                    f"Action: search_courses[{chu_de}, {gia}]")

        if len(quan_sat) == 2:
            ma = _re.search(r"\b([A-Z]{2,3}\d{3})\b", quan_sat[1])
            if not ma:
                return ("Thought: Không có khóa nào khớp điều kiện.\n"
                        "Final Answer: Hiện chưa có khóa nào vừa đúng chủ đề vừa nằm trong "
                        "ngân sách của bạn. Bạn cân nhắc nới ngân sách hoặc đổi chủ đề nhé.")
            return (f"Thought: Có khóa {ma.group(1)}. Mình kiểm tra xem học viên đăng ký được không.\n"
                    f"Action: check_suitability[{sdt}, {ma.group(1)}]")

        return ("Thought: Mình đã có đủ thông tin để trả lời.\n"
                f"Final Answer: {quan_sat[-1]} Dựa trên hồ sơ của bạn, đây là khóa mình "
                "gợi ý. Bạn xem thêm chi tiết lịch học và học phí rồi đăng ký nhé.")


def get_llm_provider(provider_name: str = None) -> BaseLLMProvider:
    """Factory function tự chọn Provider từ biến môi trường LLM_PROVIDER"""
    name = (provider_name or os.getenv("LLM_PROVIDER") or "mock").lower().strip()
    
    if name == "gemini":
        return GeminiProvider()
    elif name == "openai":
        return OpenAIProvider()
    elif name == "anthropic":
        return AnthropicProvider()
    elif name == "openrouter":
        return OpenRouterProvider()
    else:
        return MockProvider()


if __name__ == "__main__":
    print("=== TEST MULTI-PROVIDER LLM ADAPTER ===")
    provider = get_llm_provider()
    print(f"✅ Provider đang dùng: {provider.__class__.__name__}")
    print(f"🤖 User Query: Hello")
    print(f"💬 Response  : {provider.generate('Hello')}")
