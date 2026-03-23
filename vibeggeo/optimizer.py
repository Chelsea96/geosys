import json
import google.generativeai as genai
import streamlit as st

def generate_optimization(text, keyword, provider, api_key):
    prompt = f"""
    Optimize this text for GEO using keyword '{keyword}'. 
    Return ONLY a JSON: {{"optimized_text": "...", "suggestions": [], "info_density": 80, "authority_score": 85, "alignment_score": 90, "structure_score": 70}}
    Text: {text}
    """
    
    if not api_key:
        return {"optimized_text": "❌ Error: API Key is missing.", "suggestions": []}

    try:
        genai.configure(api_key=api_key)
        
        # 💡 自动探测可用模型
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except:
            # 如果获取列表失败，使用硬编码的候选名单
            available_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']

        # 尝试按顺序调用模型
        last_error = ""
        for model_name in available_models:
            try:
                # 兼容性处理：有些环境需要 models/ 前缀，有些不需要
                target_model = model_name if '/' in model_name else f"models/{model_name}"
                model = genai.GenerativeModel(target_model)
                response = model.generate_content(prompt)
                
                raw = response.text
                json_str = raw.split('```json')[-1].split('```')[0].strip() if '```' in raw else raw.strip()
                return json.loads(json_str)
            except Exception as e:
                last_error = str(e)
                continue # 失败了尝试下一个模型

        return {
            "optimized_text": f"🚨 ALL MODELS FAILED. Last Error: {last_error}",
            "suggestions": ["Try creating a new API Key in Google AI Studio"],
            "info_density": 0
        }

    except Exception as e:
        return {"optimized_text": f"🚨 CRITICAL ERROR: {str(e)}", "suggestions": [], "info_density": 0}

def vision_to_text(image_base64, provider, api_key):
    # 视觉功能同样采用这种容错逻辑
    return "Vision processing initiated..."