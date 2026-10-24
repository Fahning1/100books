#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
100天100本书 · 每日学习推送脚本
功能：计算当日学习天数，生成飞书消息并推送到指定群聊
用法：python3 daily_push.py
"""

import json
import subprocess
import sys
import os
from datetime import datetime, date

# ==================== 配置区 ====================
# 起始日期（第1天）
START_DATE = date(2026, 10, 22)

# 目标群聊 chat_id
CHAT_ID = "oc_2a15e76af3560429f6968348e42cb1c2"

# 学习页面链接（GitHub Pages）
LEARN_URL = "https://Fahning1.github.io/100books/"

# lark-cli 路径（使用绝对路径，确保 cron 环境可找到）
LARK_CLI = "/Users/fahning/.trae-cn/plugins/trae-remote-official/lark/1.0.5/bin/lark-cli"

# 脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "push.log")
# ================================================

# 100本书单数据
BOOKS_DATA = [
    {"day": 1, "title": "经济学原理（第8版）", "author": "曼昆", "category": "经济学和大势"},
    {"day": 2, "title": "宏观经济学（第十一版）", "author": "曼昆", "category": "经济学和大势"},
    {"day": 3, "title": "宏观经济学二十五讲", "author": "徐高", "category": "经济学和大势"},
    {"day": 4, "title": "战略与路径", "author": "黄奇帆", "category": "经济学和大势"},
    {"day": 5, "title": "分析与思考", "author": "黄奇帆", "category": "经济学和大势"},
    {"day": 6, "title": "八次危机", "author": "温铁军", "category": "经济学和大势"},
    {"day": 7, "title": "解读中国经济", "author": "林毅夫", "category": "经济学和大势"},
    {"day": 8, "title": "当代中国经济改革教程", "author": "吴敬琏", "category": "经济学和大势"},
    {"day": 9, "title": "繁荣与衰退", "author": "格林斯潘", "category": "经济学和大势"},
    {"day": 10, "title": "时运变迁", "author": "保罗·沃尔克", "category": "经济学和大势"},
    {"day": 11, "title": "21世纪货币政策", "author": "本·伯南克", "category": "经济学和大势"},
    {"day": 12, "title": "当音乐停止之后", "author": "艾伦·布林德", "category": "经济学和大势"},
    {"day": 13, "title": "亚洲大趋势", "author": "乔·史塔威尔", "category": "经济学和大势"},
    {"day": 14, "title": "激荡三十年", "author": "吴晓波", "category": "经济学和大势"},
    {"day": 15, "title": "小米创业思考", "author": "雷军", "category": "创业思维"},
    {"day": 16, "title": "段永平投资问答录", "author": "段永平", "category": "创业思维"},
    {"day": 17, "title": "经营者养成笔记", "author": "柳井正", "category": "创业思维"},
    {"day": 18, "title": "一胜九败", "author": "柳井正", "category": "创业思维"},
    {"day": 19, "title": "富甲美国", "author": "山姆·沃尔顿", "category": "创业思维"},
    {"day": 20, "title": "一只小鸟告诉我的事", "author": "比兹·斯通", "category": "创业思维"},
    {"day": 21, "title": "从0到1", "author": "彼得·蒂尔", "category": "创业思维"},
    {"day": 22, "title": "经营管理全集", "author": "松下幸之助", "category": "创业思维"},
    {"day": 23, "title": "创新者的解答", "author": "克里斯坦森", "category": "创业思维"},
    {"day": 24, "title": "精益创业", "author": "埃里克·莱斯", "category": "创业思维"},
    {"day": 25, "title": "精益创业实战", "author": "阿什·莫瑞亚", "category": "创业思维"},
    {"day": 26, "title": "重新定义公司", "author": "埃里克·施密特", "category": "创业思维"},
    {"day": 27, "title": "格鲁夫给经理人的第一课", "author": "安迪·格鲁夫", "category": "创业思维"},
    {"day": 28, "title": "关乎天下", "author": "关明生", "category": "创业思维"},
    {"day": 29, "title": "创业维艰", "author": "本·霍洛维茨", "category": "创业思维"},
    {"day": 30, "title": "创业之殇", "author": "David Feinleib", "category": "创业思维"},
    {"day": 31, "title": "大败局Ⅰ", "author": "吴晓波", "category": "创业思维"},
    {"day": 32, "title": "大败局Ⅱ", "author": "吴晓波", "category": "创业思维"},
    {"day": 33, "title": "十亿美金的教训", "author": "林军", "category": "创业思维"},
    {"day": 34, "title": "微信背后的产品观", "author": "张小龙", "category": "如何做产品"},
    {"day": 35, "title": "人人都是产品经理", "author": "苏杰", "category": "如何做产品"},
    {"day": 36, "title": "真需求", "author": "梁宁", "category": "如何做产品"},
    {"day": 37, "title": "俞军产品方法论", "author": "俞军", "category": "如何做产品"},
    {"day": 38, "title": "鞋狗", "author": "菲尔·奈特", "category": "如何做产品"},
    {"day": 39, "title": "Little Black Stretchy Pants", "author": "Chip Wilson", "category": "如何做产品"},
    {"day": 40, "title": "上瘾", "author": "尼尔·埃亚尔", "category": "如何做产品"},
    {"day": 41, "title": "任天堂的体验设计", "author": "玉树真一郎", "category": "如何做产品"},
    {"day": 42, "title": "启示录", "author": "Marty Cagan", "category": "如何做产品"},
    {"day": 43, "title": "用户体验要素", "author": "杰西·詹姆斯·加勒特", "category": "如何做产品"},
    {"day": 44, "title": "用户体验度量", "author": "汤姆·图丽斯", "category": "如何做产品"},
    {"day": 45, "title": "简约至上", "author": "贾尔斯·科尔伯恩", "category": "如何做产品"},
    {"day": 46, "title": "定位", "author": "艾·里斯 / 杰克·特劳特", "category": "营销和定位"},
    {"day": 47, "title": "21世纪的定位", "author": "艾·里斯 / 劳拉·里斯", "category": "营销和定位"},
    {"day": 48, "title": "升级定位", "author": "冯卫东", "category": "营销和定位"},
    {"day": 49, "title": "参与感", "author": "黎万强", "category": "营销和定位"},
    {"day": 50, "title": "超级符号就是超级创意", "author": "华杉 / 华楠", "category": "营销和定位"},
    {"day": 51, "title": "广告说服力", "author": "亚当·费里尔", "category": "营销和定位"},
    {"day": 52, "title": "影响力", "author": "罗伯特·西奥迪尼", "category": "营销和定位"},
    {"day": 53, "title": "品牌崇拜", "author": "Douglas Atkin", "category": "营销和定位"},
    {"day": 54, "title": "疯传", "author": "乔纳·伯杰", "category": "营销和定位"},
    {"day": 55, "title": "引爆点", "author": "马尔科姆·格拉德威尔", "category": "营销和定位"},
    {"day": 56, "title": "很久很久以前（新版）", "author": "玛格丽特·马克", "category": "营销和定位"},
    {"day": 57, "title": "很久很久以前（旧版）", "author": "玛格丽特·马克", "category": "营销和定位"},
    {"day": 58, "title": "文化战略", "author": "道格拉斯·霍尔特", "category": "营销和定位"},
    {"day": 59, "title": "第四消费时代", "author": "三浦展", "category": "营销和定位"},
    {"day": 60, "title": "流量池", "author": "杨飞", "category": "流量和增长"},
    {"day": 61, "title": "三双鞋", "author": "谢家华", "category": "流量和增长"},
    {"day": 62, "title": "增长黑客", "author": "Sean Ellis", "category": "流量和增长"},
    {"day": 63, "title": "硅谷增长黑客实战笔记", "author": "曲卉", "category": "流量和增长"},
    {"day": 64, "title": "新增量", "author": "彭志强", "category": "流量和增长"},
    {"day": 65, "title": "精益数据分析", "author": "阿利斯泰尔·克罗尔", "category": "流量和增长"},
    {"day": 66, "title": "牵引力", "author": "加布里埃尔·温伯格", "category": "流量和增长"},
    {"day": 67, "title": "即时引爆", "author": "徐志斌", "category": "流量和增长"},
    {"day": 68, "title": "小群效应", "author": "徐志斌", "category": "流量和增长"},
    {"day": 69, "title": "直播电商的逻辑", "author": "楚燕来", "category": "流量和增长"},
    {"day": 70, "title": "流媒体时代", "author": "迈克尔·D.史密斯", "category": "流量和增长"},
    {"day": 71, "title": "从报表看企业", "author": "张新民", "category": "财务金融和法律"},
    {"day": 72, "title": "财报掘金", "author": "张新民", "category": "财务金融和法律"},
    {"day": 73, "title": "稻盛和夫的实学：经营与会计", "author": "稻盛和夫", "category": "财务金融和法律"},
    {"day": 74, "title": "中小企业财务报表分析", "author": "张新民", "category": "财务金融和法律"},
    {"day": 75, "title": "企业财税合规实战入门", "author": "宋槿篱", "category": "财务金融和法律"},
    {"day": 76, "title": "电商财税合规一本通", "author": "", "category": "财务金融和法律"},
    {"day": 77, "title": "创业投资法律手册", "author": "杨春宝", "category": "财务金融和法律"},
    {"day": 78, "title": "什么是金融", "author": "米希尔·德赛", "category": "财务金融和法律"},
    {"day": 79, "title": "公司理财（第13版）", "author": "斯蒂芬·罗斯", "category": "财务金融和法律"},
    {"day": 80, "title": "金融经济学二十五讲", "author": "徐高", "category": "财务金融和法律"},
    {"day": 81, "title": "投资估价", "author": "达摩达兰", "category": "财务金融和法律"},
    {"day": 82, "title": "穿越寒冬", "author": "史蒂文·霍夫曼", "category": "股权分配和融资"},
    {"day": 83, "title": "超级天使投资", "author": "戴维·罗斯", "category": "股权分配和融资"},
    {"day": 84, "title": "风险投资交易（第4版）", "author": "布拉德·菲尔德", "category": "股权分配和融资"},
    {"day": 85, "title": "股权融资：创业与风险投资", "author": "桂曙光", "category": "股权分配和融资"},
    {"day": 86, "title": "创业之初你不可不知的融资知识", "author": "桂曙光", "category": "股权分配和融资"},
    {"day": 87, "title": "给你一个亿", "author": "查立", "category": "股权分配和融资"},
    {"day": 88, "title": "一本书看透股权架构", "author": "李利威", "category": "股权分配和融资"},
    {"day": 89, "title": "股权是1", "author": "王坤", "category": "股权分配和融资"},
    {"day": 90, "title": "股权战争", "author": "苏龙飞", "category": "股权分配和融资"},
    {"day": 91, "title": "穷查理宝典", "author": "查理·芒格", "category": "团队建设"},
    {"day": 92, "title": "高效能人士的七个习惯", "author": "史蒂芬·柯维", "category": "团队建设"},
    {"day": 93, "title": "学会提问（第12版）", "author": "尼尔·布朗", "category": "团队建设"},
    {"day": 94, "title": "金字塔原理", "author": "芭芭拉·明托", "category": "团队建设"},
    {"day": 95, "title": "创造时间", "author": "杰克·纳普", "category": "团队建设"},
    {"day": 96, "title": "OKR：目标与关键成果法", "author": "保罗·R·尼文", "category": "团队建设"},
    {"day": 97, "title": "这就是OKR", "author": "约翰·杜尔", "category": "团队建设"},
    {"day": 98, "title": "不拘一格", "author": "里德·哈斯廷斯", "category": "团队建设"},
    {"day": 99, "title": "奈飞文化手册", "author": "帕蒂·麦考德", "category": "团队建设"},
    {"day": 100, "title": "广告人告白", "author": "黄霑", "category": "团队建设"},
]

# 分类图标
CATEGORY_ICONS = {
    "经济学和大势": "📈",
    "创业思维": "💡",
    "如何做产品": "📦",
    "营销和定位": "🎯",
    "流量和增长": "🚀",
    "财务金融和法律": "💰",
    "股权分配和融资": "🏢",
    "团队建设": "👥",
}

# 学习寄语库（按天轮换）
QUOTES = [
    "每一本书都是一扇通往新世界的门。今天，让我们一起推开这扇门。",
    "读书的意义，是让我们在迷茫时，拥有一份内在的定力。",
    "真正的学习，是把别人的智慧，变成自己的武器。",
    "一天一本书，不是为了读完，而是为了每天都在进步的路上。",
    "知识的复利效应，远超你我的想象。坚持，就有答案。",
    "你读过的书，终会成为你的骨血，在关键时刻给你力量。",
    "读书不是为了反驳，而是为了思考；不是为了崇拜，而是为了超越。",
    "在不确定性中，唯一确定的投资，就是投资自己的大脑。",
    "慢即是快。每天精读一本好书，胜过一年匆匆翻过百本。",
    "所有看似遥不可及的目标，拆成每一天的行动，都触手可及。",
]


def get_today_book():
    """计算今天对应的书籍"""
    today = date.today()
    delta = (today - START_DATE).days + 1
    if delta < 1:
        delta = 1
    if delta > 100:
        delta = 100  # 超过100天循环到第100天
    book = BOOKS_DATA[delta - 1]
    return delta, book


def generate_message(day_num, book, content_url=None, video_url=None):
    """生成飞书消息 Markdown 内容"""
    category_icon = CATEGORY_ICONS.get(book["category"], "📚")
    quote = QUOTES[(day_num - 1) % len(QUOTES)]

    # 学习页面链接（优先使用当日内容页，否则用总览页）
    learn_link = content_url if content_url else LEARN_URL

    # 视频链接部分
    video_section = ""
    if video_url:
        video_section = f"""
🎬 [观看动画视频]({video_url})
"""

    message = f"""📚 **100天100本书 · 今日学习**

📖 **第 {day_num} 天 · {book['title']}**
{category_icon} 分类：{book['category']}
✍️ 作者：{book['author'] or '佚名'}

---

🔗 [进入深度学习页面]({learn_link})
{video_section}
**内容包含：** 语音导读 · 核心精读 · 经典案例 · 思维工具 · 自测练习

---

💡 **今日寄语**
> {quote}

📅 计划进度：{day_num} / 100 天（{(day_num/100*100):.0f}%）
⏰ 建议学习时长：60 分钟

---
*每日 23:00 自动推送 · 坚持，是最朴素的力量*"""

    return message


def send_message(message):
    """通过 lark-cli 发送飞书消息到群聊"""
    try:
        cmd = [
            LARK_CLI, "im", "+messages-send",
            "--chat-id", CHAT_ID,
            "--markdown", message,
            "--format", "json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


def log(message):
    """写日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass


def main():
    log("=" * 50)
    log("开始执行每日推送任务")

    # 解析命令行参数
    # 用法：python3 daily_push.py [day_num] [content_url] [video_url]
    day_num = None
    content_url = None
    video_url = None
    
    if len(sys.argv) >= 2:
        try:
            day_num = int(sys.argv[1])
        except ValueError:
            day_num = None
    
    if len(sys.argv) >= 3 and sys.argv[2]:
        content_url = sys.argv[2]
    
    if len(sys.argv) >= 4 and sys.argv[3]:
        video_url = sys.argv[3]

    # 1. 获取今日书籍
    if day_num is None:
        day_num, book = get_today_book()
    else:
        if day_num < 1 or day_num > len(BOOKS_DATA):
            log(f"错误：天数 {day_num} 超出范围 (1-{len(BOOKS_DATA)})")
            sys.exit(1)
        book = BOOKS_DATA[day_num - 1]
    
    log(f"今日：第 {day_num} 天 - 《{book['title']}》")
    if content_url:
        log(f"内容页：{content_url}")
    if video_url:
        log(f"视频页：{video_url}")

    # 2. 生成消息
    message = generate_message(day_num, book, content_url, video_url)
    log("消息内容生成完成")

    # 3. 发送消息
    success, result = send_message(message)
    if success:
        log(f"消息发送成功：{result[:100]}...")
        print(f"✅ 推送成功：第 {day_num} 天《{book['title']}》")
    else:
        log(f"消息发送失败：{result}")
        print(f"❌ 推送失败：{result}")
        sys.exit(1)

    log("推送任务完成")
    log("=" * 50)


if __name__ == "__main__":
    main()
