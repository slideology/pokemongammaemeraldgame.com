# Bear Clicker - 在线游戏平台 (v1.0.0)

Bear Clicker 是一个提供多种点击类游戏的在线游戏平台，用户可以在这里体验各种有趣的点击游戏，包括农场模拟、动物收集、冒险等多种类型。

## 功能特点

### 1. 游戏内容
- 丰富多样的游戏类型（包括 Capybara Clicker, Little Farm Clicker, Cookie Clicker 等40+款游戏）
- 每个游戏都有独特的视觉设计和游戏机制
- 支持在线游玩和体验
- 游戏内嵌功能，提供沉浸式体验

### 2. 平台功能
- 响应式设计，完美支持移动端和桌面端
- SEO优化，提高游戏在搜索引擎中的可见性
- 动态FAQ系统，为用户提供游戏相关问答
- 多语言支持（通过翻译文件配置）
- 游戏API集成，支持多种访问方式

### 3. 技术特性
- 现代化UI设计，使用渐变色和动画效果
- 优化的游戏加载机制
- 完善的错误处理和日志系统
- 支持Vercel部署，简化发布流程

## 技术栈

- **后端**：Flask (Python)
- **前端**：HTML + Tailwind CSS + Alpine.js
- **部署**：Vercel
- **分析**：Google Analytics, Plausible Analytics, Microsoft Clarity
- **其他**：Jinja2模板引擎

## 项目结构

```
bearclicker/
├── app.py              # Flask应用主文件，包含所有路由
│   # 主要功能：首页、游戏页面路由、用户认证、API集成
├── api/                # API目录
│   └── game_api.py     # 游戏API实现
│       # 主要功能：加载游戏配置、处理游戏请求、返回游戏内容
├── config/             # 配置文件目录
│   └── logging_config.py # 日志配置
├── models.py           # 数据模型
│   # 主要模型：User(用户)、Message(消息)、ImageGeneration(图片生成)、Payment(支付)
├── static/             # 静态资源
│   ├── css/            # 样式文件
│   │   └── tailwind.css  # Tailwind CSS样式
│   ├── js/             # JavaScript文件
│   │   ├── alpine.js    # Alpine.js框架
│   │   └── analytics.js # 分析跟踪脚本
│   ├── images/         # 图片资源
│   │   ├── games/      # 游戏预览图
│   │   └── favicon/    # 游戏图标
│   ├── data/           # 配置数据
│   │   ├── faqs.json    # FAQ数据
│   │   ├── paper.json   # 纸张游戏配置
│   │   └── translations.json # 多语言翻译
│   └── game-config/    # 游戏配置
│       └── games.json   # 游戏列表配置
├── templates/          # HTML模板
│   ├── base.html       # 基础模板（包含SEO标签、样式、脚本）
│   ├── components/     # 可重用组件
│   │   ├── hero.html        # 英雄区域（游戏标题、描述、按钮）
│   │   ├── nav.html         # 导航栏
│   │   ├── footer.html      # 页脚
│   │   ├── faq_section.html # FAQ部分
│   │   ├── trending_games.html # 热门游戏推荐
│   │   ├── trending_videos.html # 热门视频
│   │   ├── paper.html       # 纸张游戏组件
│   │   └── affiliate_banner.html # 联盟营销横幅
│   ├── index.html      # 首页模板
│   ├── game-template.html # 纯游戏页面模板
│   └── *.html          # 各游戏介绍页面模板
├── vercel.json         # Vercel部署配置
│   # 包含路由、环境变量、构建命令等
├── requirements.txt    # Python依赖
├── .env                # 环境变量（本地开发用）
└── .env.example        # 环境变量示例
```

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
- 复制 `.env.example` 为 `.env`
- 填写必要的环境变量（如SECRET_KEY等）

3. 运行应用：
```bash
python app.py
```
应用将在 http://localhost:5002 运行

## 访问方式

### 游戏介绍页面
- URL格式：`https://bearclicker.net/[game-id]`
- 示例：`https://bearclicker.net/little-farm-clicker`
- 内容：游戏介绍、游戏嵌入框、相关游戏推荐、FAQ等

### 纯游戏页面
- URL格式：`https://bearclicker.net/game/[game-id]`
- 示例：`https://bearclicker.net/game/little-farm-clicker`
- 内容：纯游戏页面，使用game-template.html模板
- 特点：沉浸式游戏体验，底部有链接回到主站

## 添加新游戏

1. 在 `templates/` 目录下创建新的游戏页面模板（如 `new-game-clicker.html`）
2. 在 `app.py` 中添加对应的路由函数
3. 在 `static/images/games/` 目录下添加游戏预览图
4. 在 `static/images/favicon/` 目录下添加游戏图标
5. 如需通过API访问，在 `static/game-config/games.json` 中添加游戏配置

## 自动化工具

项目包含自动化抓取与AI优化方案，详见 `自动化抓取与AI优化方案.md`，可用于：

### 自动化抓取与AI优化方案结构

```
自动化抓取与AI优化方案/
├── scraper.py           # 网页内容抓取脚本
│   # 功能：解析sitemap、抓取游戏页面、下载图片
├── ai_optimizer.py      # AI内容优化模块
│   # 功能：标题优化、描述优化、关键词策略、FAQ生成
├── seo_analyzer.py      # SEO分析工具
│   # 功能：分析原始页面SEO状况、生成改进建议
├── template_generator.py # 模板生成器
│   # 功能：基于优化内容生成HTML模板
├── config/              # 配置文件
│   ├── scraper_config.json # 抓取器配置
│   ├── ai_config.json     # AI优化配置
│   └── template_config.json # 模板生成配置
├── data/                # 数据存储
│   ├── raw/             # 原始抓取数据
│   ├── processed/       # 处理后数据
│   └── images/          # 下载的图片
├── logs/                # 日志文件
├── main.py              # 主执行脚本
└── requirements.txt     # 依赖包
```

### 主要功能

- **网页内容抓取**：从 stimulationclicker.com 自动抓取游戏内容
- **AI内容优化**：使用AI优化标题、描述、关键词和文案
- **SEO分析与优化**：分析原始页面并生成SEO改进建议
- **自动生成模板**：基于优化后的内容自动生成HTML模板
- **批量处理**：支持批量抓取和处理多个游戏页面
- **定时更新**：可配置定时任务自动更新内容

## 部署

项目使用Vercel进行部署，详细部署方案见 `Vercel部署方案.md`。

### 自定义域名

项目支持使用自定义域名，如 `game.bearclicker.net`，配置步骤包括：

1. 在配置文件中添加域名设置
2. 在Vercel平台配置自定义域名
3. 在DNS提供商添加相应的CNAME或A记录

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 许可证

版权所有 © 2025 Bear Clicker