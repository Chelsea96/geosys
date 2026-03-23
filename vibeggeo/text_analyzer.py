import re

def analyze_text(text: str, keyword: str):
    if not text or not keyword:
        return {"count": 0, "density": 0.0, "is_in_first": False, "geo_signals": []}
    
    # 统一转小写，使用正则匹配完整单词
    text_lower = text.lower()
    kw_lower = keyword.lower()
    matches = re.findall(rf'\b{re.escape(kw_lower)}\b', text_lower)
    count = len(matches)
    
    words = text.split()
    word_count = len(words)
    density = (count / word_count * 100) if word_count > 0 else 0.0
    
    paragraphs = [p for p in text.split('\n') if p.strip()]
    is_in_first = kw_lower in paragraphs[0].lower() if paragraphs else False
    
    geo_signals = []
    if re.search(r'\d+%', text_lower): geo_signals.append("statistics")
    if re.search(r'\b(data|research|expert|source)\b', text_lower): geo_signals.append("authority")
    
    return {
        "count": count,
        "density": density,
        "is_in_first": is_in_first,
        "geo_signals": geo_signals
    }