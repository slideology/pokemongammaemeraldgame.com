# Vercel部署方案 - 游戏API集成到Flask应用

本文档详细介绍了如何将游戏API成功集成到Flask应用中，实现统一的代码管理和部署流程。

## 目录

1. [方案概述](#方案概述)
2. [实现架构](#实现架构)
3. [关键组件](#关键组件)
4. [实现步骤](#实现步骤)
5. [访问方式](#访问方式)
6. [优化与改进](#优化与改进)
7. [部署流程](#部署流程)

## 方案概述

我们成功将原本基于Node.js的游戏API集成到了主Flask应用中，实现了统一的代码管理和部署流程。这种方案避免了使用多个代码库和子域名，简化了维护和部署过程。

### 核心功能

- **双路径访问**：通过两种URL路径访问游戏
  - `/game/[game-id]`：游戏页面，使用game-template.html模板
  - `/[game-id]`：游戏介绍页面，使用现有的模板文件
  
- **统一代码管理**：所有代码在一个项目中维护
  - 移除了原有的Node.js代码（保留备份）
  - 将游戏API功能集成到Flask应用中

- **简化部署流程**：单一部署流程
  - 一次部署即可更新所有功能
  - 避免了多个部署流程的协调问题

## 实现架构

整个系统采用以下架构：

```
bearclicker/
├── app.py                     # Flask主应用，包含所有路由
├── api/                       # API目录
│   └── game_api.py            # 游戏API实现
├── static/                    # 静态资源
│   └── game-templates/        # 游戏模板
│       └── game-template.html # 游戏iframe嵌套模板
├── templates/                 # 模板目录
│   └── [game-id].html         # 游戏介绍页面模板
├── vercel.json                # Vercel配置文件
└── bearclicker-vercel-backup/ # 原Node.js实现备份
```

## 关键组件

### 1. Flask路由

在`app.py`中，我们添加了两种路由处理方式：

```python
# 游戏API路由 - 返回游戏页面
@app.route('/game/<path:game_id>')
def game_page(game_id):
    return game_api(game_id)

# 游戏介绍页面路由 - 如astro-robot-clicker
@app.route('/astro-robot-clicker')
def astro_robot_clicker():
    return render_template('astro-robot-clicker.html')
```

### 2. 游戏API实现

在`api/game_api.py`中，我们实现了游戏API功能：

```python
def game_api(game_id=None):
    # 处理游戏ID
    if game_id:
        game_id = game_id.replace('.html', '')
    
    # 加载游戏配置
    games = load_games_config()
    
    # 查找游戏配置
    game_config = next((g for g in games if g['id'] == game_id), None)
    
    if not game_config:
        return "Game not found", 404
    
    # 读取游戏模板
    template_path = os.path.join(app.static_folder, 'game-templates', 'game-template.html')
    with open(template_path, 'r') as f:
        html = f.read()
    
    # 替换模板中的占位符
    html = html.replace('{{GAME_TITLE}}', game_config['title'])
    html = html.replace('{{GAME_URL}}', game_config['url'])
    
    return html
```

### 3. 游戏模板

游戏模板`static/game-templates/game-template.html`提供了游戏iframe嵌套功能：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{GAME_TITLE}} - Bear Clicker</title>
    <!-- CSS样式 -->
</head>
<body>
    <div class="game-container">
        <iframe src="{{GAME_URL}}" allowfullscreen></iframe>
        <div class="bottom-bar">
            <div class="game-link-container">
                <!-- 底部链接，带有金色对勾图标 -->
                <a href="https://bearclicker.net" class="link-button" target="_blank">
                    More Games on BearClicker.net
                </a>
            </div>
        </div>
    </div>
</body>
</html>
```

### 4. Vercel配置

在`vercel.json`中，我们配置了路由规则：

```json
{
  "version": 2,
  "routes": [
    {
      "src": "/game/(.*)",
      "dest": "/api/game-api?gameId=$1"
    }
  ]
}
```

## 实现步骤

1. **创建备份**：
   - 将原`bearclicker-vercel`目录重命名为`bearclicker-vercel-backup`

2. **集成游戏API**：
   - 在`app.py`中添加游戏API路由
   - 修改`game_api.py`文件以接收参数
   - 移除embed请求的处理逻辑

3. **更新Vercel配置**：
   - 修改`vercel.json`中的路由配置
   - 确保请求正确路由到Flask应用

4. **优化游戏模板**：
   - 移除顶部导航栏
   - 添加更美观的底部游戏链接容器

5. **本地测试**：
   - 测试`/game/[game-id]`和`/[game-id]`两种访问方式
   - 确认返回的内容符合预期

## 访问方式

本方案支持两种访问方式：

1. **游戏页面**：
   - URL格式：`https://bearclicker.net/game/[game-id]`
   - 示例：`https://bearclicker.net/game/astro-robot-clicker`
   - 内容：纯游戏页面，使用game-template.html模板
   - 特点：沉浸式游戏体验，底部有链接回到主站

2. **游戏介绍页面**：
   - URL格式：`https://bearclicker.net/[game-id]`
   - 示例：`https://bearclicker.net/astro-robot-clicker`
   - 内容：游戏介绍页面，使用现有的模板文件
   - 特点：包含游戏介绍、评论等信息

## 优化与改进

### 游戏模板优化

我们对游戏模板进行了以下优化：

1. **移除顶部导航栏**：
   - 提供更沉浸的游戏体验
   - 减少视觉干扰

2. **添加底部链接容器**：
   - 使用半透明背景
   - 添加金色对勾图标
   - 设置悬停效果
   - 文本："More Games on Bear Clicker"

3. **响应式设计**：
   - 适配不同屏幕尺寸
   - 移动设备友好

## 部署流程

1. **提交更改**：
   - 将所有更改提交到Git仓库
   - 推送到GitHub

2. **Vercel自动部署**：
   - Vercel监听GitHub仓库变化
   - 自动构建和部署更新

3. **验证部署**：
   - 测试线上环境中的游戏页面和介绍页面
   - 确保所有功能正常工作

## 结论

通过将游戏API集成到Flask应用中，我们实现了：

1. **统一代码管理**：所有代码在一个项目中维护
2. **简化部署流程**：一次部署即可更新所有功能
3. **双路径访问**：两种不同的游戏访问体验
4. **优化用户体验**：更美观的游戏页面设计

这种实现方式不仅简化了开发和维护流程，还提供了更好的用户体验。未来可以基于此架构进一步扩展功能，如添加更多游戏、优化加载速度等。