import streamlit as st
import pandas as pd
from vibeggeo.geoprocess import fetch_input_content, optimize_content

# 设置页面配置
st.set_page_config(page_title="VibeGEO - Generative Engine Optimizer", layout="wide")

def _render_metrics(result):
    """渲染 GEO 指标看板"""
    st.markdown("---")
    st.subheader("📊 GEO Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    # 使用 getattr 安全获取属性，确保不会因变量名报错
    with col1:
        st.metric("Info Density", f"{getattr(result, 'info_density', 0.0)}%")
    with col2:
        st.metric("Authority", f"{getattr(result, 'authority_score', 0.0)}%")
    with col3:
        st.metric("Alignment", f"{getattr(result, 'alignment_score', 0.0)}%")
    with col4:
        st.metric("Structure", f"{getattr(result, 'structure_score', 0.0)}%")

    # 展示透明度信号数据
    with st.expander("View Transparency & Signals"):
        st.json(getattr(result, 'transparency_data', {}))

def main():
    st.title("🚀 VibeGEO: Generative Engine Optimization")
    st.markdown("Optimize your content to be cited by Perplexity, SearchGPT, and Gemini.")

    # 1. 侧边栏配置
    with st.sidebar:
        st.header("Settings")
        provider = st.selectbox("AI Provider", ["Google Gemini", "OpenAI"])
        gemini_api_key = st.text_input("Gemini API Key", type="password")
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        
        st.markdown("---")
        st.info("GEO Tip: AI Engines favor content with high information density and expert citations.")

    # 2. 输入区域
    input_mode = st.radio("Input Mode", ["URL", "Text"])
    
    source_url = ""
    input_text = ""
    
    if input_mode == "URL":
        source_url = st.text_input("Enter URL", placeholder="https://example.com/product")
    else:
        input_text = st.text_area("Paste Content", height=200, placeholder="Paste your article here...")

    target_keyword = st.text_input("Target Keyword (English)", placeholder="e.g., glow, sustainable, organic")

    # 3. 执行按钮
    if st.button("Start GEO Optimization", type="primary"):
        if not target_keyword:
            st.error("Please enter a target keyword.")
            return

        with st.spinner("VibeGEO is analyzing and optimizing..."):
            try:
                # 获取内容 (fetch_input_content 现在返回 5 个值)
                content_text, final_url, screenshot, image_tags, audio = fetch_input_content(
                    url=source_url if input_mode == "URL" else None,
                    text=input_text if input_mode == "Text" else None
                )

                if not content_text and not screenshot:
                    st.error("Could not fetch content. Please try 'Text' mode.")
                    return

                # 执行优化 (使用 **kwargs 传递所有参数)
                result = optimize_content(
                    text=content_text,
                    keyword=target_keyword,
                    provider=provider,
                    gemini_api_key=gemini_api_key,
                    openai_api_key=openai_api_key,
                    visual_screenshot_base64=screenshot
                )

                # 4. 展示结果
                st.success("Optimization Completed!")
                
                # 指标展示
                _render_metrics(result)

                # 内容展示
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.subheader("Original Content")
                    # 使用 schemas.py 中定义的 original_content
                    st.text_area("Original", value=result.original_content, height=400, disabled=True)

                with col_right:
                    st.subheader("GEO-Optimized Content")
                    st.markdown(result.optimized_text)
                    st.download_button("Download Optimized Markdown", result.optimized_text, file_name="optimized.md")

                # 展示优化建议
                if result.suggestions:
                    st.markdown("---")
                    st.subheader("💡 Actionable Insights")
                    for s in result.suggestions:
                        st.info(s)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.exception(e) # 打印完整错误堆栈方便调试

if __name__ == "__main__":
    main()