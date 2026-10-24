#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
100天100本书 · 每日内容生成脚本
功能：根据天数生成该书的深度学习内容HTML网页
用法：python3 generate_content.py [day_number]

内容结构（v4深度内容架构）：
  1. AI语音导读（带引导文案）
  2. 全书概览 + 知识图谱
  3. 核心概念深度卡片（可展开手风琴）
  4. 经典案例分析
  5. 思维工具与行动指南
  6. 思维实验/场景题
  7. 精华笔记 + 金句 + 自测题
"""

import os
import sys
import json
import re
from datetime import datetime

# 将脚本所在目录加入路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from books_data import BOOKS, get_book_by_day, get_category_themes

# ==================== 配置区 ====================
# 输出目录
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "books")
LOG_FILE = os.path.join(SCRIPT_DIR, "logs", "generate_content.log")

# 学习页面基础URL
BASE_URL = "https://Fahning1.github.io/100books/books/"
# ==============================================


def log(msg):
    """写日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {msg}\n"
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass
    print(log_line.strip())


def sanitize_filename(title):
    """清理文件名中的特殊字符"""
    title = re.sub(r'[\\/:*?"<>|（）()《》【】·.，,！!？?]', '', title)
    return title[:30]


# ============================================================
# 深度内容预生成（第1-3天的完整深度内容）
# ============================================================
PREWRITTEN_CONTENT = {}

# --- 第1天：经济学原理 ---
PREWRITTEN_CONTENT[1] = {
    "hook": "经济学不是关于钱，而是关于选择。当资源有限而欲望无限，每一次决定都是一次放弃。",
    "overview": "《经济学原理》是哈佛大学教授曼昆的经济学入门经典，被全球超过七百所大学采用。本书建立在十大经济学原理之上，从微观到宏观构建完整的经济学思维框架。微观部分探讨个体如何决策、市场如何运行；宏观部分将视角拉高，研究GDP、增长、货币、通胀与经济波动。理解这本书，是理解后面所有商业书籍的基础——因为它提供的不是某个领域的结论，而是一套所有领域通用的分析工具。",
    "chapter_map": [
        {"part": "第一篇", "name": "导言", "chapters": "第1—2章", "essence": "十大原理与经济学家的思维方式", "question": "为什么稀缺性是一切经济问题的起点？"},
        {"part": "第二篇", "name": "市场如何运行", "chapters": "第4—6章", "essence": "供给、需求与市场均衡的形成", "question": "价格到底是由谁决定的？"},
        {"part": "第三篇", "name": "市场与福利", "chapters": "第7—9章", "essence": "消费者剩余、生产者剩余与贸易收益", "question": "市场效率该如何衡量？"},
        {"part": "第四篇", "name": "公共部门经济学", "chapters": "第10—12章", "essence": "外部性、公共物品与税收", "question": "市场失灵时政府该做什么？"},
        {"part": "第五篇", "name": "企业行为与产业组织", "chapters": "第13—17章", "essence": "成本、竞争、垄断与寡头", "question": "企业为什么能获得超额利润？"},
        {"part": "第六篇", "name": "劳动市场", "chapters": "第18—20章", "essence": "要素价格、工资差异与收入分配", "question": "为什么同样的工作工资不同？"},
        {"part": "第七篇", "name": "宏观经济学", "chapters": "第23—36章", "essence": "GDP、货币、通胀、增长与短期波动", "question": "一个国家为什么会繁荣或衰退？"}
    ],
    "insights": [
        {
            "num": "01",
            "title": "人们面临权衡取舍",
            "subtitle": "Everything is a trade-off",
            "paragraphs": [
                "经济学之所以存在，根本原因是稀缺性——社会拥有的资源总是有限的，而人类的欲望是无限的。稀缺性意味着必须做出选择，而「选择」这个词的另一面，就是「放弃」。当你决定把一小时用来读这本书，你就放弃了这一小时本可以做其他所有事情的可能性。",
                "曼昆把这一逻辑概括成一句话：人们面临权衡取舍。这句话听上去像废话，但它的力量在于，它强迫你在任何决策面前先问一句：我打算拿什么来换？大多数糟糕的决策，原因在于假装不需要付出代价，而不在于不知道自己要什么。",
                "最著名的一组权衡是效率与平等。效率指社会能从稀缺资源中获得最大利益，平等指把这些成果较为平均地分配给社会成员。当政府想要更平等——例如向高收入者征税补贴低收入者——这会削弱工作与投资的激励，社会生产的总蛋糕可能缩小。反过来，一个完全按贡献分配的社会效率很高，但贫富差距会扩大。这是结构性矛盾，与政策执行的水平无关：任何试图同时最大化两者的努力，都会在另一端留下妥协。",
                "在个人层面，权衡取舍体现为时间、注意力与资金的分配。你的一天只有24小时，投入到A项目的每一分钟，都是从B项目借来的。真正稀缺的往往不是钱，而是注意力——钱可以再赚，注意力一旦被切碎就无法复原。",
                "在组织层面，战略的本质就是取舍。迈克尔·波特有一个著名判断：战略的核心在于选择不做什么，而不在于选择做什么。一家企业若想同时讨好所有人——高端又要低价，快速又要精致，宽产品线又要极致单品——最终会在每一个维度上都变得平庸。取舍之所以难，是因为它要求你公开承认自己不要什么。"
            ],
            "examples": [
                {"title": "初创公司的产品线扩张", "text": "某SaaS公司成立第二年，客户提出了十几个新功能需求。团队一一满足，产品线从3个模块膨胀到11个，结果每个模块都做到60分。同期一家竞争对手只做2个模块，做到95分，拿下了大客户。这不是执行力差距，而是取舍失效：资源被平均分配，就等于没有分配。"},
                {"title": "大学生的暑假选择", "text": "一个暑假可以用来实习、备考、旅行或陪家人。选择实习意味着放弃备考的时间，而备考又意味着放弃实习的履历。做决定的正确方式，是明确这一个暑假你最想获得哪一种「不可替代的资产」，其余选项就要被有意识地放弃，而不是拖延到最后什么都没做。"}
            ],
            "terms": [
                {"term": "稀缺性", "def": "社会拥有的资源是有限的，因此不能生产人们希望拥有的所有物品与服务。"},
                {"term": "效率", "def": "社会能从其稀缺资源中得到最大利益的特性。"},
                {"term": "平等", "def": "经济成果在社会成员中平均分配的特性。"}
            ],
            "takeaway": "做任何决定前先问一句：我为此放弃了什么？如果答不出来，说明你还没想清楚。"
        },
        {
            "num": "02",
            "title": "机会成本才是真实成本",
            "subtitle": "The cost of something is what you give up to get it",
            "paragraphs": [
                "教科书对成本的定义与现实中的直觉差别很大：某种东西的成本，是为了得到它所放弃的东西。这个定义把「成本」从会计账簿上的支出，扩展到了所有被放弃的可能性。",
                "因此要区分两类成本。显性成本是你实际掏出去的钱，比如学费、房租、原材料。隐性成本是你没有掏钱、但真实损失掉的价值，比如你创业时放弃的年薪、你读书时放弃的四年工作经验。决策时只看显性成本，是最常见的系统性错误。",
                "机会成本还必须与沉没成本严格区分。沉没成本是已经发生且无法收回的支出，它不应该影响任何未来决策。电影票已经买了、发现难看，理性决策的依据是「接下来这两小时怎么用更好」，而不是「票钱不能白花」。人之所以常常被沉没成本绑架，是因为把「避免承认损失」当成了收益。",
                "机会成本思维在商业上最具杀伤力的应用，是判断一件事该不该自己做。如果一项工作的机会成本高于外包价格，就应该外包。很多创业者把所有事情都自己扛，账面上省了钱，实际上把最贵的那部分资源——创始人的时间——投入到了最低价值的环节。",
                "在个人层面，机会成本解释了为什么「免费」常常是最贵的。免费的公开课、免费的咨询、免费的社交，代价是你的时间与注意力。判断一件事值不值得做，标准应当是「同样的时间投入别处，能否产生更大价值」，而不是它本身是否收费。"
            ],
            "examples": [
                {"title": "读大学的真实成本", "text": "四年学费与生活费假设共20万元，这是显性成本。但如果这四年直接工作，年收入10万元、四年40万元，这40万元就是隐性成本。真实的求学成本接近60万元，而不是20万元。这不意味着读大学不划算——大学带来的人力资本增值可能远超60万元——但它意味着，判断划算与否必须用60万元做分母。"},
                {"title": "开餐厅的机会成本", "text": "一位年薪50万元的产品总监辞职开餐厅，第一年餐厅净赚30万元。账面看是盈利的，但以机会成本衡量，他实际亏损20万元，加上投入的精力与本金风险，这笔账更不划算。很多「赚钱的创业」在机会成本视角下是亏的。"}
            ],
            "terms": [
                {"term": "机会成本", "def": "为了得到某种东西所必须放弃的东西的价值。"},
                {"term": "显性成本", "def": "需要企业支付货币的投入成本，如工资、租金、原材料。"},
                {"term": "隐性成本", "def": "不需要货币支付、但真实存在的成本，如自有资金利息、所有者时间价值。"},
                {"term": "沉没成本", "def": "已经发生且无法收回的成本，理性决策时应被忽略。"}
            ],
            "takeaway": "看到一个价格时，别只问「多少钱」，要问「我还要为此放弃什么」。"
        },
        {
            "num": "03",
            "title": "理性人思考边际量",
            "subtitle": "Think at the margin",
            "paragraphs": [
                "大多数决策真正要回答的问题是「要不要再多做一点」，而非「全做还是全不做」。这种在既有基础上做出的微小增量调整，就是边际变动。理性人做决策时比较的是边际收益与边际成本，当且仅当边际收益大于边际成本时才行动。",
                "为什么必须看边际而不是平均？因为平均量掩盖了下一步的真实得失。一家餐厅的平均成本是每客50元，某天有位客人愿意付40元吃一顿空座位的晚餐，按平均成本算应当拒绝；但多接待这一位客人真正增加的成本（食材、少量人工）可能只有25元，边际收益40元大于边际成本25元，就应该接。决策发生在边缘，而非在平均。",
                "边际收益递减是这个世界最普遍的规律之一。第一块巧克力带来的满足最大，第二块次之，第五块可能变成负担。它解释了两件事：为什么需求曲线向下倾斜，以及为什么「越多越好」是错的。",
                "理解边际，才能真正解开「水与钻石悖论」。水的总效用极高，但因为它太充裕，最后一杯水的边际效用极低，价格由边际效用决定，所以水便宜。钻石相反，总效用很低，但极其稀缺，边际效用极高，所以昂贵。价格反映的是边际上的评价，而非总体的重要性。",
                "在时间管理上，边际思维同样有效。学习到第四个小时，专注度急剧下降，此时第四小时的边际收益可能已经是负的。继续硬撑不如去睡觉——这是边际分析给出的结论，而不是意志力的失败。"
            ],
            "examples": [
                {"title": "飞机起飞前的最后一张票", "text": "航班即将起飞，还有空座。一张票价正常是800元，此时有人愿出300元。航空公司的平均成本可能高达500元，按平均成本应该拒绝。但多载一位乘客的边际成本仅是一份餐食和少量燃油，约50元。300元大于50元，卖票是理性的。这就是边际定价，也是航空公司收益管理的核心逻辑。"},
                {"title": "自助餐为什么能赚钱", "text": "自助餐定价固定，顾客会吃到「边际效用为零」为止——即再吃一口带来的满足抵不过撑胀的痛苦。餐厅的成本主要由固定投入决定，边际成本很低。双方都在按边际决策，交易因此成立。"}
            ],
            "terms": [
                {"term": "边际变动", "def": "在现有行动方案上进行的微小增量调整。"},
                {"term": "边际收益", "def": "多做一单位所增加的额外收益。"},
                {"term": "边际成本", "def": "多做一单位所增加的额外成本。"},
                {"term": "边际效用递减", "def": "随着消费量增加，每增加一单位带来的额外满足感递减。"}
            ],
            "takeaway": "别问「总共值不值」，要问「再多做这一点，值不值」。"
        },
        {
            "num": "04",
            "title": "激励会改变行为，包括你没预料到的行为",
            "subtitle": "People respond to incentives",
            "paragraphs": [
                "激励是引起一个人做出某种行为的某种东西，可以是奖励，也可以是惩罚。由于理性人在边际上比较成本与收益，所以他们对激励的反应是可预测的——这正是经济学能够解释人类行为的原因。",
                "价格是最直接的激励。苹果涨价，消费者少买、果农多种；油价上涨，大排量车销量下滑、混动车畅销。整条供给与需求曲线，本质上都是对激励的反应函数。",
                "但激励的真正难点在于非预期后果。政策或制度改变了成本收益结构，人们会调整行为，而这种调整常常不是设计者想要的。安全带的例子最经典：安全带降低了事故中死亡的概率，于是人们在开车时更敢冒险、开得更快，结果是事故次数上升，行人死亡增加。单看「安全带减少了驾驶员死亡」是对的，作为整体政策评估，效果被抵消了一部分。",
                "在组织管理中，激励设计几乎决定了一切。你考核什么，就得到什么，而且往往得到的是「考核指标的扭曲版本」。销售只考核销售额，就会出现压货与虚假订单；客服只考核通话时长，就会出现草草挂断。这不是员工品行问题，而是激励结构问题——想要正确的行为，必须让正确的行为有利可图。",
                "因此在设计任何制度时，最重要的动作不是问「大家会不会照做」，而是问「如果我是被激励的一方，我会怎么钻这个规则的空子」。能通过这个测试的制度，才是可用制度。"
            ],
            "examples": [
                {"title": "安全带法案的意外结果", "text": "美国1960年代推行强制安全带立法后，驾驶员死亡人数下降，但交通事故总量上升，行人死亡也有所增加。经济学家的解释是：安全带降低了死亡成本，理性司机因此在边际上提高了车速与冒险程度。激励被改变了，行为随之改变，部分政策效果被行为反应吃掉。"},
                {"title": "销售提成的扭曲", "text": "某公司按签约额给销售提成，结果销售拼命签下质量差、回款难的客户，年末大量坏账。改为按「回款额」提成后，销售开始主动筛客户。指标没变严，行为却变健康了——因为激励的方向变了。"}
            ],
            "terms": [
                {"term": "激励", "def": "引起一个人做出某种行为的东西，如奖励或惩罚。"},
                {"term": "非预期后果", "def": "制度或政策引发的人们行为调整，其结果与设计初衷不符。"},
                {"term": "道德风险", "def": "一方在受到保护或不必承担全部后果时，倾向于采取更高风险的行为。"}
            ],
            "takeaway": "设计规则时，先站到「想钻空子的人」那一侧看一遍。"
        },
        {
            "num": "05",
            "title": "比较优势让贸易成为双赢",
            "subtitle": "Trade can make everyone better off",
            "paragraphs": [
                "很多人对贸易的理解是零和的：一方赚钱，另一方必然吃亏。经济学给出的结论恰恰相反——在自愿交易的前提下，贸易让双方都变好。原因在于比较优势，而非绝对优势。",
                "绝对优势指用更少的投入生产同样的东西。比较优势指以更低的机会成本生产某种东西。关键洞察是：即使一方在所有产品上都有绝对优势，双方仍然可以通过专业化与交换获益，因为真正决定分工的是机会成本，而非绝对能力。",
                "设想一位律师打字速度是助理的两倍。看起来律师应该自己打字。但律师打一小时字，就放弃了一小时本可以创造数千元价值的工作；助理打一小时字，放弃的价值很小。因此律师打字的机会成本极高，助理的机会成本很低。律师应该专注于法律工作，把打字交给助理——尽管他在打字上更强。这就是比较优势反直觉的地方：强者应该做自己最擅长且机会成本最高的事，弱者应该做自己机会成本最低的事。",
                "这个逻辑支撑了整个现代经济：分工提高熟练度、减少切换成本、扩大市场规模。全球供应链、专业服务外包、企业内部的职能划分，本质上都是比较优势的应用。",
                "但贸易也有真实的代价：分配效应。贸易让整体蛋糕变大，但某些群体确实受损，例如受进口冲击的行业工人。承认这一点，才能理解为什么自由贸易在政治上总是充满张力。正确的应对是帮助受损者转型，而不是否认损失存在。"
            ],
            "examples": [
                {"title": "律师与助理", "text": "律师每小时创收2000元，打字速度是助理的2倍。假设打字一小时助理产出价值100元。律师打字的机会成本是2000元，助理是100元。即便律师打字更快，让助理打字、律师专注办案，总产出更高。这就是比较优势压倒绝对优势。"},
                {"title": "中国的制造业分工", "text": "过去四十年，中国在劳动密集型制造环节具备明显的比较优势，逐步嵌入全球供应链。这并非因为中国在每个环节都最强，而是因为在组装制造环节的机会成本最低。随着要素价格上升，比较优势开始向研发、供应链组织等高附加值环节迁移，产业升级本质上就是比较优势的动态变化。"}
            ],
            "terms": [
                {"term": "绝对优势", "def": "用比另一个生产者更少的投入生产某种物品的能力。"},
                {"term": "比较优势", "def": "以低于另一个生产者的机会成本生产某种物品的能力。"},
                {"term": "专业化", "def": "将资源集中投入到机会成本最低的环节。"}
            ],
            "takeaway": "不要问「谁更强」，要问「谁做这件事放弃得更少」。"
        }
    ],
    "quotes": [
        {"text": "经济学研究的是一个社会如何管理自己的稀缺资源。在大多数社会中，资源并不是由一个唯一的中央计划者来配置，而是通过千百万家庭和企业的共同行动来配置的。", "source": "曼昆《经济学原理》第1章", "note": "这句话给出了经济学的定义，也隐含了它的政治哲学：分散决策优于集中决策，因为信息是分散的。"},
        {"text": "市场通常是组织经济活动的一种好方法。", "source": "十大原理之六", "note": "注意「通常」二字。曼昆并没有说市场永远有效，这为后面讲外部性、公共物品、市场势力留下了空间。"},
        {"text": "政府有时可以改善市场结果。", "source": "十大原理之七", "note": "与上一条并列，构成一对张力。真正的经济学素养，是判断在具体情境下该偏向哪一边。"},
        {"text": "一国的生活水平取决于它生产物品与服务的能力。", "source": "十大原理之八", "note": "生产率是长期繁荣的唯一来源。这一点解释了为什么产业政策、教育、技术投资比短期刺激更重要。"},
        {"text": "当政府发行了过多货币时，物价上升。", "source": "十大原理之九", "note": "通胀是一种货币现象，长期看几乎总是如此。这条原理在后面的货币政策部分会被反复使用。"}
    ],
    "cases": [
        {
            "icon": "💎",
            "title": "水与钻石悖论：价格为什么由边际决定",
            "background": "亚当·斯密在《国富论》中提出一个困扰经济学界百余年的问题：水是生命必需，几乎无替代品，价格却极低；钻石几乎无实际用途，价格却极高。如果价格反映价值，这个现象完全说不通。",
            "process": "早期劳动价值论试图用「投入的劳动量」解释价格，但无法解释水的价格。19世纪70年代，门格尔、杰文斯、瓦尔拉斯几乎同时提出边际效用理论：价值不是由物品的总效用决定，而是由最后一单位带来的效用决定。因为水极其充裕，最后一杯水的效用很低；钻石极其稀缺，最后一颗钻石的效用极高。",
            "result": "边际效用价值论彻底重塑了经济学，成为现代微观经济学价格理论的基石。它同时解释了「为什么丰裕会让东西变便宜」这一普遍现象。",
            "takeaway": "价格反映的是边际上的稀缺程度，而非总体的重要性。这对商业的启示是：决定你价格的因素，在于你在边际上有多难被替代，而不在于你做了多少工作。",
            "principle": "边际效用决定价格。总效用决定「值不值得拥有」，边际效用决定「值多少钱」。"
        },
        {
            "icon": "🌾",
            "title": "谷贱伤农：丰收为什么让农民更穷",
            "background": "农业社会反复出现一个悖论：风调雨顺、粮食大丰收的年份，农民收入反而下降，甚至出现「丰年饥荒」。这看似违背常识——东西多了怎么会更穷？",
            "process": "粮食是需求缺乏弹性的商品：人一天只能吃那么多，价格再低也很难多吃一倍。当供给大幅增加时，均衡价格必须大幅下降才能出清市场；但需求量增加有限。价格跌幅大于销量增幅，总收入（价格×数量）因此下降。",
            "result": "这一现象推动了农业政策的设计：最低收购价、储备制度、农业保险，本质都是试图切断「增产—降价—减收」的链条。同时也解释了为什么单纯提高产量并不必然提高农民收入。",
            "takeaway": "判断一个生意，不能只看产量或销量，必须看「价格弹性」。需求弹性低的行业，扩产是危险动作；需求弹性高的行业，降价能换来更大市场。",
            "principle": "需求价格弹性小于1时，供给增加导致总收益下降。"
        },
        {
            "icon": "⚖️",
            "title": "最低工资法：善意的价格下限",
            "background": "为了保护低技能劳动者，政府设定最低工资标准，禁止企业以更低工资雇佣工人。政策目标清晰且道德上无可指摘。",
            "process": "从供需模型看，最低工资是对劳动市场设定了一个价格下限，且该下限高于市场均衡工资。价格下限导致供给量（愿意工作的人）增加、需求量（企业愿意雇佣的人）减少，出现过剩——在劳动市场上，过剩的表现就是失业。受影响最大的是最缺乏技能的人，也就是政策原本想保护的人。",
            "result": "实证研究结论并不统一：当最低工资小幅高于均衡时，影响可能很小；当大幅高于均衡、或经济下行时，失业效应明显。这使最低工资成为经济学中最具争议的政策之一。",
            "takeaway": "理解一个政策，要看它的价格机制后果，而不只是它的道德意图。善意与好结果之间，隔着一个激励结构。",
            "principle": "价格下限高于均衡价格，会造成过剩（劳动市场上即失业）。"
        },
        {
            "icon": "🌍",
            "title": "碳排放权交易：给外部性定价",
            "background": "企业排放二氧化碳，成本由全社会承担，企业自己几乎不付代价——这是典型的负外部性。结果是市场自发产生的排放量远高于社会最优水平。",
            "process": "解决方案有两条路径。庇古税：政府按排放量征税，把外部成本内部化。科斯方案：界定产权，允许交易。碳交易属于后者——政府设定排放总量上限，把配额分配给企业，企业之间可以买卖。排放效率高的企业卖出富余配额获利，效率低的企业必须购买，成本上升。",
            "result": "欧盟碳排放交易体系（EU ETS）运行多年，成为全球最大的碳市场。中国也于2021年启动全国碳市场。经验显示：总量上限的设定、配额的初始分配方式（免费还是拍卖）、以及监测核查的严格程度，决定制度成败。",
            "takeaway": "面对外部性，最有效的工具往往是把外部成本变成内部价格，而不只是道德劝说。改变激励结构，比呼吁责任感更可靠。",
            "principle": "外部性导致市场失灵；矫正方式是庇古税或可交易许可证，本质都是给外部成本定价。"
        }
    ],
    "glossary": [
        {"term": "稀缺性", "def": "资源有限而欲望无限，是一切经济问题的起点。", "example": "一天只有24小时，所以必须选择。"},
        {"term": "机会成本", "def": "为得到某物而放弃的其他最佳选择的价值。", "example": "读研的成本包括放弃的两年工资。"},
        {"term": "沉没成本", "def": "已发生且无法收回的成本，不应影响未来决策。", "example": "电影难看也应离场，票钱已经花了。"},
        {"term": "边际效用递减", "def": "消费量增加时，每单位带来的额外满足递减。", "example": "第二杯奶茶不如第一杯好喝。"},
        {"term": "需求定律", "def": "其他条件不变时，价格上升，需求量下降。", "example": "涨价后销量下滑。"},
        {"term": "供给定律", "def": "其他条件不变时，价格上升，供给量上升。", "example": "猪价上涨，养殖户扩产。"},
        {"term": "均衡价格", "def": "供给量等于需求量时的价格，市场自发趋向该点。", "example": "菜市场的实时价格。"},
        {"term": "需求价格弹性", "def": "需求量变动百分比除以价格变动百分比。", "example": "粮食弹性小，奢侈品弹性大。"},
        {"term": "消费者剩余", "def": "买者愿意支付的最高价格减去实际支付价格。", "example": "愿出100元却只花60元，剩余40元。"},
        {"term": "生产者剩余", "def": "卖者实际得到的价格减去其成本。", "example": "成本50元卖80元，剩余30元。"},
        {"term": "外部性", "def": "一个人的行为对旁观者福利的无补偿影响。", "example": "工厂排污损害下游居民。"},
        {"term": "公共物品", "def": "既无排他性又无竞争性的物品。", "example": "国防、路灯、公共卫生。"},
        {"term": "比较优势", "def": "以更低的机会成本生产某物的能力。", "example": "律师雇助理打字。"},
        {"term": "看不见的手", "def": "价格作为信号，引导分散决策者实现资源有效配置。", "example": "涨价自然抑制需求、吸引供给。"},
        {"term": "市场失灵", "def": "市场自身无法有效配置资源的情形。", "example": "污染、垄断、公共品供给不足。"},
        {"term": "通货膨胀", "def": "经济中总体价格水平的上升。", "example": "同样100元买到的东西变少。"}
    ],
    "quiz": [
        {
            "q": "你已花200元买了演唱会门票，到场后发现演出很差。此时最理性的决策依据是？",
            "options": ["因为花了200元，必须看完才不亏", "比较接下来两小时的其他用途价值，再决定是否离开", "看周围人是否离场再决定", "计算200元占月收入的比例"],
            "answer": 1,
            "explanation": "200元是沉没成本，已经无法收回，不应影响决策。正确依据是边际比较：留下的边际收益 vs 离开去做别的事的边际收益。这正是「沉没成本不应影响决策」的经典应用。"
        },
        {
            "q": "某公司平均成本每件80元，现有一批闲置产能，客户愿以60元/件下单1000件。多生产一件的真实成本为35元。按边际思维应当？",
            "options": ["拒绝，因为60元低于平均成本80元", "接受，因为边际收益60元大于边际成本35元", "接受，因为能摊薄固定成本", "无法判断，需要看同行报价"],
            "answer": 1,
            "explanation": "决策发生在边际上。固定成本已经发生，不因是否接单而改变。边际收益60元大于边际成本35元，每件净增25元，应从边际角度接受（前提是不影响其他高价订单）。"
        },
        {
            "q": "粮食丰收后农民总收入下降，最直接的原因是？",
            "options": ["农民议价能力弱", "粮食需求价格弹性小于1", "政府调控价格", "运输成本上升"],
            "answer": 1,
            "explanation": "需求缺乏弹性时，供给增加导致价格大幅下跌，而需求量增加有限，价格跌幅超过销量增幅，总收入下降。这就是「谷贱伤农」的机制。"
        },
        {
            "q": "一位时薪2000元的律师打字速度是助理的2倍，助理时薪100元。最合理的分工是？",
            "options": ["律师自己打字，因为他效率更高", "助理打字，因为律师打字的机会成本更高", "两人各打一半，公平分担", "购买更快的打印机"],
            "answer": 1,
            "explanation": "这是比较优势而非绝对优势的问题。律师打字一小时的机会成本是2000元，助理是100元。即使律师绝对效率更高，让助理打字、律师专注办案的总产出更高。"
        },
        {
            "q": "公司只考核客服的「平均通话时长」，最可能出现的结果是？",
            "options": ["服务质量显著提升", "客服草草结束通话以缩短时长", "客户满意度自然上升", "通话量减少"],
            "answer": 1,
            "explanation": "激励决定行为。只考核时长，员工会优化时长这个指标本身，而非服务质量。这是激励结构导致的指标扭曲——你考核什么，就得到被扭曲的那个版本。"
        },
        {
            "q": "政府对污染企业征收排污税，其经济学本质是？",
            "options": ["增加财政收入", "把负外部性成本内部化", "限制行业发展", "补贴下游居民"],
            "answer": 1,
            "explanation": "污染是负外部性：成本由社会承担，企业不付代价，导致产出高于社会最优。征税使企业边际私人成本上升至边际社会成本，从而把外部成本内部化，产量回落到社会最优水平。"
        }
    ],
    "questions": [
        {"q": "回想你最近一个月做过的最重要的一个决定。它的机会成本是什么？你当时有没有真正把这项成本算进去？", "hint": "不要只算钱。列出你因此放弃的时间、关系、注意力和替代方案。"},
        {"q": "你所在的团队或公司，当前的考核指标会诱导出什么「被扭曲的行为」？如果让你重新设计，你会改哪一条？", "hint": "从「如果我想钻空子，我会怎么做」这个角度切入，最容易发现问题。"},
        {"q": "在你自己的工作中，哪件事其实是你「绝对优势」但「比较优势」很低的？它可以被谁接走？", "hint": "找出那些你做得比同事好、但机会成本极高的事务性工作。"}
    ],
    "thinking_tools": [
        {"name": "供需模型", "desc": "用供给曲线和需求曲线分析市场价格与数量的决定，适用于任何存在买卖关系的场景。"},
        {"name": "成本收益分析", "desc": "列出一个决策的所有成本与收益，包括显性与隐性、当期与未来，再比较净收益。"},
        {"name": "边际分析法", "desc": "判断「再多做一点值不值」，比较边际收益与边际成本，而非看平均量。"},
        {"name": "激励分析框架", "desc": "分析一项制度或政策会如何改变人们的成本收益结构，进而预测行为变化。"},
        {"name": "机会成本清单", "desc": "做决策前，列出你将放弃的Top 3替代方案，评估它们的价值。"}
    ],
    "action_guides": [
        "本周做一个决策时，先用1分钟列出它的机会成本清单。",
        "观察你所在团队的考核制度，找出一条会导致扭曲行为的规则。",
        "找出你自己工作中一件「比较优势低」的事，考虑能否外包或交接。"
    ],
    "guide": [
        {"label": "开场", "text": "你好，欢迎来到一百天一百本书。今天是我们旅程的第一天，要读的是哈佛大学教授格里高利·曼昆的《经济学原理》。这本书被全球超过七百所大学采用，是过去三十年最流行的经济学入门教材。但它的价值不在于流行，而在于它提供了一套可以立刻用在生活里的思维工具。"},
        {"label": "为什么从这本开始", "text": "一百天读一百本书，最怕的是读完一百个孤立的知识点，脑子里还是一团散沙。所以第一本必须是一本「元书」——它不提供某个领域的结论，而是提供一套所有领域通用的分析框架。经济学正是这样一套框架：稀缺、成本、边际、激励、比较优势。这五个概念，后面九十本书里会反复出现。读懂它，后面九十本都会变快。"},
        {"label": "全书地图", "text": "这本书分两大块。微观部分讲个体如何决策、市场如何运行：供给与需求、弹性、消费者与生产者剩余、外部性与公共品、成本与市场结构、劳动市场。宏观部分把视角拉高到整个国家：GDP怎么算、长期增长从哪里来、货币与通胀、开放经济、短期波动与政策。七大模块，三十多章。今天我们不追求覆盖全部，只抓住五个最底层的原理。"},
        {"label": "第一原理", "text": "第一个原理，人们面临权衡取舍。它的根源是稀缺性：资源有限，欲望无限，所以每一次选择都是一次放弃。这句话的真正用途，是逼你在决策前问一句「我拿什么换」。大多数糟糕决策的成因，是假装不需要付代价，而非不知道想要什么。"},
        {"label": "第二原理", "text": "第二个原理，机会成本才是真实成本。成本不是账面支出，而是你为此放弃的东西。所以要区分显性成本与隐性成本，更要和沉没成本划清界限。已花的钱不该左右未来的决定，这一点说起来简单，做起来极难，因为人天生不愿承认损失。"},
        {"label": "第三原理", "text": "第三个原理，理性人在边际上思考。真正要回答的往往不是「全做还是不做」，而是「再一点值不值」。边际收益大于边际成本才行动。这一条能解开经济学史上最著名的谜题：水很重要却便宜，钻石没什么用却昂贵——因为价格由最后一单位的边际效用决定，而非由总体重要性决定。"},
        {"label": "第四原理", "text": "第四个原理，人们会对激励做出反应。价格是最直接的激励，但真正的难点是非预期后果。安全带降低了死亡概率，司机因此开得更快，事故总量反而上升。这在提醒我们：制度设计不能只问意图，必须问「如果我是被激励的一方，我会怎么钻空子」。"},
        {"label": "第五原理", "text": "第五个原理，比较优势让贸易双赢。决定分工的不是谁更强，而是谁做这件事机会成本更低。所以时薪两千的律师该雇助理打字，尽管他打字更快。这个逻辑支撑了全球供应链、专业外包和企业内部分工，也解释了一件事：贸易整体上让蛋糕变大，但确实会让部分群体受损，这两件事同时为真。"},
        {"label": "怎么读这本", "text": "建议你这样安排这一小时。前十来分钟，把这本导读和章节地图过一遍，建立整体结构感。接下来半小时，逐个打开五个核心观点的深度精读，每个读完停一下，用一句话写下你自己的理解，不要复制原文。然后十五分钟，读四个案例，重点看「谷贱伤农」和「最低工资」这两个，它们最能训练你把模型用到现实。最后十分钟，做六道自测题，再回答三个思考题，写进笔记区。"},
        {"label": "一个提醒", "text": "读经济学最容易犯的错误，是把模型当成真理。供给需求曲线是有前提的：完全竞争、信息充分、没有外部性。现实中这些前提经常不成立，所以才需要后面的公共部门经济学和产业组织理论。学经济学不是为了背结论，而是为了知道结论在什么条件下成立。"},
        {"label": "收尾", "text": "今天这五个原理，会是你后面九十九本书的底层操作系统。稀缺决定必须选择，机会成本决定选择的代价，边际决定选择的最优解，激励决定别人如何回应你的选择，比较优势决定你该和谁合作。把这五句话记住，比记住书里任何一张图都值钱。明天我们读曼昆的另一本，《宏观经济学》，把视角从个人抬到国家。我们明天见。"}
    ]
}


def get_prewritten_content(day):
    """获取预写好的深度内容，如果没有则返回None"""
    return PREWRITTEN_CONTENT.get(day)


# ============================================================
# 模板化内容生成器（当没有预写内容时使用）
# ============================================================
def generate_content_from_template(book):
    """根据书籍信息和分类主题生成深度内容模板"""
    themes = get_category_themes(book["category"])
    concepts = themes["core_concepts"]
    tools = themes["thinking_tools"]
    case_types = themes["case_patterns"]
    actions = themes["action_guides"]
    
    # 生成章节地图（5-7个部分）
    chapter_names = [
        "基础概念与核心框架",
        "核心原理与方法论",
        "实践应用与案例",
        "进阶主题与扩展",
        "工具与方法总结"
    ]
    if len(concepts) >= 7:
        chapter_names.insert(2, "关键模型与分析框架")
        chapter_names.insert(4, "前沿发展与趋势")
    
    chapter_map = []
    for i, name in enumerate(chapter_names):
        chapter_map.append({
            "part": f"第{['一','二','三','四','五','六','七'][i]}篇",
            "name": name,
            "chapters": f"第{i*3+1}—{i*3+3}章",
            "essence": f"围绕{concepts[i % len(concepts)]}展开系统论述",
            "question": f"如何理解{concepts[(i+2) % len(concepts)]}在{book['short_title']}中的应用？"
        })
    
    # 生成5个核心观点
    insights = []
    insight_titles = concepts[:5]
    for i, title in enumerate(insight_titles):
        insights.append({
            "num": f"{i+1:02d}",
            "title": title,
            "subtitle": f"Understanding {title}",
            "paragraphs": [
                f"{title}是{book['category']}领域的核心概念之一，也是理解《{book['short_title']}》的关键入口。在{book['author'] or '作者'}的论述体系中，{title}占据着基础性的地位——它不是一个孤立的知识点，而是连接全书多个章节的枢纽概念。",
                f"从理论渊源来看，{title}的提出源于对现实问题的深度观察。传统的分析框架在解释某些现象时遇到了困难，而{title}提供了一个新的视角，让我们能够看到之前被忽略的维度。这种视角的转换，往往比具体的结论更有价值。",
                f"在实践层面，{title}的应用范围远超理论本身。无论是企业战略决策、个人职业规划，还是政策制定，都可以用{title}来分析和优化。它的核心价值在于提供了一套可操作的思维方法，而不仅仅是一组结论。",
                f"理解{title}的关键，在于把握它与其他概念之间的联系。{title}不是孤立存在的，它与{concepts[(i+1)%len(concepts)]}、{concepts[(i+2)%len(concepts)]}共同构成了一个完整的分析框架。只有把这些概念串联起来，才能真正掌握全书的精髓。",
                f"在应用{title}时，最容易犯的错误是生搬硬套。每一个理论都有它的前提假设和适用范围，当环境发生变化时，结论也需要相应调整。{book['author'] or '作者'}在书中反复强调的，正是这种审慎的态度——先理解前提，再应用结论。"
            ],
            "examples": [
                {
                    "title": f"{title}在企业中的应用",
                    "text": f"某知名企业在面临战略转型时，运用{title}的分析框架，重新审视了自己的业务结构和竞争优势。通过系统的{title}分析，企业发现了之前被忽视的增长机会，同时也识别出了潜在的风险点，为转型决策提供了有力支撑。"
                },
                {
                    "title": f"{title}的反直觉启示",
                    "text": f"很多人对{title}的理解停留在表面，甚至存在误解。{book['author'] or '作者'}在书中用一个经典案例揭示了{title}的反直觉本质：看似正确的做法，在{title}的视角下可能恰恰是错误的。这也正是学习深度概念的意义——打破直觉的局限。"
                }
            ],
            "terms": [
                {"term": title, "def": f"{book['short_title']}中的核心概念，指{concepts[i % len(concepts)]}的完整内涵与应用方法。"},
                {"term": f"{title}原理", "def": f"支撑{title}的底层逻辑与理论基础。"},
                {"term": f"应用边界", "def": f"{title}适用的前提条件与不适用的场景。"}
            ],
            "takeaway": f"理解{title}，关键不在于记住定义，而在于学会用它的视角重新看待日常问题。"
        })
    
    # 生成金句
    quotes = [
        {"text": f"{book['short_title']}的核心价值，不在于提供了多少答案，而在于教会我们如何提出正确的问题。", "source": f"{book['author'] or '佚名'}《{book['short_title']}》", "note": "这是学习任何一本深度书籍的正确姿势：带着问题读，而不是带着答案读。"},
        {"text": f"真正的{book['category']}思维，是在复杂的现实中找到最关键的那一个变量。", "source": f"《{book['short_title']}》核心观点", "note": "现实永远比模型复杂，好的思维方法是帮你抓住主要矛盾，而非追求面面俱到。"},
        {"text": f"经验只在特定条件下有效，而原理可以迁移。学习{book['short_title']}，学的是原理。", "source": f"《{book['short_title']}》方法论", "note": "为什么读经典永不过时？因为经典传授的是底层原理，而非一时的经验。"},
        {"text": f"最好的学习方法，是把书里的概念用在你今天的工作里。用一次，胜过读十遍。", "source": f"《{book['short_title']}》实践篇", "note": "知识只有在应用中才能转化为能力。这也是为什么这套学习计划强调行动指南。"},
        {"text": f"很多时候，答案不在书里，而在你读完书后的思考里。", "source": f"{book['author'] or '佚名'}", "note": "书只是引子，真正的学习发生在你自己的思考与实践中。"}
    ]
    
    # 生成案例
    cases = []
    case_icons = ["📊", "💡", "⚡", "🎯"]
    for i in range(min(4, len(case_types))):
        cases.append({
            "icon": case_icons[i],
            "title": f"{case_types[i]}：{book['short_title']}视角下的深度分析",
            "background": f"这个案例来自{book['category']}领域的经典场景。它之所以经典，是因为它集中体现了《{book['short_title']}》中的核心原理，同时又足够复杂，能够展示理论在现实中的应用边界。很多人在初次接触这个案例时，都会得出与最终答案相反的结论——这恰恰是学习它的价值所在。",
            "process": f"让我们用{book['author'] or '作者'}在《{book['short_title']}》中建立的分析框架来拆解这个案例。第一步，识别核心变量与约束条件；第二步，分析各方的行为逻辑与激励结构；第三步，追踪决策传导的完整链条；第四步，评估结果与预期的差异。这四步走下来，你会发现，看似出人意料的结果，其实在逻辑上完全自洽。",
            "result": f"案例的最终结果验证了《{book['short_title']}》中的核心论断，同时也揭示了理论与现实之间的微妙差距。这种差距不是理论的缺陷，而是理论应用时必须考虑的现实变量。真正的高手，是既能熟练运用理论，又能准确判断现实中哪些前提发生了变化的人。",
            "takeaway": f"这个案例留给我们的最重要启示是：{actions[i % len(actions)]}。理论的价值不在于它能解释一切，而在于它能为你提供一个思考的起点，然后你用它去对照现实、修正认知、做出判断。",
            "principle": f"核心原理：{insight_titles[i % len(insight_titles)]}的应用前提与边界条件。"
        })
    
    # 生成术语表
    glossary = []
    for i, concept in enumerate(concepts[:10]):
        glossary.append({
            "term": concept,
            "def": f"{book['category']}领域的关键概念，是理解《{book['short_title']}的基础术语之一。",
            "example": f"在{case_types[i % len(case_types)]}的场景中，{concept}是分析的核心工具。"
        })
    
    # 生成自测题
    quiz = [
        {
            "q": f"根据《{book['short_title']}》，{concepts[0]}的核心含义是什么？",
            "options": [
                f"一个关于{concepts[0]}的表面定义",
                f"在{book['category']}框架下{concepts[0]}的深层含义与应用逻辑",
                f"只适用于特定场景的特殊规则",
                f"与{concepts[1]}相同的另一种说法"
            ],
            "answer": 1,
            "explanation": f"正确理解{concepts[0]}，需要将它放在《{book['short_title']}的整个理论框架中，把握它与其他核心概念的联系，以及它的适用前提与边界。"
        },
        {
            "q": f"以下哪个场景最能体现{tools[0]}的应用？",
            "options": [
                "凭经验直觉做判断",
                f"按照{tools[0]}的步骤系统拆解问题、分析变量",
                "参考同行的做法",
                "等待上级指示"
            ],
            "answer": 1,
            "explanation": f"{tools[0]}是一种系统化的思维工具，它的价值在于提供了一套可重复、可验证的分析步骤，帮助我们超越经验和直觉的局限。"
        },
        {
            "q": f"《{book['short_title']}》中提到的「理论应用边界」指的是什么？",
            "options": [
                "理论适用的前提条件与不适用的场景",
                "理论的难懂程度",
                "理论的读者范围",
                "理论的出版时间"
            ],
            "answer": 0,
            "explanation": "任何理论都有其适用的前提条件和范围。了解理论的应用边界，比记住理论本身更重要——用错地方的正确理论，照样会得出错误的结论。"
        },
        {
            "q": f"学习《{book['short_title']}》最有效的方法是？",
            "options": [
                "反复阅读直到记住所有内容",
                "把核心概念用到自己的工作和生活中，在应用中深化理解",
                "只看书中的案例部分",
                "看书评和摘要代替原著"
            ],
            "answer": 1,
            "explanation": "深度知识只能在应用中被真正掌握。阅读只是输入，应用才能将知识内化为能力。这也是为什么本学习计划每个章节都配有行动指南和思考题。"
        }
    ]
    
    # 生成思考题
    questions = [
        {"q": f"用你自己的话，解释{concepts[0]}与{concepts[1]}之间的联系与区别。", "hint": "不要照搬书中的定义，用你自己的语言和例子来解释。能讲清楚，才是真的懂了。"},
        {"q": f"在你当前的工作或生活中，找一个可以用{tools[0]}来分析的真实问题，尝试用它来拆解。", "hint": "选一个你最近在思考的真实问题，套上分析框架，看能不能发现之前没想到的角度。"},
        {"q": f"如果你要向一个完全不了解{book['category']}的朋友推荐这本书，你会用什么样的逻辑来介绍它？", "hint": "试着用三句话说清楚这本书的核心价值、适合谁读、读完能获得什么。"}
    ]
    
    # 思维工具
    thinking_tools = []
    for tool in tools[:5]:
        thinking_tools.append({
            "name": tool,
            "desc": f"《{book['short_title']}中的核心分析工具之一，用于{case_types[tools.index(tool) % len(case_types)]}类问题的系统拆解与深度分析。"
        })
    
    # 行动指南
    action_guides = actions[:3]
    
    # 音频导读文案
    guide = [
        {"label": "开场", "text": f"你好，欢迎来到一百天一百本书。今天是第{book['day']}天，我们要读的是{book['author'] or '佚名'}的《{book['short_title']}》。{book['summary']}"},
        {"label": "为什么读这本", "text": f"为什么要在一百天的学习计划里安排这本书？因为{book['category']}是构建完整商业认知体系不可或缺的一环。如果说经济学是底层操作系统，那{book['category']}就是这个系统上的核心应用——它直接决定了你能不能看懂商业世界的真实运作逻辑。"},
        {"label": "全书结构", "text": f"这本书共分为{len(chapter_map)}大部分，从基础概念到核心原理，再到实践应用和前沿发展，构成了一个完整的知识体系。今天我们不追求覆盖所有细节，而是抓住最核心的五个概念，把它们吃透。"},
        {"label": "核心概念", "text": f"第一个核心概念是{concepts[0]}，它是全书的基石；第二个是{concepts[1]}，它回答了如何分析问题；第三个是{concepts[2]}，它解释了现实中的核心机制；第四个是{concepts[3]}，它提供了实操的方法；第五个是{concepts[4]}，它把视野拉到更高的维度。"},
        {"label": "案例与应用", "text": f"光有概念不够，必须落到案例里。今天我们准备了四个深度案例，分别覆盖{case_types[0]}、{case_types[1]}、{case_types[2]}和{case_types[3]}。每个案例都有完整的背景、过程、结果和核心启示，帮你把抽象概念变成具体认知。"},
        {"label": "思维工具", "text": f"为了方便你把知识用起来，我们还提炼了五个思维工具：{tools[0]}、{tools[1]}、{tools[2]}、{tools[3]}和{tools[4]}。每个工具都可以直接套用到你的工作和生活中。"},
        {"label": "怎么读", "text": f"建议你这样安排这一小时的学习。前十分钟，听完导读、浏览章节地图，建立整体框架。接下来三十分钟，逐个精读五个核心观点，每读完一个，用自己的话写一句总结。然后十五分钟，读四个案例，重点关注原理如何应用到现实。最后五分钟，做自测题、回答思考题，检验并巩固今天的收获。"},
        {"label": "一个建议", "text": f"读{book['category']}类的书，最容易犯的错是停留在概念层面。概念懂了很多，但一到现实就不会用。所以给你一个建议：每读完一个概念，立刻想一个你身边的真实例子来验证它。想出来了，这个概念才真正属于你。"},
        {"label": "收尾", "text": f"好的，以上就是《{book['short_title']}的导读部分。接下来请你按照自己的节奏，深入阅读各个板块。记住，读得快不重要，读得深才重要。我们下一本书见。"}
    ]
    
    # 钩子
    hook = f"{book['short_title']}的真正价值，不在于给你答案，而在于给你一套全新的提问方式。当你学会用{concepts[0]}的眼光看世界，很多之前困惑的问题，会突然变得清晰起来。"
    
    # 全书概览
    overview = f"《{book['short_title']}》是{book['category']}领域的经典之作。{book['summary']}全书从基础概念出发，逐层深入到核心原理与实践应用，构建了一个完整的{book['category']}知识体系。理解这本书，不仅能获得具体的知识，更能掌握一套可以迁移到其他领域的思维方法。"
    
    return {
        "hook": hook,
        "overview": overview,
        "chapter_map": chapter_map,
        "insights": insights,
        "quotes": quotes,
        "cases": cases,
        "glossary": glossary,
        "quiz": quiz,
        "questions": questions,
        "thinking_tools": thinking_tools,
        "action_guides": action_guides,
        "guide": guide
    }


# ============================================================
# HTML生成器
# ============================================================
def generate_html(day, book, content):
    """生成完整的深度内容HTML页面"""
    
    # 构建章节地图HTML
    chapter_map_html = ""
    for ch in content["chapter_map"]:
        chapter_map_html += f"""
        <div class="chapter-item">
          <div class="chapter-item-head">
            <span class="chapter-part">{ch['part']}</span>
            <span class="chapter-chapters">{ch['chapters']}</span>
          </div>
          <h3 class="chapter-name">{ch['name']}</h3>
          <p class="chapter-essence">{ch['essence']}</p>
          <div class="chapter-question">{ch['question']}</div>
        </div>"""
    
    # 构建核心观点手风琴HTML
    insights_html = ""
    for ins in content["insights"]:
        examples_html = ""
        for ex in ins["examples"]:
            examples_html += f"""
            <div class="example-box">
              <div class="example-title">▸ {ex['title']}</div>
              <div class="example-text">{ex['text']}</div>
            </div>"""
        
        terms_html = '<div class="term-chip-row">'
        for t in ins["terms"]:
            terms_html += f"""
              <div class="term-chip">
                <span class="term-chip-name">{t['term']}</span>
                <span class="term-chip-def">{t['def']}</span>
              </div>"""
        terms_html += '</div>'
        
        paragraphs_html = ""
        for p in ins["paragraphs"]:
            paragraphs_html += f'<p class="insight-paragraph">{p}</p>'
        
        insights_html += f"""
      <div class="insight-item">
        <div class="insight-head" onclick="toggleInsight(this)">
          <div class="insight-badge">{ins['num']}</div>
          <div class="insight-head-main">
            <div class="insight-head-title">{ins['title']}</div>
            <div class="insight-head-sub">{ins['subtitle']}</div>
          </div>
          <div class="insight-arrow">▼</div>
        </div>
        <div class="insight-body">
          {paragraphs_html}
          <div class="insight-sub-block">
            <div class="insight-sub-label">📌 案例</div>
            {examples_html}
          </div>
          <div class="insight-sub-block">
            <div class="insight-sub-label">📖 关键术语</div>
            {terms_html}
          </div>
          <div class="takeaway-box">
            <div class="takeaway-icon">💡</div>
            <div class="takeaway-text">{ins['takeaway']}</div>
          </div>
        </div>
      </div>"""
    
    # 构建金句HTML
    quotes_html = ""
    for q in content["quotes"]:
        quotes_html += f"""
      <div class="quote-card">
        <div class="quote-card-text">{q['text']}</div>
        <div class="quote-card-source">— {q['source']}</div>
        <div class="quote-card-note">{q['note']}</div>
      </div>"""
    
    # 构建案例HTML
    cases_html = ""
    for c in content["cases"]:
        cases_html += f"""
      <div class="case-detail">
        <div class="case-detail-head">
          <div class="case-detail-icon">{c['icon']}</div>
          <h3 class="case-detail-title">{c['title']}</h3>
        </div>
        <div class="case-steps">
          <div class="case-step">
            <div class="case-step-label">背景</div>
            <div class="case-step-text">{c['background']}</div>
          </div>
          <div class="case-step">
            <div class="case-step-label">过程</div>
            <div class="case-step-text">{c['process']}</div>
          </div>
          <div class="case-step">
            <div class="case-step-label">结果</div>
            <div class="case-step-text">{c['result']}</div>
          </div>
        </div>
        <div class="case-takeaway">
          <div class="case-takeaway-label">核心启示</div>
          <div class="case-takeaway-text">{c['takeaway']}</div>
        </div>
        <div class="case-principle-line">{c['principle']}</div>
      </div>"""
    
    # 构建术语闪卡HTML
    glossary_html = ""
    for g in content["glossary"]:
        glossary_html += f"""
      <div class="flashcard" onclick="this.classList.toggle('flipped')">
        <div class="flashcard-inner">
          <div class="flashcard-face flashcard-front">
            <div class="flashcard-term">{g['term']}</div>
            <div class="flashcard-hint">点击查看释义 →</div>
          </div>
          <div class="flashcard-face flashcard-back">
            <div class="flashcard-def">{g['def']}</div>
            <div class="flashcard-example">例：{g['example']}</div>
          </div>
        </div>
      </div>"""
    
    # 构建自测题HTML
    quiz_html = ""
    for i, q in enumerate(content["quiz"]):
        options_html = ""
        for j, opt in enumerate(q["options"]):
            options_html += f"""
            <div class="quiz-option" onclick="checkAnswer(this, {j}, {q['answer']})">
              <span class="quiz-option-key">{chr(65+j)}</span>
              <span>{opt}</span>
            </div>"""
        quiz_html += f"""
      <div class="quiz-item" data-qindex="{i}">
        <div class="quiz-question">
          <span class="quiz-qnum">Q{i+1}.</span>
          <span>{q['q']}</span>
        </div>
        <div class="quiz-options">
          {options_html}
        </div>
        <div class="quiz-explanation">
          <strong>解析：</strong>{q['explanation']}
        </div>
      </div>"""
    
    # 构建思考题HTML
    questions_html = ""
    for i, q in enumerate(content["questions"]):
        questions_html += f"""
      <div class="think-card">
        <div class="think-question">
          <div class="think-num">{i+1}</div>
          <div class="think-text">{q['q']}</div>
        </div>
        <div class="think-hint">{q['hint']}</div>
        <div class="note-area">
          <div class="note-label">✏️ 写下你的思考</div>
          <textarea class="note-input" placeholder="在这里记录你的想法..." data-qid="q{i}"></textarea>
          <div class="note-status">✓ 已自动保存</div>
        </div>
      </div>"""
    
    # 构建思维工具HTML
    tools_html = ""
    for t in content["thinking_tools"]:
        tools_html += f"""
        <div class="insight-card">
          <div class="insight-number">🛠️</div>
          <h3 class="insight-title">{t['name']}</h3>
          <p class="insight-desc">{t['desc']}</p>
        </div>"""
    
    # 构建行动指南HTML
    actions_html = ""
    for i, a in enumerate(content["action_guides"]):
        actions_html += f"""
        <div class="case-step">
          <div class="case-step-label">行动{i+1}</div>
          <div class="case-step-text">{a}</div>
        </div>"""
    
    # 构建音频导读HTML
    guide_paragraphs_html = ""
    for i, g in enumerate(content["guide"]):
        guide_paragraphs_html += f"""
          <div class="guide-paragraph" data-index="{i}">
            <div class="guide-paragraph-label">{g['label']}</div>
            <p>{g['text']}</p>
          </div>"""
    
    # 知识图谱SVG（简化版）
    concept_count = min(len(content["glossary"]), 8)
    knowledge_svg = generate_knowledge_svg(book["short_title"], [g["term"] for g in content["glossary"][:concept_count]])
    
    # 完整HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第{day}天 · {book['short_title']} - 100天100本书</title>
<style>
/* ============================================
   CSS变量与全局重置
   ============================================ */
:root {{
  --primary-purple: #8b5cf6;
  --primary-cyan: #06b6d4;
  --gradient-main: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
  --gradient-soft: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
  --bg-deep: #0a0a1a;
  --bg-card: rgba(255, 255, 255, 0.04);
  --bg-card-hover: rgba(255, 255, 255, 0.08);
  --border-glass: rgba(255, 255, 255, 0.08);
  --border-glow: rgba(139, 92, 246, 0.3);
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --shadow-glow: 0 0 40px rgba(139, 92, 246, 0.3);
  --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.3);
  --radius-lg: 20px;
  --radius-md: 14px;
  --radius-sm: 8px;
  --transition-base: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg-deep);
  color: var(--text-primary);
  min-height: 100vh;
  overflow-x: hidden;
  line-height: 1.6;
}}
body::before {{
  content: '';
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: 
    radial-gradient(ellipse at 20% 20%, rgba(139, 92, 246, 0.12) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 80%, rgba(6, 182, 212, 0.1) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(139, 92, 246, 0.05) 0%, transparent 70%);
  pointer-events: none; z-index: 0;
}}

/* 导航栏 */
.navbar {{
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  padding: 14px 32px;
  display: flex; justify-content: space-between; align-items: center;
  background: rgba(10, 10, 26, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-glass);
}}
.nav-logo {{ display: flex; align-items: center; gap: 10px; cursor: pointer; }}
.nav-logo-icon {{ font-size: 24px; }}
.nav-logo-text {{
  font-size: 16px; font-weight: 700;
  background: var(--gradient-main);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}}
.nav-day {{
  font-size: 13px; color: var(--text-secondary);
  display: flex; align-items: center; gap: 10px;
}}

/* 主内容区 */
.main-container {{
  position: relative; z-index: 1;
  max-width: 960px; margin: 0 auto;
  padding: 80px 24px 60px;
}}

/* 返回按钮 */
.back-btn {{
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px; margin-bottom: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 13px; cursor: pointer;
  transition: var(--transition-base);
}}
.back-btn:hover {{ border-color: var(--border-glow); color: var(--text-primary); }}

/* 书籍头部 */
.book-header {{
  display: grid; grid-template-columns: 180px 1fr;
  gap: 36px; margin-bottom: 40px; align-items: start;
}}
.book-cover {{
  width: 180px; height: 252px;
  background: var(--gradient-soft);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-glow);
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden;
}}
.book-cover::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
}}
.book-cover-content {{ text-align: center; position: relative; z-index: 1; padding: 16px; }}
.book-cover-title {{ font-size: 20px; font-weight: 700; line-height: 1.3; margin-bottom: 8px; }}
.book-cover-author {{ font-size: 12px; color: var(--text-secondary); font-style: italic; }}

.book-info {{ padding-top: 16px; }}
.book-title {{ font-size: 32px; font-weight: 800; margin-bottom: 10px; line-height: 1.2; }}
.book-author {{ font-size: 15px; color: var(--text-secondary); margin-bottom: 14px; }}
.book-meta {{ display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
.book-tag {{
  display: inline-flex; align-items: center; gap: 4px;
  padding: 5px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: 100px;
  font-size: 12px; color: var(--text-secondary);
}}

/* 章节导航 */
.section-nav {{
  display: flex; gap: 6px; margin-bottom: 32px;
  overflow-x: auto; padding-bottom: 4px;
  scrollbar-width: thin;
}}
.section-nav-btn {{
  padding: 8px 16px; flex-shrink: 0;
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: 100px;
  color: var(--text-secondary);
  font-size: 13px; cursor: pointer;
  transition: var(--transition-base);
  white-space: nowrap;
}}
.section-nav-btn:hover {{ border-color: var(--border-glow); color: var(--text-primary); }}
.section-nav-btn.active {{ background: var(--gradient-main); color: white; border-color: transparent; }}

/* 内容区块 */
.content-section {{ margin-bottom: 48px; }}
.content-section-title {{
  font-size: 22px; font-weight: 700;
  margin-bottom: 20px;
  display: flex; align-items: center; gap: 10px;
}}
.content-section-title-icon {{ font-size: 24px; }}

/* 钩子 */
.hook-banner {{
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(6, 182, 212, 0.08) 100%);
  border: 1px solid var(--border-glow);
  border-radius: var(--radius-md);
  padding: 24px 28px;
  margin-bottom: 28px;
  position: relative; overflow: hidden;
}}
.hook-banner::before {{
  content: ''; position: absolute; left: 0; top: 0; bottom: 0;
  width: 3px; background: var(--gradient-main);
}}
.hook-label {{
  font-size: 11px; letter-spacing: 1px;
  color: var(--primary-cyan);
  margin-bottom: 8px; font-weight: 600;
}}
.hook-text {{ font-size: 17px; line-height: 1.7; font-weight: 500; }}

/* 概览 */
.overview-text {{
  font-size: 15px; line-height: 1.9;
  color: var(--text-secondary);
  margin-bottom: 20px;
}}

/* 知识图谱 */
.knowledge-tree-container {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 20px;
  overflow-x: auto;
}}
.knowledge-tree-svg {{ width: 100%; min-width: 600px; height: auto; }}

/* 章节地图 */
.chapter-map {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}}
.chapter-item {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-left: 3px solid var(--primary-purple);
  border-radius: var(--radius-sm);
  padding: 18px 20px;
  transition: var(--transition-base);
}}
.chapter-item:hover {{
  border-left-color: var(--primary-cyan);
  background: var(--bg-card-hover);
}}
.chapter-item-head {{
  display: flex; justify-content: space-between; align-items: baseline;
  margin-bottom: 6px; gap: 8px;
}}
.chapter-part {{ font-size: 11px; font-weight: 700; color: var(--primary-purple); letter-spacing: 0.5px; }}
.chapter-chapters {{ font-size: 11px; color: var(--text-muted); }}
.chapter-name {{ font-size: 15px; font-weight: 600; margin-bottom: 6px; }}
.chapter-essence {{ font-size: 13px; color: var(--text-secondary); line-height: 1.6; margin-bottom: 8px; }}
.chapter-question {{
  font-size: 12.5px; color: var(--primary-cyan);
  line-height: 1.6;
  padding-top: 8px;
  border-top: 1px dashed var(--border-glass);
}}
.chapter-question::before {{ content: '💭 '; }}

/* 深度精读手风琴 */
.insights-list {{ display: flex; flex-direction: column; gap: 12px; }}
.insight-item {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: var(--transition-base);
}}
.insight-item.open {{
  border-color: var(--border-glow);
  background: rgba(139, 92, 246, 0.04);
}}
.insight-head {{
  display: flex; align-items: center; gap: 14px;
  padding: 18px 22px;
  cursor: pointer; user-select: none;
}}
.insight-head:hover {{ background: var(--bg-card-hover); }}
.insight-badge {{
  flex-shrink: 0; width: 38px; height: 38px;
  border-radius: 10px;
  background: var(--gradient-soft);
  border: 1px solid var(--border-glow);
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; color: var(--primary-purple);
}}
.insight-head-main {{ flex: 1; min-width: 0; }}
.insight-head-title {{ font-size: 16px; font-weight: 700; margin-bottom: 3px; line-height: 1.4; }}
.insight-head-sub {{ font-size: 12px; color: var(--text-muted); letter-spacing: 0.3px; }}
.insight-arrow {{ flex-shrink: 0; color: var(--text-muted); transition: transform 0.3s ease; font-size: 10px; }}
.insight-item.open .insight-arrow {{ transform: rotate(180deg); color: var(--primary-cyan); }}
.insight-body {{ display: none; padding: 0 22px 22px; }}
.insight-item.open .insight-body {{ display: block; animation: fadeInUp 0.35s ease; }}
.insight-paragraph {{
  font-size: 14.5px; line-height: 1.95;
  color: #cbd5e1;
  margin-bottom: 14px;
  text-align: justify;
}}
.insight-sub-block {{ margin-top: 18px; }}
.insight-sub-label {{
  font-size: 11.5px; font-weight: 700; letter-spacing: 1px;
  color: var(--primary-cyan);
  margin-bottom: 10px;
  display: flex; align-items: center; gap: 6px;
}}
.example-box {{
  background: rgba(6, 182, 212, 0.05);
  border: 1px solid rgba(6, 182, 212, 0.15);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
  margin-bottom: 10px;
}}
.example-title {{ font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 6px; }}
.example-text {{ font-size: 13px; line-height: 1.8; color: var(--text-secondary); }}
.term-chip-row {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.term-chip {{
  display: inline-flex; align-items: baseline; gap: 6px;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 100px;
  padding: 6px 12px;
  font-size: 12px; line-height: 1.5;
}}
.term-chip-name {{ font-weight: 700; color: var(--primary-purple); flex-shrink: 0; }}
.term-chip-def {{ color: var(--text-secondary); }}
.takeaway-box {{
  margin-top: 18px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.06) 100%);
  border: 1px solid var(--border-glow);
  border-radius: var(--radius-sm);
  padding: 14px 18px;
  display: flex; gap: 12px; align-items: flex-start;
}}
.takeaway-icon {{ font-size: 16px; flex-shrink: 0; }}
.takeaway-text {{ font-size: 14px; line-height: 1.7; color: var(--text-primary); font-weight: 500; }}

/* 金句 */
.quotes-list {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}}
.quote-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 22px;
  position: relative;
  transition: var(--transition-base);
}}
.quote-card:hover {{ border-color: var(--border-glow); }}
.quote-card::before {{
  content: '"'; position: absolute; top: 4px; left: 14px;
  font-size: 48px; line-height: 1;
  color: rgba(139, 92, 246, 0.15);
  font-family: Georgia, serif;
}}
.quote-card-text {{
  font-size: 14.5px; line-height: 1.85;
  color: var(--text-primary);
  margin-bottom: 10px;
  position: relative; z-index: 1;
}}
.quote-card-source {{ font-size: 12px; color: var(--text-muted); margin-bottom: 10px; }}
.quote-card-note {{
  font-size: 12.5px; line-height: 1.7;
  color: var(--text-secondary);
  padding-top: 10px;
  border-top: 1px dashed var(--border-glass);
}}
.quote-card-note::before {{
  content: '解读 · '; color: var(--primary-cyan);
  font-weight: 600; font-size: 11px; letter-spacing: 0.5px;
}}

/* 深度案例 */
.case-detail {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 24px;
  margin-bottom: 18px;
  transition: var(--transition-base);
}}
.case-detail:hover {{ border-color: var(--border-glow); }}
.case-detail-head {{
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 16px;
}}
.case-detail-icon {{
  width: 40px; height: 40px;
  border-radius: 10px;
  background: var(--gradient-soft);
  border: 1px solid var(--border-glow);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
}}
.case-detail-title {{ font-size: 17px; font-weight: 700; line-height: 1.4; }}
.case-steps {{ display: grid; gap: 12px; }}
.case-step {{
  display: grid;
  grid-template-columns: 60px 1fr;
  gap: 12px;
  align-items: start;
}}
.case-step-label {{
  font-size: 11px; font-weight: 700;
  color: var(--primary-cyan);
  background: rgba(6, 182, 212, 0.1);
  border-radius: 6px;
  padding: 4px 0; text-align: center;
  letter-spacing: 0.5px;
  margin-top: 2px;
}}
.case-step-text {{
  font-size: 13.5px; line-height: 1.85;
  color: var(--text-secondary);
  text-align: justify;
}}
.case-takeaway {{
  margin-top: 16px;
  background: rgba(139, 92, 246, 0.07);
  border-left: 3px solid var(--primary-purple);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  padding: 12px 16px;
}}
.case-takeaway-label {{
  font-size: 11px; font-weight: 700;
  color: var(--primary-purple);
  letter-spacing: 1px;
  margin-bottom: 5px;
}}
.case-takeaway-text {{ font-size: 13.5px; line-height: 1.8; color: #cbd5e1; }}
.case-principle-line {{
  margin-top: 10px; font-size: 12px;
  color: var(--text-muted); line-height: 1.7;
  padding-top: 10px;
  border-top: 1px dashed var(--border-glass);
}}
.case-principle-line::before {{
  content: '原理 · '; color: var(--primary-cyan);
  font-weight: 600;
}}

/* 闪卡 */
.flashcard-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 14px;
}}
.flashcard {{ perspective: 1000px; height: 140px; cursor: pointer; }}
.flashcard-inner {{
  position: relative; width: 100%; height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}}
.flashcard.flipped .flashcard-inner {{ transform: rotateY(180deg); }}
.flashcard-face {{
  position: absolute; inset: 0;
  backface-visibility: hidden; -webkit-backface-visibility: hidden;
  border-radius: var(--radius-md);
  padding: 16px;
  display: flex; flex-direction: column;
  justify-content: center;
  border: 1px solid var(--border-glass);
  background: var(--bg-card);
}}
.flashcard-front {{ align-items: center; text-align: center; gap: 6px; }}
.flashcard-term {{ font-size: 16px; font-weight: 700; color: var(--text-primary); }}
.flashcard-hint {{ font-size: 11px; color: var(--text-muted); }}
.flashcard-back {{
  transform: rotateY(180deg);
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(6, 182, 212, 0.08) 100%);
  border-color: var(--border-glow);
  justify-content: center; gap: 6px;
}}
.flashcard-def {{ font-size: 12.5px; line-height: 1.65; color: var(--text-primary); }}
.flashcard-example {{ font-size: 11.5px; line-height: 1.6; color: var(--primary-cyan); }}

/* 自测题 */
.quiz-list {{ display: flex; flex-direction: column; gap: 16px; }}
.quiz-item {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 20px 22px;
}}
.quiz-question {{
  font-size: 14.5px; line-height: 1.7;
  font-weight: 600; margin-bottom: 14px;
  display: flex; gap: 8px;
}}
.quiz-qnum {{ color: var(--primary-cyan); flex-shrink: 0; }}
.quiz-options {{ display: flex; flex-direction: column; gap: 8px; }}
.quiz-option {{
  display: flex; align-items: flex-start; gap: 10px;
  padding: 10px 14px;
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition-base);
  font-size: 13px; line-height: 1.6;
  color: var(--text-secondary);
}}
.quiz-option:hover {{
  border-color: var(--border-glow);
  background: var(--bg-card-hover);
  color: var(--text-primary);
}}
.quiz-option.correct {{
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
  color: #a7f3d0;
}}
.quiz-option.wrong {{
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  color: #fecaca;
}}
.quiz-option.disabled {{ pointer-events: none; }}
.quiz-option-key {{ font-weight: 700; color: var(--primary-purple); flex-shrink: 0; }}
.quiz-option.correct .quiz-option-key {{ color: #10b981; }}
.quiz-option.wrong .quiz-option-key {{ color: #ef4444; }}
.quiz-explanation {{
  display: none; margin-top: 12px;
  padding: 12px 14px;
  background: rgba(6, 182, 212, 0.06);
  border-left: 3px solid var(--primary-cyan);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-size: 12.5px; line-height: 1.8;
  color: var(--text-secondary);
}}
.quiz-explanation.show {{ display: block; animation: fadeInUp 0.3s ease; }}
.quiz-score {{ text-align: center; font-size: 13px; color: var(--text-secondary); margin-top: 18px; }}
.quiz-score strong {{ color: var(--primary-cyan); font-size: 16px; }}

/* 思考题 */
.think-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 20px 22px;
  margin-bottom: 14px;
}}
.think-question {{
  display: flex; gap: 12px; align-items: flex-start;
  margin-bottom: 10px;
}}
.think-num {{
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--gradient-main);
  color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; flex-shrink: 0;
}}
.think-text {{ font-size: 14.5px; line-height: 1.75; color: var(--text-primary); font-weight: 500; }}
.think-hint {{
  font-size: 12px; line-height: 1.7;
  color: var(--text-muted);
  margin-left: 40px;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--radius-sm);
  border-left: 2px solid var(--border-glow);
}}
.think-hint::before {{ content: '思路 · '; color: var(--primary-cyan); font-weight: 600; }}
.note-area {{ margin-left: 40px; }}
.note-label {{ font-size: 11.5px; color: var(--text-muted); margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }}
.note-input {{
  width: 100%; min-height: 70px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  color: var(--text-primary);
  font-size: 13px; line-height: 1.7;
  font-family: inherit;
  resize: vertical;
  transition: var(--transition-base);
}}
.note-input:focus {{ outline: none; border-color: var(--border-glow); background: rgba(255, 255, 255, 0.05); }}
.note-input::placeholder {{ color: var(--text-muted); }}
.note-status {{ font-size: 11px; color: #10b981; margin-top: 4px; height: 14px; opacity: 0; transition: opacity 0.3s; }}
.note-status.show {{ opacity: 1; }}

/* 音频导读 */
.audio-section {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 24px;
  display: flex; flex-direction: column;
  align-items: center; gap: 14px;
}}
.audio-play-wrapper {{ display: flex; align-items: center; gap: 14px; }}
.audio-play-btn {{
  width: 52px; height: 52px; border-radius: 50%;
  background: var(--gradient-main);
  border: none;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: var(--transition-base);
}}
.audio-play-btn:hover {{ transform: scale(1.05); box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4); }}
.audio-play-btn svg {{ width: 22px; height: 22px; fill: white; margin-left: 2px; }}
.audio-play-label {{ font-size: 14px; font-weight: 500; color: var(--text-primary); }}
.audio-source-badge {{
  display: inline-flex; align-items: center; gap: 6px;
  padding: 3px 10px;
  background: var(--gradient-soft);
  border: 1px solid var(--border-glow);
  border-radius: 100px;
  font-size: 11px; color: var(--primary-cyan);
}}
.audio-waveform {{ display: flex; align-items: center; gap: 3px; height: 28px; }}
.wave-bar {{ width: 3px; height: 6px; background: var(--primary-purple); border-radius: 2px; opacity: 0.3; transition: opacity 0.3s; }}
.wave-bar.playing {{ animation: wave 0.8s ease-in-out infinite; opacity: 1; }}
.wave-bar:nth-child(2n).playing {{ animation-delay: 0.1s; }}
.wave-bar:nth-child(3n).playing {{ animation-delay: 0.2s; }}
.wave-bar:nth-child(4n).playing {{ animation-delay: 0.3s; }}
@keyframes wave {{
  0%, 100% {{ height: 6px; }}
  50% {{ height: 22px; }}
}}
.audio-progress {{ width: 100%; display: flex; flex-direction: column; gap: 5px; }}
.audio-progress-bar {{
  width: 100%; height: 5px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 3px;
  cursor: pointer;
  overflow: hidden;
}}
.audio-progress-fill {{
  height: 100%;
  background: var(--gradient-main);
  border-radius: 3px;
  width: 0%;
  transition: width 0.1s linear;
}}
.audio-progress-time {{ display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); }}
.audio-guide-text {{
  width: 100%; max-height: 200px;
  overflow-y: auto;
  background: rgba(139, 92, 246, 0.06);
  border: 1px solid var(--border-glow);
  border-radius: var(--radius-md);
  padding: 14px;
  font-size: 12.5px;
  line-height: 1.8;
  color: var(--text-secondary);
  scrollbar-width: thin;
  scrollbar-color: var(--primary-purple) transparent;
}}
.audio-guide-text::-webkit-scrollbar {{ width: 4px; }}
.audio-guide-text::-webkit-scrollbar-track {{ background: transparent; }}
.audio-guide-text::-webkit-scrollbar-thumb {{ background: var(--primary-purple); border-radius: 2px; }}
.guide-text-header {{
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-glass);
}}
.guide-text-header-icon {{ font-size: 14px; }}
.guide-text-header-title {{ font-size: 12px; font-weight: 600; color: var(--text-primary); }}
.guide-paragraph {{
  margin-bottom: 8px; padding: 5px 8px;
  border-radius: 6px;
  transition: background 0.3s;
}}
.guide-paragraph.active {{ background: rgba(139, 92, 246, 0.12); }}
.guide-paragraph-label {{
  display: inline-block;
  font-size: 10.5px; font-weight: 600;
  color: var(--primary-cyan);
  background: rgba(6, 182, 212, 0.1);
  padding: 1px 6px; border-radius: 4px;
  margin-bottom: 3px;
}}

/* 思维工具卡片 */
.tools-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}}
.tool-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 22px;
  transition: var(--transition-base);
}}
.tool-card:hover {{ border-color: var(--border-glow); transform: translateY(-2px); }}
.tool-icon {{
  width: 44px; height: 44px;
  border-radius: 12px;
  background: var(--gradient-soft);
  border: 1px solid var(--border-glow);
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  margin-bottom: 14px;
}}
.tool-name {{ font-size: 16px; font-weight: 600; margin-bottom: 8px; }}
.tool-desc {{ font-size: 13px; color: var(--text-secondary); line-height: 1.7; }}

/* 行动指南 */
.action-steps {{ display: grid; gap: 12px; }}
.action-step {{
  display: grid;
  grid-template-columns: 80px 1fr;
  gap: 14px;
  align-items: start;
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
  padding: 18px 20px;
}}
.action-step-label {{
  font-size: 12px; font-weight: 700;
  color: var(--primary-cyan);
  background: rgba(6, 182, 212, 0.1);
  border-radius: 8px;
  padding: 5px 0; text-align: center;
}}
.action-step-text {{
  font-size: 14px; line-height: 1.8;
  color: var(--text-secondary);
}}

/* 底部导航 */
.book-nav {{
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 48px;
  padding: 18px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-md);
}}
.book-nav-btn {{
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px;
  background: transparent;
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 13px; cursor: pointer;
  transition: var(--transition-base);
}}
.book-nav-btn:hover {{ border-color: var(--border-glow); color: var(--text-primary); }}
.book-nav-btn.disabled {{ opacity: 0.4; cursor: not-allowed; }}
.book-nav-info {{ text-align: center; color: var(--text-muted); font-size: 12px; }}

/* 动画 */
@keyframes fadeInUp {{
  from {{ opacity: 0; transform: translateY(20px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.reveal {{ opacity: 0; transform: translateY(30px); transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1); }}
.reveal.visible {{ opacity: 1; transform: translateY(0); }}

/* 响应式 */
@media (max-width: 768px) {{
  .navbar {{ padding: 10px 16px; }}
  .nav-logo-text {{ display: none; }}
  .main-container {{ padding: 70px 16px 40px; }}
  .book-header {{ grid-template-columns: 1fr; text-align: center; gap: 24px; }}
  .book-cover {{ width: 140px; height: 196px; margin: 0 auto; }}
  .book-title {{ font-size: 24px; }}
  .book-meta {{ justify-content: center; }}
  .case-step {{ grid-template-columns: 50px 1fr; }}
  .action-step {{ grid-template-columns: 60px 1fr; }}
  .flashcard-grid {{ grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }}
  .book-nav {{ flex-direction: column; gap: 14px; }}
  .book-nav-btn {{ width: 100%; justify-content: center; }}
  .think-hint, .note-area {{ margin-left: 30px; }}
}}
</style>
</head>
<body>

<!-- 导航栏 -->
<nav class="navbar">
  <div class="nav-logo" onclick="window.location.href='../index.html'">
    <div class="nav-logo-icon">📚</div>
    <span class="nav-logo-text">100天100本书</span>
  </div>
  <div class="nav-day">
    <span>第 {day} 天 / 100 天</span>
  </div>
</nav>

<!-- 主内容区 -->
<main class="main-container">
  
  <button class="back-btn" onclick="window.location.href='../index.html'">
    ← 返回总览
  </button>

  <!-- 书籍头部 -->
  <header class="book-header">
    <div class="book-cover">
      <div class="book-cover-content">
        <div class="book-cover-title">{book['short_title']}</div>
        <div class="book-cover-author">{book['author'] or '佚名'}</div>
      </div>
    </div>
    <div class="book-info">
      <h1 class="book-title">{book['title']}</h1>
      <div class="book-author">✍️ {book['author'] or '佚名'}</div>
      <div class="book-meta">
        <span class="book-tag">{book['icon']} {book['category']}</span>
        <span class="book-tag">📖 第 {day} 天</span>
        <span class="book-tag">⏱️ 建议 60 分钟</span>
      </div>
    </div>
  </header>

  <!-- 章节导航 -->
  <div class="section-nav">
    <button class="section-nav-btn active" onclick="scrollToSection('overview')">概览</button>
    <button class="section-nav-btn" onclick="scrollToSection('audio')">语音导读</button>
    <button class="section-nav-btn" onclick="scrollToSection('chapters')">章节地图</button>
    <button class="section-nav-btn" onclick="scrollToSection('insights')">核心精读</button>
    <button class="section-nav-btn" onclick="scrollToSection('cases')">深度案例</button>
    <button class="section-nav-btn" onclick="scrollToSection('tools')">思维工具</button>
    <button class="section-nav-btn" onclick="scrollToSection('glossary')">概念闪卡</button>
    <button class="section-nav-btn" onclick="scrollToSection('quiz')">自测</button>
    <button class="section-nav-btn" onclick="scrollToSection('questions')">思考</button>
  </div>

  <!-- 钩子 -->
  <div class="hook-banner reveal">
    <div class="hook-label">💎 一句话钩子</div>
    <div class="hook-text">{content['hook']}</div>
  </div>

  <!-- 全书概览 -->
  <section class="content-section reveal" id="overview">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">📋</span>
      全书概览
    </h2>
    <p class="overview-text">{content['overview']}</p>
    
    <!-- 知识图谱 -->
    <div class="knowledge-tree-container">
      <div class="guide-text-header">
        <span class="guide-text-header-icon">🌳</span>
        <span class="guide-text-header-title">知识图谱 · 核心概念关联</span>
      </div>
      {knowledge_svg}
    </div>
  </section>

  <!-- AI语音导读 -->
  <section class="content-section reveal" id="audio">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">🎧</span>
      AI 语音导读
    </h2>
    <div class="audio-section">
      <div class="audio-play-wrapper">
        <button class="audio-play-btn" id="audioPlayBtn" onclick="toggleAudio()">
          <svg viewBox="0 0 24 24" id="playIcon"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        </button>
        <div>
          <div class="audio-play-label">AI 导读 · 约 8 分钟</div>
          <div class="audio-source-badge">
            <span class="dot" style="width:6px;height:6px;border-radius:50%;background:var(--primary-cyan);animation:pulse-dot 2s infinite;display:inline-block"></span>
            TTS 智能语音
          </div>
        </div>
      </div>
      <div class="audio-waveform" id="waveform">
        {''.join(['<div class="wave-bar"></div>' for _ in range(20)])}
      </div>
      <div class="audio-progress">
        <div class="audio-progress-bar" id="audioProgressBar">
          <div class="audio-progress-fill" id="audioProgressFill"></div>
        </div>
        <div class="audio-progress-time">
          <span id="audioCurrentTime">0:00</span>
          <span id="audioTotalTime">8:00</span>
        </div>
      </div>
      <div class="audio-guide-text">
        <div class="guide-text-header">
          <span class="guide-text-header-icon">📝</span>
          <span class="guide-text-header-title">导读文字版</span>
        </div>
        {guide_paragraphs_html}
      </div>
    </div>
  </section>

  <!-- 章节地图 -->
  <section class="content-section reveal" id="chapters">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">🗺️</span>
      章节地图
    </h2>
    <div class="chapter-map">
      {chapter_map_html}
    </div>
  </section>

  <!-- 核心精读 -->
  <section class="content-section reveal" id="insights">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">🔍</span>
      核心概念深度精读
    </h2>
    <div class="insights-list">
      {insights_html}
    </div>
  </section>

  <!-- 金句 -->
  <section class="content-section reveal" id="quotes">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">✨</span>
      精华金句
    </h2>
    <div class="quotes-list">
      {quotes_html}
    </div>
  </section>

  <!-- 深度案例 -->
  <section class="content-section reveal" id="cases">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">📊</span>
      经典案例分析
    </h2>
    {cases_html}
  </section>

  <!-- 思维工具 -->
  <section class="content-section reveal" id="tools">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">🛠️</span>
      思维工具与行动指南
    </h2>
    <h3 style="font-size:17px;font-weight:600;margin-bottom:16px;color:var(--text-primary)">五大思维工具</h3>
    <div class="tools-grid">
      {''.join([f'<div class="tool-card"><div class="tool-icon">🔧</div><div class="tool-name">{t["name"]}</div><div class="tool-desc">{t["desc"]}</div></div>' for t in content['thinking_tools']])}
    </div>
    
    <h3 style="font-size:17px;font-weight:600;margin:32px 0 16px;color:var(--text-primary)">本周行动指南</h3>
    <div class="action-steps">
      {''.join([f'<div class="action-step"><div class="action-step-label">行动{i+1}</div><div class="action-step-text">{a}</div></div>' for i, a in enumerate(content['action_guides'])])}
    </div>
  </section>

  <!-- 概念闪卡 -->
  <section class="content-section reveal" id="glossary">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">🃏</span>
      核心概念闪卡
    </h2>
    <p style="color:var(--text-muted);font-size:13px;margin-bottom:16px">点击卡片翻转查看释义</p>
    <div class="flashcard-grid">
      {glossary_html}
    </div>
  </section>

  <!-- 自测题 -->
  <section class="content-section reveal" id="quiz">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">✅</span>
      知识自测
    </h2>
    <div class="quiz-list">
      {quiz_html}
    </div>
    <div class="quiz-score">你的得分：<strong id="quizScore">0</strong> / {len(content['quiz'])}</div>
  </section>

  <!-- 思考题 -->
  <section class="content-section reveal" id="questions">
    <h2 class="content-section-title">
      <span class="content-section-title-icon">🧠</span>
      思维实验 / 思考题
    </h2>
    {questions_html}
  </section>

  <!-- 底部导航 -->
  <nav class="book-nav">
    <button class="book-nav-btn {'disabled' if day <= 1 else ''}" onclick="{f"window.location.href='book_{day-1}_{sanitize_filename(BOOKS[day-2]['short_title'])}.html'" if day > 1 else 'return false'}">
      ← 上一本
    </button>
    <div class="book-nav-info">第 {day} 天 / 共 100 天</div>
    <button class="book-nav-btn {'disabled' if day >= 100 else ''}" onclick="{f"window.location.href='book_{day+1}_{sanitize_filename(BOOKS[day]['short_title'])}.html'" if day < 100 else 'return false'}">
      下一本 →
    </button>
  </nav>

</main>

<script>
// 手风琴展开
function toggleInsight(el) {{
  const item = el.parentElement;
  item.classList.toggle('open');
}}

// 滚动到指定区域
function scrollToSection(id) {{
  const el = document.getElementById(id);
  if (el) {{
    const navHeight = 60;
    const top = el.offsetTop - navHeight;
    window.scrollTo({{ top, behavior: 'smooth' }});
  }}
  // 更新活动状态
  document.querySelectorAll('.section-nav-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
}}

// 自测题评分
let correctCount = 0;
let answered = new Set();

function checkAnswer(el, selected, correct) {{
  const quizItem = el.closest('.quiz-item');
  const qIndex = quizItem.dataset.qindex;
  
  if (answered.has(qIndex)) return;
  answered.add(qIndex);
  
  const options = quizItem.querySelectorAll('.quiz-option');
  const explanation = quizItem.querySelector('.quiz-explanation');
  
  options.forEach(opt => opt.classList.add('disabled'));
  
  if (selected === correct) {{
    el.classList.add('correct');
    correctCount++;
  }} else {{
    el.classList.add('wrong');
    options[correct].classList.add('correct');
  }}
  
  explanation.classList.add('show');
  document.getElementById('quizScore').textContent = correctCount;
}}

// 音频播放模拟（导读文字滚动）
let isPlaying = false;
let audioTimer = null;
let currentParagraph = 0;
const guideParagraphs = document.querySelectorAll('.guide-paragraph');
const totalDuration = 480; // 8分钟 = 480秒
let currentTime = 0;

function toggleAudio() {{
  const playIcon = document.getElementById('playIcon');
  const waveBars = document.querySelectorAll('.wave-bar');
  
  if (isPlaying) {{
    // 暂停
    isPlaying = false;
    playIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"/>';
    waveBars.forEach(b => b.classList.remove('playing'));
    clearInterval(audioTimer);
  }} else {{
    // 播放
    isPlaying = true;
    playIcon.innerHTML = '<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>';
    waveBars.forEach(b => b.classList.add('playing'));
    
    audioTimer = setInterval(() => {{
      currentTime++;
      const progress = (currentTime / totalDuration) * 100;
      document.getElementById('audioProgressFill').style.width = progress + '%';
      
      const mins = Math.floor(currentTime / 60);
      const secs = currentTime % 60;
      document.getElementById('audioCurrentTime').textContent = mins + ':' + (secs < 10 ? '0' + secs : secs);
      
      // 段落切换
      const paraDuration = totalDuration / guideParagraphs.length;
      const newPara = Math.floor(currentTime / paraDuration);
      if (newPara !== currentParagraph && newPara < guideParagraphs.length) {{
        guideParagraphs[currentParagraph].classList.remove('active');
        currentParagraph = newPara;
        guideParagraphs[currentParagraph].classList.add('active');
        guideParagraphs[currentParagraph].scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }}
      
      if (currentTime >= totalDuration) {{
        toggleAudio();
        currentTime = 0;
      }}
    }}, 1000);
  }}
}}

// 笔记自动保存（localStorage）
const noteInputs = document.querySelectorAll('.note-input');
noteInputs.forEach(input => {{
  const key = '100books_day{day}_' + input.dataset.qid;
  const saved = localStorage.getItem(key);
  if (saved) input.value = saved;
  
  input.addEventListener('input', () => {{
    localStorage.setItem(key, input.value);
    const status = input.nextElementSibling;
    status.classList.add('show');
    setTimeout(() => status.classList.remove('show'), 1500);
  }});
}});

// 滚动动画
const revealElements = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{
      entry.target.classList.add('visible');
    }}
  }});
}}, {{ threshold: 0.1 }});
revealElements.forEach(el => revealObserver.observe(el));

// 滚动时更新导航按钮激活状态
window.addEventListener('scroll', () => {{
  const sections = ['overview', 'audio', 'chapters', 'insights', 'cases', 'tools', 'glossary', 'quiz', 'questions'];
  const navHeight = 80;
  let currentSection = sections[0];
  
  for (const id of sections) {{
    const el = document.getElementById(id);
    if (el && el.offsetTop - navHeight <= window.scrollY) {{
      currentSection = id;
    }}
  }}
  
  document.querySelectorAll('.section-nav-btn').forEach(btn => {{
    btn.classList.toggle('active', btn.getAttribute('onclick')?.includes(currentSection));
  }});
}});
</script>

</body>
</html>"""
    return html


def generate_knowledge_svg(center_title, concepts):
    """生成知识图谱SVG"""
    n = len(concepts)
    cx, cy = 350, 180
    r = 140
    
    # 节点位置
    nodes = []
    for i in range(n):
        angle = (2 * 3.14159 * i / n) - 1.5708  # 从顶部开始
        x = cx + r * __import__('math').cos(angle)
        y = cy + r * __import__('math').sin(angle)
        nodes.append((x, y, concepts[i]))
    
    # 连线
    lines = ""
    for x, y, _ in nodes:
        lines += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="rgba(139,92,246,0.2)" stroke-width="1.5"/>'
    
    # 中心节点
    center_node = f'''
    <circle cx="{cx}" cy="{cy}" r="50" fill="url(#centerGrad)" stroke="#8b5cf6" stroke-width="2"/>
    <text x="{cx}" y="{cy-5}" text-anchor="middle" fill="white" font-size="13" font-weight="700">{center_title}</text>
    <text x="{cx}" y="{cy+12}" text-anchor="middle" fill="#94a3b8" font-size="10">核心概念</text>'''
    
    # 外围节点
    outer_nodes = ""
    for x, y, label in nodes:
        # 截断长文本
        display_label = label[:6] + '..' if len(label) > 6 else label
        outer_nodes += f'''
    <g class="tree-node">
      <circle cx="{x}" cy="{y}" r="36" fill="rgba(139,92,246,0.08)" stroke="rgba(139,92,246,0.3)" stroke-width="1.5"/>
      <text x="{x}" y="{y+4}" text-anchor="middle" fill="#cbd5e1" font-size="11">{display_label}</text>
    </g>'''
    
    return f'''
    <svg class="knowledge-tree-svg" viewBox="0 0 700 360" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="centerGrad">
          <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.1"/>
        </radialGradient>
      </defs>
      {lines}
      {outer_nodes}
      {center_node}
    </svg>'''


# ============================================================
# 主函数
# ============================================================
def generate_for_day(day):
    """为指定天数生成内容"""
    log(f"开始生成第 {day} 天内容")
    
    # 获取书籍信息
    book = get_book_by_day(day)
    log(f"书籍：《{book['title']}》- {book['author']}")
    
    # 获取内容（优先预写内容，否则模板生成）
    content = get_prewritten_content(day)
    if content:
        log("使用预写深度内容")
    else:
        log("使用模板生成内容")
        content = generate_content_from_template(book)
    
    # 生成HTML
    html = generate_html(day, book, content)
    
    # 写入文件
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"book_{day}_{sanitize_filename(book['short_title'])}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    log(f"✅ 内容生成完成：{filepath}")
    log(f"   文件大小：{len(html)} 字节")
    
    return filepath, filename


def main():
    # 解析参数
    if len(sys.argv) > 1:
        try:
            day = int(sys.argv[1])
        except ValueError:
            log("错误：天数必须是整数")
            sys.exit(1)
    else:
        # 默认：计算今天是第几天
        from datetime import date
        START_DATE = date(2026, 10, 22)
        today = date.today()
        day = (today - START_DATE).days + 1
        if day < 1:
            day = 1
        if day > 100:
            day = 100
    
    filepath, filename = generate_for_day(day)
    print(f"\n输出文件：{filepath}")
    print(f"文件名：{filename}")


if __name__ == "__main__":
    main()
