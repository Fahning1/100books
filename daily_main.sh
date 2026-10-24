#!/bin/bash
# ============================================================
# 100天100本书 · 每日主调度脚本
# 功能：串联完整流水线 - 内容生成 → 视频生成 → GitHub上传 → 飞书推送
# 用法：./daily_main.sh
# 建议：22:00 执行
# ============================================================

set -e  # 出错即退出

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 配置
PYTHON="/usr/bin/python3"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/daily_main_$(date +%Y%m%d).log"
START_DATE="2026-10-22"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

log "=================================================="
log "🚀 每日流水线启动"
log "=================================================="

# ============================================================
# 步骤1：计算今天是第几天
# ============================================================
log "📅 步骤1：计算学习天数"

# 使用 Python 计算天数（更可靠的日期计算）
DAY_NUM=$($PYTHON -c "
from datetime import date
start = date(2026, 10, 22)
today = date.today()
delta = (today - start).days + 1
if delta < 1: delta = 1
if delta > 100: delta = 100
print(delta)
")

log "   今天是第 $DAY_NUM 天 / 100 天"

# 获取书籍信息
BOOK_INFO=$($PYTHON - "$SCRIPT_DIR" "$DAY_NUM" <<'PYEOF'
import sys
sys.path.insert(0, sys.argv[1])
from books_data import get_book_by_day
book = get_book_by_day(int(sys.argv[2]))
author = book.get('author') or '佚名'
print(f"{book['short_title']}||{author}||{book['category']}")
PYEOF
)

BOOK_TITLE=$(echo "$BOOK_INFO" | cut -d'|' -f1)
BOOK_AUTHOR=$(echo "$BOOK_INFO" | cut -d'|' -f2)
BOOK_CATEGORY=$(echo "$BOOK_INFO" | cut -d'|' -f3)

log "   今日书目：《$BOOK_TITLE》- $BOOK_AUTHOR ($BOOK_CATEGORY)"

# ============================================================
# 步骤2：生成深度内容HTML
# ============================================================
log "📝 步骤2：生成深度内容 HTML"

CONTENT_START=$(date +%s)

if $PYTHON "$SCRIPT_DIR/generate_content.py" "$DAY_NUM" >> "$LOG_FILE" 2>&1; then
    CONTENT_END=$(date +%s)
    CONTENT_DURATION=$((CONTENT_END - CONTENT_START))
    log "   ✅ 内容生成完成，用时 ${CONTENT_DURATION} 秒"
else
    log "   ❌ 内容生成失败！"
    log "   详见日志：$LOG_FILE"
    exit 1
fi

# 生成文件名（与 Python 脚本保持一致）
CLEAN_TITLE=$($PYTHON -c "
import re
title = '''$BOOK_TITLE'''
title = re.sub(r'[\\\\/:*?\"<>|（）()《》【】·.，,！!？?]', '', title)
print(title[:30])
")
HTML_FILENAME="book_${DAY_NUM}_${CLEAN_TITLE}.html"
HTML_PATH="$SCRIPT_DIR/books/$HTML_FILENAME"

if [ -f "$HTML_PATH" ]; then
    HTML_SIZE=$(du -h "$HTML_PATH" | cut -f1)
    log "   文件：$HTML_FILENAME ($HTML_SIZE)"
else
    log "   ⚠️ HTML 文件未找到：$HTML_PATH"
fi

# ============================================================
# 步骤3：生成动画视频（可选，失败不中断流程）
# ============================================================
log "🎬 步骤3：生成动画视频"

VIDEO_START=$(date +%s)
VIDEO_GENERATED=false
VIDEO_FILENAME="book_${DAY_NUM}_${CLEAN_TITLE}.mp4"
VIDEO_PATH="$SCRIPT_DIR/videos/$VIDEO_FILENAME"

if $PYTHON "$SCRIPT_DIR/generate_video.py" "$DAY_NUM" >> "$LOG_FILE" 2>&1; then
    VIDEO_END=$(date +%s)
    VIDEO_DURATION=$((VIDEO_END - VIDEO_START))
    
    if [ -f "$VIDEO_PATH" ]; then
        VIDEO_SIZE=$(du -h "$VIDEO_PATH" | cut -f1)
        log "   ✅ 视频生成完成，用时 ${VIDEO_DURATION} 秒"
        log "   文件：$VIDEO_FILENAME ($VIDEO_SIZE)"
        VIDEO_GENERATED=true
    else
        log "   ⚠️ 视频组合文件已生成，但 MP4 未生成（HyperFrames CLI 可能未安装）"
        log "   组合文件在 hf_compositions/ 目录中，可手动渲染"
    fi
else
    log "   ⚠️ 视频生成失败，继续后续流程"
fi

# ============================================================
# 步骤4：上传到 GitHub
# ============================================================
log "☁️ 步骤4：上传到 GitHub"

UPLOAD_START=$(date +%s)
HTML_URL=""
VIDEO_URL=""

if $PYTHON "$SCRIPT_DIR/upload_github.py" "$DAY_NUM" >> "$LOG_FILE" 2>&1; then
    UPLOAD_END=$(date +%s)
    UPLOAD_DURATION=$((UPLOAD_END - UPLOAD_START))
    log "   ✅ 上传完成，用时 ${UPLOAD_DURATION} 秒"
    
    # 构造 URL
    HTML_URL="https://Fahning1.github.io/100books/books/$HTML_FILENAME"
    if [ "$VIDEO_GENERATED" = true ]; then
        VIDEO_URL="https://Fahning1.github.io/100books/videos/$VIDEO_FILENAME"
    fi
    
    log "   内容页：$HTML_URL"
    if [ -n "$VIDEO_URL" ]; then
        log "   视频页：$VIDEO_URL"
    fi
else
    log "   ❌ 上传失败！"
    log "   详见日志：$LOG_FILE"
    # 上传失败不退出，继续尝试推送（本地文件仍在）
fi

# ============================================================
# 步骤5：飞书推送
# ============================================================
log "💬 步骤5：飞书消息推送"

PUSH_START=$(date +%s)

# 调用推送脚本，传入当天内容页 URL
if $PYTHON "$SCRIPT_DIR/daily_push.py" "$DAY_NUM" "$HTML_URL" "$VIDEO_URL" >> "$LOG_FILE" 2>&1; then
    PUSH_END=$(date +%s)
    PUSH_DURATION=$((PUSH_END - PUSH_START))
    log "   ✅ 推送完成，用时 ${PUSH_DURATION} 秒"
else
    log "   ❌ 推送失败！"
    log "   详见日志：$LOG_FILE"
    exit 1
fi

# ============================================================
# 完成
# ============================================================
TOTAL_END=$(date +%s)
TOTAL_DURATION=$((TOTAL_END - $(date -d "$START_DATE" +%s 2>/dev/null || echo 0)))
# 计算总耗时（从脚本启动开始）
START_TIME=$(head -1 "$LOG_FILE" | grep -oP '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}' | head -1)
log "=================================================="
log "🎉 每日流水线完成！"
log "=================================================="
log "📖 第 $DAY_NUM 天：《$BOOK_TITLE》"
log "📝 内容文件：$HTML_FILENAME"
if [ "$VIDEO_GENERATED" = true ]; then
    log "🎬 视频文件：$VIDEO_FILENAME"
fi
if [ -n "$HTML_URL" ]; then
    log "🌐 内容链接：$HTML_URL"
fi
log "=================================================="

exit 0
