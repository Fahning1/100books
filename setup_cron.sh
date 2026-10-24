#!/bin/bash
# ============================================================
# 100天100本书 · crontab 定时任务设置脚本
# 用法：./setup_cron.sh
# 功能：配置每日 22:00 自动执行内容生成流水线
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAIN_SCRIPT="$SCRIPT_DIR/daily_main.sh"

# 确保主调度脚本可执行
chmod +x "$MAIN_SCRIPT"

# 要添加的 cron 任务
CRON_JOB="0 22 * * * $MAIN_SCRIPT >> $SCRIPT_DIR/logs/cron.log 2>&1"

# 检查是否已存在
EXISTING=$(crontab -l 2>/dev/null || echo "")

if echo "$EXISTING" | grep -q "daily_main.sh"; then
    echo "⚠️  crontab 中已存在 daily_main.sh 任务"
    echo "当前任务："
    crontab -l | grep "daily_main.sh"
    exit 0
fi

# 添加新任务
if [ -z "$EXISTING" ]; then
    echo "$CRON_JOB" | crontab -
else
    (echo "$EXISTING"; echo "$CRON_JOB") | crontab -
fi

echo "✅ crontab 定时任务已设置"
echo ""
echo "任务内容："
echo "  0 22 * * *  $MAIN_SCRIPT"
echo ""
echo "执行时间：每天 22:00"
echo "日志位置：$SCRIPT_DIR/logs/cron.log"
echo ""
echo "当前 crontab 列表："
crontab -l
