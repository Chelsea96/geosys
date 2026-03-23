from .content_fetcher import fetch_content_from_url
from .text_analyzer import analyze_text
from .optimizer import generate_optimization, vision_to_text
from .schemas import GeoOptimizationResult
import streamlit as st

def fetch_input_content(url=None, text=None):
    content = text if text else ""
    screenshot = None
    if url and not text:
        content, screenshot = fetch_content_from_url(url)
    return content, url or "", screenshot, [], None

def optimize_content(text, keyword, **kwargs):
    provider = kwargs.get('provider', 'Google Gemini')
    api_key = kwargs.get('gemini_api_key') or kwargs.get('openai_api_key')
    
    # 1. 运行优化
    opt_data = generate_optimization(text, keyword, provider, api_key)
    
    # 2. 💡 修复评分逻辑：如果 API 报错，我们分析【原始文本】；如果成功，分析【优化后文本】
    target_text_for_analysis = text if "🚨 API ERROR" in opt_data.get("optimized_text", "") else opt_data.get("optimized_text", "")
    analysis = analyze_text(target_text_for_analysis, keyword)
    
    # 3. 封装结果
    return GeoOptimizationResult(
        original_content=text, 
        optimized_text=opt_data.get("optimized_text", text),
        suggestions=opt_data.get("suggestions", []),
        info_density=float(opt_data.get("info_density") or (len(analysis['geo_signals']) * 20 + 10)),
        authority_score=float(opt_data.get("authority_score") or 50.0),
        alignment_score=float(opt_data.get("alignment_score") or (analysis['density'] * 10 + 20)),
        structure_score=float(opt_data.get("structure_score") or 60.0),
        transparency_data={
            "keyword_count": analysis['count'],
            "signals": analysis['geo_signals'],
            "is_in_first_para": analysis['is_in_first']
        }
    )