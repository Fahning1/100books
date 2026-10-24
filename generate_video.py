#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
100天100本书 · 每日视频生成脚本
功能：根据当天书名和核心内容，生成 HyperFrames 动画视频组合文件
用法：python3 generate_video.py [day_number]

视频结构（约105秒）：
  1. 开场（10秒） - 书名 + 分类 + 天数
  2. 核心知识点动画（50秒） - 5个核心概念的动画展示
  3. 经典案例（30秒） - 1个深度案例的核心启示
  4. 总结（15秒） - 金句 + 行动号召
"""

import os
import sys
import re
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from books_data import BOOKS, get_book_by_day, get_category_themes

VIDEO_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "videos")
HF_COMPOSITION_DIR = os.path.join(SCRIPT_DIR, "hf_compositions")
LOG_FILE = os.path.join(SCRIPT_DIR, "logs", "generate_video.log")
TARGET_DURATION = 105


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = "[%s] %s\n" % (timestamp, msg)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass
    print(log_line.strip())


def sanitize_filename(title):
    title = re.sub(r'[\\/:*?"<>|（）()《》【】·.，,！!？?]', '', title)
    return title[:30]


# HyperFrames 组合文件 HTML 模板
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN" data-fps="30">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第__DAY__天 · __TITLE__</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1280px; height: 720px; overflow: hidden;
  font-family: "Noto Sans SC", -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: #0a0a1a; color: #f1f5f9;
}
.composition { position: relative; width: 100%; height: 100%; }
.scene {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none;
}
.scene.active { opacity: 1; pointer-events: auto; }
.bg-gradient {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background: 
    radial-gradient(ellipse at 30% 30%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 70%, rgba(6, 182, 212, 0.12) 0%, transparent 50%);
}

/* 开场 */
.intro-scene .intro-content { text-align: center; position: relative; z-index: 1; }
.intro-icon { font-size: 56px; display: block; margin-bottom: 16px; }
.intro-day { font-size: 18px; color: #06b6d4; letter-spacing: 4px; margin-bottom: 20px; font-weight: 500; }
.intro-title {
  font-size: 64px; font-weight: 800;
  background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin-bottom: 14px; letter-spacing: 2px;
}
.intro-author { font-size: 22px; color: #94a3b8; margin-bottom: 22px; }
.intro-category {
  display: inline-block; padding: 10px 28px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%);
  border: 1px solid rgba(139, 92, 246, 0.4);
  border-radius: 100px; font-size: 16px; color: #06b6d4; font-weight: 500;
}

/* 概念场景 */
.concept-container { text-align: center; position: relative; z-index: 1; max-width: 850px; padding: 0 60px; }
.concept-number {
  font-size: 100px; font-weight: 800;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(6, 182, 212, 0.15) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  line-height: 1; position: absolute; top: -50px; left: 50%; transform: translateX(-50%); z-index: 0;
}
.concept-title { font-size: 42px; font-weight: 700; margin-bottom: 10px; position: relative; z-index: 1; }
.concept-subtitle { font-size: 18px; color: #94a3b8; margin-bottom: 28px; position: relative; z-index: 1; }
.concept-takeaway {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 14px 28px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(6, 182, 212, 0.08) 100%);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 14px; font-size: 17px; line-height: 1.6; max-width: 650px;
  position: relative; z-index: 1;
}
.tk-icon { font-size: 20px; }
.tk-text { color: #e2e8f0; font-weight: 500; }

/* 浮动装饰 */
.floating-shapes { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
.shape { position: absolute; border-radius: 50%; filter: blur(60px); opacity: 0.35; }
.shape.s1 { width: 180px; height: 180px; background: #8b5cf6; top: 12%; left: 12%; }
.shape.s2 { width: 140px; height: 140px; background: #06b6d4; bottom: 22%; right: 16%; }

/* 案例场景 */
.case-scene .case-content { max-width: 850px; padding: 0 60px; position: relative; z-index: 1; }
.case-label { font-size: 14px; color: #06b6d4; letter-spacing: 3px; margin-bottom: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.case-label-icon { font-size: 22px; }
.case-title { font-size: 32px; font-weight: 700; margin-bottom: 22px; line-height: 1.3; }
.case-tk-box {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.06) 100%);
  border-left: 4px solid #8b5cf6;
  border-radius: 0 12px 12px 0;
  padding: 22px 26px; margin-top: 18px;
}
.case-tk-label { font-size: 12px; font-weight: 700; color: #8b5cf6; letter-spacing: 2px; margin-bottom: 6px; }
.case-tk-text { font-size: 17px; line-height: 1.8; color: #e2e8f0; }

/* 结尾场景 */
.outro-scene .outro-content { text-align: center; position: relative; z-index: 1; max-width: 750px; padding: 0 60px; }
.outro-quote {
  font-size: 28px; line-height: 1.6; font-weight: 500;
  margin-bottom: 28px; color: #f1f5f9; font-style: italic;
}
.outro-cta { font-size: 20px; color: #94a3b8; margin-bottom: 14px; }
.outro-brand {
  font-size: 18px; font-weight: 700;
  background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin-top: 20px;
}
.outro-progress { font-size: 15px; color: #64748b; margin-top: 6px; }

/* 进度条 */
.progress-bar {
  position: absolute; bottom: 0; left: 0;
  height: 3px;
  background: linear-gradient(90deg, #8b5cf6, #06b6d4);
  width: 0%; z-index: 100;
}
</style>
</head>
<body>

<div class="composition" data-composition-id="book-__DAY__" data-duration="__DURATION__">

<div class="bg-gradient"></div>
<div class="progress-bar" id="progressBar"></div>

<!-- 开场场景 -->
<div class="scene intro-scene active" data-start="0" data-duration="__T_INTRO__">
  <div class="intro-content">
    <span class="intro-icon">__ICON__</span>
    <div class="intro-day">第 __DAY__ 天 · 100天100本书</div>
    <h1 class="intro-title">__TITLE__</h1>
    <div class="intro-author">— __AUTHOR__ —</div>
    <div class="intro-category">__CATEGORY__</div>
  </div>
  <div class="floating-shapes">
    <div class="shape s1"></div>
    <div class="shape s2"></div>
  </div>
</div>

__CONCEPT_SCENES__

<!-- 案例场景 -->
<div class="scene case-scene" data-start="__CASE_START__" data-duration="__T_CASE__">
  <div class="case-content">
    <div class="case-label">
      <span class="case-label-icon">📊</span>
      经典案例分析
    </div>
    <h2 class="case-title">__CASE_TITLE__</h2>
    <div class="case-tk-box">
      <div class="case-tk-label">核心启示</div>
      <div class="case-tk-text">__CASE_TAKEAWAY__</div>
    </div>
  </div>
  <div class="floating-shapes">
    <div class="shape s1"></div>
    <div class="shape s2"></div>
  </div>
</div>

<!-- 结尾场景 -->
<div class="scene outro-scene" data-start="__OUTRO_START__" data-duration="__T_OUTRO__">
  <div class="outro-content">
    <div class="outro-quote">__QUOTE__</div>
    <div class="outro-cta">每天一小时，构建完整商业知识体系</div>
    <div class="outro-brand">📚 100天100本书 · AI递归学习计划</div>
    <div class="outro-progress">第 __DAY__ / 100 天</div>
  </div>
  <div class="floating-shapes">
    <div class="shape s1"></div>
    <div class="shape s2"></div>
  </div>
</div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script>
  const tl = gsap.timeline();
  const totalDuration = __TOTAL__;
  
  // 开场动画
  tl.from('.intro-scene .intro-icon', { scale: 0, opacity: 0, duration: 0.5, ease: "back.out(1.7)" }, 0)
    .from('.intro-scene .intro-day', { y: 20, opacity: 0, duration: 0.4 }, 0.2)
    .from('.intro-scene .intro-title', { y: 30, opacity: 0, duration: 0.6, ease: "power2.out" }, 0.4)
    .from('.intro-scene .intro-author', { y: 20, opacity: 0, duration: 0.4 }, 0.8)
    .from('.intro-scene .intro-category', { y: 20, opacity: 0, duration: 0.4 }, 1.0);
  
  __CONCEPT_JS__
  
  // 案例入场
  tl.from('.case-scene .case-label', { x: -30, opacity: 0, duration: 0.5 }, __CASE_START__)
    .from('.case-scene .case-title', { y: 30, opacity: 0, duration: 0.6, ease: "power2.out" }, __CASE_START__+0.2)
    .from('.case-scene .case-tk-box', { x: 30, opacity: 0, duration: 0.5 }, __CASE_START__+0.5);
  
  // 结尾入场
  tl.from('.outro-scene .outro-quote', { y: 30, opacity: 0, duration: 0.6, ease: "power2.out" }, __OUTRO_START__)
    .from('.outro-scene .outro-cta', { y: 20, opacity: 0, duration: 0.5 }, __OUTRO_START__+0.3)
    .from('.outro-scene .outro-brand', { y: 20, opacity: 0, duration: 0.5 }, __OUTRO_START__+0.5)
    .from('.outro-scene .outro-progress', { y: 10, opacity: 0, duration: 0.4 }, __OUTRO_START__+0.7);
</script>

</body>
</html>"""


def generate_composition_html(day, book, content):
    """生成 HyperFrames 组合 HTML 文件"""
    
    themes = get_category_themes(book["category"])
    insights = content["insights"][:5]
    cases = content.get("cases", [])
    quotes = content.get("quotes", [])
    
    case_title = cases[0]["title"] if cases else "经典案例分析"
    case_takeaway = cases[0]["takeaway"] if cases else (book["summary"][:80] + "...")
    quote_text = quotes[0]["text"] if quotes else (book["summary"][:60] + "...")
    
    # 截断长文本
    if len(case_takeaway) > 85:
        case_takeaway = case_takeaway[:85] + "..."
    if len(quote_text) > 70:
        quote_text = quote_text[:70] + "..."
    
    # 各段时长
    T_INTRO = 10
    T_CONCEPT = 50
    T_CASE = 30
    T_OUTRO = 15
    TOTAL = T_INTRO + T_CONCEPT + T_CASE + T_OUTRO
    PER_CONCEPT = T_CONCEPT // len(insights)
    
    # 构建概念场景HTML和JS
    concept_scenes_html = ""
    concept_js = ""
    
    for i, ins in enumerate(insights):
        idx = i + 1
        start_t = T_INTRO + i * PER_CONCEPT
        takeaway = ins.get("takeaway", "")[:65]
        if len(ins.get("takeaway", "")) > 65:
            takeaway = takeaway + "..."
        subtitle = ins.get("subtitle", "")
        
        concept_scenes_html += """
<div class="scene concept-scene scene-%d" data-start="%d" data-duration="%d">
  <div class="concept-container">
    <div class="concept-number">0%d</div>
    <h2 class="concept-title">%s</h2>
    <p class="concept-subtitle">%s</p>
    <div class="concept-takeaway">
      <span class="tk-icon">💡</span>
      <span class="tk-text">%s</span>
    </div>
  </div>
  <div class="floating-shapes">
    <div class="shape s1"></div>
    <div class="shape s2"></div>
  </div>
</div>""" % (idx, start_t, PER_CONCEPT, idx, ins["title"], subtitle, takeaway)
        
        concept_js += """
  tl.from('.scene-%d .concept-number', { scale: 0, opacity: 0, duration: 0.6, ease: "back.out(1.7)" }, %d)
    .from('.scene-%d .concept-title', { y: 30, opacity: 0, duration: 0.5, ease: "power2.out" }, %d+0.2)
    .from('.scene-%d .concept-subtitle', { y: 20, opacity: 0, duration: 0.4 }, %d+0.4)
    .from('.scene-%d .concept-takeaway', { y: 20, opacity: 0, duration: 0.5 }, %d+0.6);
""" % (idx, start_t, idx, start_t, idx, start_t, idx, start_t)
    
    case_start = T_INTRO + T_CONCEPT
    outro_start = case_start + T_CASE
    
    # 替换模板占位符
    html = HTML_TEMPLATE
    replacements = [
        ("__DAY__", str(day)),
        ("__TITLE__", book["short_title"]),
        ("__ICON__", book["icon"]),
        ("__AUTHOR__", book["author"] or "佚名"),
        ("__CATEGORY__", book["category"]),
        ("__DURATION__", str(TOTAL)),
        ("__T_INTRO__", str(T_INTRO)),
        ("__T_CASE__", str(T_CASE)),
        ("__T_OUTRO__", str(T_OUTRO)),
        ("__TOTAL__", str(TOTAL)),
        ("__CASE_START__", str(case_start)),
        ("__OUTRO_START__", str(outro_start)),
        ("__CONCEPT_SCENES__", concept_scenes_html),
        ("__CONCEPT_JS__", concept_js),
        ("__CASE_TITLE__", case_title),
        ("__CASE_TAKEAWAY__", case_takeaway),
        ("__QUOTE__", quote_text),
    ]
    
    for key, value in replacements:
        html = html.replace(key, value)
    
    return html, TOTAL


def render_video(comp_path, output_path):
    """尝试使用 HyperFrames CLI 渲染视频"""
    
    candidates = [
        "npx hyperframes",
        "hyperframes",
        os.path.expanduser("~/.npm-global/bin/hyperframes"),
    ]
    
    for cmd in candidates:
        try:
            result = subprocess.run(
                cmd + " --version",
                shell=True, capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                log("找到 HyperFrames CLI: %s" % cmd)
                render_cmd = "%s render -c '%s' -o '%s'" % (cmd, comp_path, output_path)
                log("开始渲染: %s" % render_cmd)
                result = subprocess.run(
                    render_cmd, shell=True,
                    capture_output=True, text=True, timeout=900
                )
                if result.returncode == 0:
                    log("✅ 视频渲染成功")
                    return True, output_path
                else:
                    # 提取错误摘要
                    err = result.stderr
                    if len(err) > 500:
                        # 找关键错误行
                        for line in err.split('\n'):
                            if 'Error' in line or 'error' in line or '✗' in line or 'failed' in line:
                                log("渲染错误: %s" % line.strip()[:200])
                                break
                        log("完整错误已写入日志")
                    else:
                        log("视频渲染失败: %s" % err[:300])
                    return False, err[:300]
        except Exception as e:
            continue
    
    log("⚠️ 未找到 HyperFrames CLI，跳过视频渲染")
    return False, "HyperFrames CLI 未安装"


def generate_for_day(day):
    """为指定天数生成视频"""
    log("开始生成第 %d 天视频" % day)
    
    book = get_book_by_day(day)
    log("书籍：《%s》" % book["short_title"])
    
    # 获取内容
    from generate_content import get_prewritten_content, generate_content_from_template
    content = get_prewritten_content(day)
    if not content:
        content = generate_content_from_template(book)
    
    # 生成组合文件
    composition_html, duration = generate_composition_html(day, book, content)
    
    os.makedirs(HF_COMPOSITION_DIR, exist_ok=True)
    comp_filename = "book_%d_%s.html" % (day, sanitize_filename(book["short_title"]))
    comp_path = os.path.join(HF_COMPOSITION_DIR, comp_filename)
    
    with open(comp_path, "w", encoding="utf-8") as f:
        f.write(composition_html)
    
    log("组合文件已生成：%s" % comp_path)
    log("目标时长：%d秒" % duration)
    
    # 尝试渲染视频
    os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)
    video_filename = "book_%d_%s.mp4" % (day, sanitize_filename(book["short_title"]))
    video_path = os.path.join(VIDEO_OUTPUT_DIR, video_filename)
    
    success, result = render_video(comp_path, video_path)
    
    if success:
        log("✅ 视频生成完成：%s" % video_path)
        return video_path, video_filename, comp_path
    else:
        log("⚠️ 视频渲染跳过，组合文件在：%s" % comp_path)
        return None, video_filename, comp_path


def main():
    if len(sys.argv) > 1:
        try:
            day = int(sys.argv[1])
        except ValueError:
            log("错误：天数必须是整数")
            sys.exit(1)
    else:
        from datetime import date
        START_DATE = date(2026, 10, 22)
        today = date.today()
        day = (today - START_DATE).days + 1
        if day < 1: day = 1
        if day > 100: day = 100
    
    video_path, video_filename, comp_path = generate_for_day(day)
    
    if video_path:
        print("\n视频文件：%s" % video_path)
    else:
        print("\n组合文件：%s" % comp_path)
        print("（视频渲染跳过，可手动使用 hyperframes render -c 组合文件路径 渲染）")


if __name__ == "__main__":
    main()
