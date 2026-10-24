# 100天100本书 · 自动化内容生成流水线

## 架构概览

```
每天 22:00 crontab 触发
    ↓
daily_main.sh（主调度）
    ├─→ generate_content.py  → books/book_N_书名.html  （深度内容网页）
    ├─→ generate_video.py    → videos/book_N_书名.mp4  （动画视频，HyperFrames）
    │                         hf_compositions/        （组合源文件）
    ├─→ upload_github.py     → GitHub Pages 部署
    └─→ daily_push.py        → 飞书群推送
```

## 文件说明

| 文件 | 功能 |
|------|------|
| `books_data.py` | 100本书单数据（8大分类）+ 工具函数 |
| `generate_content.py` | 生成每日深度内容HTML网页 |
| `generate_video.py` | 生成HyperFrames组合文件 + 渲染MP4视频 |
| `upload_github.py` | Git上传内容到GitHub Pages |
| `daily_push.py` | 飞书群消息推送 |
| `daily_main.sh` | 每日主调度脚本（串联全流程） |
| `setup_cron.sh` | crontab定时任务一键安装脚本 |
| `content.js` | 预写内容数据（前几天有深度内容） |
| `books/` | 生成的HTML内容页 |
| `hf_compositions/` | HyperFrames组合源文件 |
| `videos/` | 渲染完成的MP4视频 |
| `logs/` | 各步骤日志 |

## 每日流程时间线

- **22:00** - `daily_main.sh` 启动
- **22:00-22:05** - 内容HTML生成（约5秒）
- **22:05-22:15** - 视频渲染（约10分钟，取决于机器性能）
- **22:15-22:17** - GitHub上传（约2分钟）
- **22:17-22:18** - 飞书推送

## 手动使用

### 生成指定天数的内容
```bash
python3 generate_content.py 3    # 生成第3天内容HTML
```

### 生成指定天数的视频
```bash
python3 generate_video.py 3      # 生成第3天视频组合+渲染
```

### 上传指定天数到GitHub
```bash
python3 upload_github.py 3       # 上传第3天内容
```

### 手动推送飞书
```bash
python3 daily_push.py 3 "https://Fahning1.github.io/100books/books/book_3_xxx.html"
```

### 手动执行完整流水线
```bash
./daily_main.sh
```

## 安装定时任务

```bash
cd /path/to/100books
./setup_cron.sh
```

安装后可通过 `crontab -l` 验证。

## 视频说明

视频使用 HyperFrames 生成，结构：
1. **开场**（10秒）- 书名 + 分类 + 天数
2. **核心知识点**（50秒）- 5个核心概念动画
3. **经典案例**（30秒）- 深度案例启示
4. **总结**（15秒）- 金句 + 行动号召

总计约105秒，1280×720分辨率，30fps。

> 若HyperFrames CLI未安装，脚本会跳过视频渲染，但会生成组合文件（`hf_compositions/`），可手动渲染。

## GitHub Pages 访问地址

- 总览页：`https://Fahning1.github.io/100books/`
- 第N天内容：`https://Fahning1.github.io/100books/books/book_N_书名.html`
- 第N天视频：`https://Fahning1.github.io/100books/videos/book_N_书名.mp4`

## 内容结构（深度网页）

1. 🎧 AI语音导读
2. 📖 全书概览 + 知识图谱
3. 💡 核心概念深度卡片（可展开）
4. 📊 经典案例分析
5. 🛠️ 思维工具与行动指南
6. 🧪 思维实验/场景题
7. 📝 精华笔记

## 故障排查

### 视频渲染失败
- 检查 HyperFrames 是否安装：`npx hyperframes --version`
- 查看日志：`logs/generate_video.log`

### GitHub上传失败
- 检查网络连接
- 检查token权限：`git remote -v`
- 查看日志：`logs/upload_github.log`

### 飞书推送失败
- 检查lark-cli路径配置
- 检查chat_id是否正确
- 查看日志：`push.log`

### 定时任务不执行
- 确认cron服务运行：`crontab -l`
- 检查脚本有执行权限
- 查看cron日志：`logs/cron.log`
