import json
import google.generativeai as genai

def generate_optimization(text, keyword, provider, api_key):
    prompt = f"Optimize for GEO using keyword '{keyword}': {text}. Return ONLY JSON: {{'optimized_text': '...', 'suggestions': [], 'info_density': 80}}"
    
    try:
        if provider == "Google Gemini" and api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(prompt)
            raw = response.text
            json_str = raw.split('```json')[-1].split('```')[0].strip() if '```' in raw else raw.strip()
            return json.loads(json_str)
    except Exception as e:
        return {"optimized_text": f"🚨 API ERROR: {str(e)}", "suggestions": []}
    return {"optimized_text": text, "suggestions": ["API error"]}

def vision_to_text(image_base64, provider, api_key):
    """
    视觉分析函数
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        img_data = [{"mime_type": "image/png", "data": image_base64}]
        response = model.generate_content(["Describe this product for GEO optimization", img_data[0]])
        return response.text
    except:
        return "Vision analysis currently unavailable."
