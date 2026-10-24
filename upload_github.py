#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
100天100本书 · GitHub上传脚本
功能：将生成的内容文件上传到 GitHub 仓库
用法：python3 upload_github.py [day_number]

使用 git 命令行操作，返回最终访问 URL
"""

import os
import sys
import subprocess
from datetime import datetime

# ==================== 配置区 ====================
# 脚本所在目录 / 仓库根目录
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
# 日志文件
LOG_FILE = os.path.join(REPO_DIR, "logs", "upload_github.log")
# GitHub Pages 基础 URL
GITHUB_PAGES_BASE = "https://Fahning1.github.io/100books"
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


def run_git(cmd, cwd=None, timeout=120):
    """执行 git 命令"""
    if cwd is None:
        cwd = REPO_DIR
    
    full_cmd = f"git {cmd}"
    log(f"执行: {full_cmd}")
    
    try:
        result = subprocess.run(
            full_cmd, shell=True, cwd=cwd,
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0:
            log(f"  ✅ 成功")
            if result.stdout.strip():
                log(f"  输出: {result.stdout.strip()[:200]}")
            return True, result.stdout.strip()
        else:
            log(f"  ❌ 失败")
            log(f"  错误: {result.stderr.strip()[:300]}")
            return False, result.stderr.strip()
    except subprocess.TimeoutExpired:
        log(f"  ❌ 超时")
        return False, "命令执行超时"
    except Exception as e:
        log(f"  ❌ 异常: {e}")
        return False, str(e)


def check_git_status():
    """检查 git 仓库状态"""
    log("检查 Git 仓库状态...")
    
    # 检查是否在 git 仓库中
    success, output = run_git("status --short")
    if not success:
        log("❌ 当前目录不是 Git 仓库")
        return False
    
    # 检查远程仓库
    success, output = run_git("remote -v")
    if success and output:
        log(f"远程仓库配置: {output.split(chr(10))[0]}")
    else:
        log("⚠️ 未配置远程仓库")
    
    # 检查当前分支
    success, output = run_git("branch --show-current")
    if success:
        log(f"当前分支: {output}")
    
    return True


def upload_files(files, commit_message=None):
    """上传指定文件到 GitHub
    
    Args:
        files: 要上传的文件路径列表（相对于仓库根目录的路径或绝对路径）
        commit_message: 提交信息
    
    Returns:
        (success, urls) - 成功与否，以及文件的访问 URL 列表
    """
    if not files:
        log("没有要上传的文件")
        return True, []
    
    if commit_message is None:
        commit_message = f"Update content - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    log(f"准备上传 {len(files)} 个文件")
    log(f"提交信息: {commit_message}")
    
    # 将文件路径转换为相对于仓库根目录的路径
    rel_files = []
    for f in files:
        if os.path.isabs(f):
            # 绝对路径，转换为相对路径
            if f.startswith(REPO_DIR):
                rel_path = os.path.relpath(f, REPO_DIR)
            else:
                log(f"⚠️ 文件不在仓库内: {f}")
                continue
        else:
            rel_path = f
        
        # 检查文件是否存在
        abs_path = os.path.join(REPO_DIR, rel_path)
        if not os.path.exists(abs_path):
            log(f"⚠️ 文件不存在: {abs_path}")
            continue
        
        rel_files.append(rel_path)
    
    if not rel_files:
        log("❌ 没有有效的文件可上传")
        return False, []
    
    # 1. 添加文件
    add_cmd = "add " + " ".join([f"'{f}'" for f in rel_files])
    success, _ = run_git(add_cmd)
    if not success:
        log("❌ git add 失败")
        return False, []
    
    # 2. 提交
    success, _ = run_git(f"commit -m '{commit_message}'")
    if not success:
        # 可能没有变更
        log("⚠️ 没有新的变更需要提交")
        # 继续尝试 pull 和 push
    
    # 3. 拉取最新代码（避免冲突）
    log("同步远程仓库...")
    success, _ = run_git("pull --rebase origin main", timeout=60)
    if not success:
        log("⚠️ pull 失败，尝试直接 push")
    
    # 4. 推送
    log("推送到远程仓库...")
    success, output = run_git("push origin main", timeout=60)
    if not success:
        log("❌ push 失败")
        return False, []
    
    log("✅ 上传成功！")
    
    # 生成访问 URL
    urls = []
    for rel_path in rel_files:
        # GitHub Pages URL
        url = f"{GITHUB_PAGES_BASE}/{rel_path}"
        urls.append(url)
        log(f"  🌐 {url}")
    
    return True, urls


def upload_for_day(day, html_filename=None, video_filename=None):
    """上传指定天数的内容
    
    Args:
        day: 天数
        html_filename: HTML 文件名（在 books/ 目录下）
        video_filename: 视频文件名（在 videos/ 目录下）
    
    Returns:
        (success, html_url, video_url)
    """
    from books_data import get_book_by_day, sanitize_filename
    
    book = get_book_by_day(day)
    clean_title = sanitize_filename(book['short_title'])
    
    files_to_upload = []
    
    # HTML 文件
    if html_filename:
        html_path = os.path.join("books", html_filename)
    else:
        html_path = f"books/book_{day}_{clean_title}.html"
    
    abs_html_path = os.path.join(REPO_DIR, html_path)
    if os.path.exists(abs_html_path):
        files_to_upload.append(html_path)
        log(f"找到 HTML 文件: {html_path}")
    else:
        log(f"⚠️ HTML 文件不存在: {abs_html_path}")
    
    # 视频文件
    if video_filename:
        video_path = os.path.join("videos", video_filename)
    else:
        video_path = f"videos/book_{day}_{clean_title}.mp4"
    
    abs_video_path = os.path.join(REPO_DIR, video_path)
    if os.path.exists(abs_video_path):
        files_to_upload.append(video_path)
        log(f"找到视频文件: {video_path}")
    else:
        log(f"ℹ️ 视频文件不存在（可选）: {video_path}")
    
    if not files_to_upload:
        log("❌ 没有可上传的文件")
        return False, None, None
    
    # 提交信息
    commit_msg = f"Day {day}: {book['short_title']} content"
    
    success, urls = upload_files(files_to_upload, commit_msg)
    
    html_url = None
    video_url = None
    
    for url in urls:
        if url.endswith('.html'):
            html_url = url
        elif url.endswith('.mp4'):
            video_url = url
    
    return success, html_url, video_url


def main():
    # 解析参数
    day = None
    
    if len(sys.argv) > 1:
        try:
            day = int(sys.argv[1])
        except ValueError:
            pass
    
    if day is None:
        from datetime import date
        START_DATE = date(2026, 10, 22)
        today = date.today()
        day = (today - START_DATE).days + 1
        if day < 1:
            day = 1
        if day > 100:
            day = 100
    
    log(f"=" * 50)
    log(f"开始第 {day} 天内容上传")
    
    # 检查状态
    if not check_git_status():
        sys.exit(1)
    
    # 上传
    success, html_url, video_url = upload_for_day(day)
    
    if success:
        log(f"=" * 50)
        log(f"✅ 第 {day} 天上载完成")
        if html_url:
            log(f"   HTML: {html_url}")
        if video_url:
            log(f"   视频: {video_url}")
    else:
        log(f"❌ 上传失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
