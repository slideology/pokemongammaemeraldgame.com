# Vercel部署方案 - 多域名游戏iframe嵌套系统

本文档详细介绍如何将当前基于Cloudflare Workers的游戏iframe嵌套系统迁移到Vercel平台，实现相同的多域名游戏访问功能。

## 目录

1. [方案概述](#方案概述)
2. [Vercel vs Cloudflare Workers对比](#vercel-vs-cloudflare-workers对比)
3. [项目重构](#项目重构)
4. [实现步骤](#实现步骤)
5. [部署流程](#部署流程)
6. [域名配置](#域名配置)
7. [维护与更新](#维护与更新)
8. [与现有项目集成](#与现有项目集成)
9. [常见问题](#常见问题)
10. [参考资源](#参考资源)

## 方案概述

Vercel是一个现代化的云平台，专为前端和Jamstack应用设计，提供了简单的部署流程和强大的全球CDN。本方案将展示如何利用Vercel的Serverless Functions和静态文件托管功能，实现与当前Cloudflare Workers相同的多域名游戏iframe嵌套系统。

### 核心功能保留

- 多域名支持：不同游戏可通过不同域名访问
- 动态HTML生成：根据游戏ID和域名生成适配的iframe页面
- 品牌链接定制：根据域名显示不同的品牌和外部链接
- 简单的配置管理：通过JSON文件管理游戏和域名配置

## Vercel vs Cloudflare Workers对比

### Vercel优势

1. **更简单的部署流程**
   - 直接连接GitHub/GitLab仓库，自动部署
   - 提供直观的Web界面管理部署和配置
   - 每个PR自动生成预览环境

2. **开发者体验**
   - 本地开发环境与生产环境高度一致
   - 详细的部署日志和错误报告
   - 内置分析和性能监控工具

3. **扩展性**
   - 无缝支持Next.js、Nuxt、SvelteKit等现代框架
   - 丰富的集成选项（CMS、数据库、认证等）
   - 强大的Edge Functions支持

4. **免费计划慷慨**
   - 每月100GB带宽
   - 无限制的函数调用（有执行时间限制）
   - 最多支持3个团队成员

### 需要调整的地方

1. **存储方式**
   - 从Cloudflare R2存储桶迁移到Vercel静态文件存储
   - 文件上传流程需要调整

2. **API实现**
   - 使用Vercel的Serverless Functions替代Worker脚本
   - 路由处理方式略有不同

3. **缓存策略**
   - 调整为Vercel的缓存控制方式
   - 配置适当的缓存头部

## 项目重构

### 新的项目结构

```
game-deploy/
├── public/                    # 静态资源目录
│   ├── game-template.html     # 游戏iframe嵌套模板
│   └── assets/                # 其他静态资源（图标、样式等）
├── api/                       # Vercel API路由
│   └── [gameId].js            # 动态路由处理游戏请求
├── config/                    # 配置文件目录
│   └── games.json             # 游戏和域名配置
├── scripts/                   # 部署和管理脚本
│   ├── update-config.js       # 更新配置脚本
│   └── deploy-preview.js      # 本地预览脚本
├── package.json               # 项目依赖和脚本
├── vercel.json                # Vercel配置文件
└── README.md                  # 项目说明文档
```

## 实现步骤

### 1. 准备项目

1. 创建基本项目结构：

```bash
mkdir -p game-deploy/{public,api,config,scripts}
cd game-deploy
npm init -y
npm install --save-dev vercel
```

2. 将现有的`game-template.html`复制到`public`目录：

```bash
cp assets/game-template.html public/
```

3. 创建配置文件，将现有的`config.json`转换为新格式：

```bash
mkdir -p config
cp deploy/config.json config/games.json
```

### 2. 创建API路由

在`api/[gameId].js`文件中实现动态路由处理：

```javascript
// api/[gameId].js
const fs = require('fs');
const path = require('path');

// 加载游戏配置
const config = require('../config/games.json');

export default function handler(req, res) {
  // 获取游戏ID（从URL路径中提取）
  const { gameId } = req.query;
  const gameIdClean = gameId.replace(/\.html$/, '');
  
  console.log(`处理游戏请求: ${gameIdClean}`);
  
  // 获取请求域名
  const hostname = req.headers.host;
  const domainParts = hostname.split('.');
  const mainDomain = domainParts.length >= 2 
    ? `${domainParts[domainParts.length-2]}.${domainParts[domainParts.length-1]}` 
    : hostname;
  
  console.log(`请求域名: ${mainDomain}`);
  
  // 查找游戏配置
  let gameConfig = config.games.find(g => g.id === gameIdClean);
  
  // 检查域名是否匹配
  if (gameConfig && gameConfig.domain && gameConfig.domain !== mainDomain) {
    console.log(`游戏域名不匹配: 游戏域名=${gameConfig.domain}, 请求域名=${mainDomain}`);
    gameConfig = null; // 如果域名不匹配，则将游戏配置设置为空
  }
  
  if (!gameConfig) {
    console.log(`未找到游戏配置: ${gameIdClean}`);
    return res.status(404).send('游戏未找到或在此域名下不可用');
  }
  
  // 获取域名配置
  const domainConfig = config.domains[gameConfig.domain || mainDomain] || {
    displayName: mainDomain,
    linkUrl: `https://${mainDomain}/`
  };
  
  // 读取模板文件
  const templatePath = path.join(process.cwd(), 'public', 'game-template.html');
  let templateContent = fs.readFileSync(templatePath, 'utf8');
  
  // 替换占位符
  templateContent = templateContent.replace(/\{\{GAME_TITLE\}\}/g, gameConfig.title);
  templateContent = templateContent.replace(/\{\{GAME_URL\}\}/g, gameConfig.sourceUrl);
  templateContent = templateContent.replace(/\{\{DOMAIN_DISPLAY\}\}/g, domainConfig.displayName);
  templateContent = templateContent.replace(/\{\{DOMAIN_LINK\}\}/g, domainConfig.linkUrl);
  
  // 设置缓存控制
  res.setHeader('Cache-Control', 'public, max-age=14400, s-maxage=2592000');
  res.setHeader('Content-Type', 'text/html; charset=UTF-8');
  
  // 返回处理后的HTML
  res.status(200).send(templateContent);
}
```

### 3. 创建Vercel配置文件

在项目根目录创建`vercel.json`：

```json
{
  "version": 2,
  "routes": [
    {
      "src": "/(.*)\\.html",
      "dest": "/api/$1"
    },
    {
      "src": "/(.+)",
      "dest": "/api/$1"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=14400, s-maxage=2592000"
        }
      ]
    }
  ]
}
```

### 4. 创建配置更新脚本

在`scripts/update-config.js`中创建配置更新脚本：

```javascript
// scripts/update-config.js
const fs = require('fs');
const path = require('path');

// 配置文件路径
const configPath = path.join(__dirname, '../config/games.json');

// 读取现有配置
const config = require(configPath);

// 添加或更新游戏
function addOrUpdateGame(id, title, sourceUrl, domain) {
  // 查找现有游戏
  const existingGameIndex = config.games.findIndex(g => g.id === id);
  
  const gameConfig = {
    id,
    title,
    sourceUrl,
    domain
  };
  
  if (existingGameIndex >= 0) {
    // 更新现有游戏
    config.games[existingGameIndex] = gameConfig;
    console.log(`已更新游戏: ${id}`);
  } else {
    // 添加新游戏
    config.games.push(gameConfig);
    console.log(`已添加游戏: ${id}`);
  }
}

// 添加或更新域名
function addOrUpdateDomain(domain, displayName, linkUrl, isDefault = false) {
  config.domains[domain] = {
    defaultDomain: isDefault,
    displayName,
    linkUrl
  };
  
  console.log(`已更新域名: ${domain}`);
  
  // 如果设置为默认域名，则将其他域名的默认标志设置为false
  if (isDefault) {
    Object.keys(config.domains).forEach(key => {
      if (key !== domain) {
        config.domains[key].defaultDomain = false;
      }
    });
  }
}

// 保存配置
function saveConfig() {
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log('配置已保存');
}

// 命令行参数处理
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'add-game':
    if (args.length < 4) {
      console.error('用法: node update-config.js add-game <id> <title> <sourceUrl> [domain]');
      process.exit(1);
    }
    addOrUpdateGame(args[1], args[2], args[3], args[4]);
    saveConfig();
    break;
    
  case 'add-domain':
    if (args.length < 4) {
      console.error('用法: node update-config.js add-domain <domain> <displayName> <linkUrl> [isDefault]');
      process.exit(1);
    }
    addOrUpdateDomain(args[1], args[2], args[3], args[4] === 'true');
    saveConfig();
    break;
    
  default:
    console.error('未知命令');
    console.error('可用命令: add-game, add-domain');
    process.exit(1);
}
```

### 5. 创建本地预览脚本

在`scripts/deploy-preview.js`中创建本地预览脚本：

```javascript
// scripts/deploy-preview.js
const { exec } = require('child_process');
const path = require('path');

// 项目根目录
const rootDir = path.join(__dirname, '..');

// 运行Vercel开发服务器
console.log('启动Vercel开发服务器...');
const vercel = exec('npx vercel dev', { cwd: rootDir });

vercel.stdout.on('data', (data) => {
  console.log(data);
});

vercel.stderr.on('data', (data) => {
  console.error(data);
});

vercel.on('close', (code) => {
  console.log(`Vercel开发服务器已退出，退出码: ${code}`);
});

// 处理进程终止信号
process.on('SIGINT', () => {
  console.log('正在关闭Vercel开发服务器...');
  vercel.kill();
  process.exit();
});
```

### 6. 更新package.json

配置项目脚本和依赖：

```json
{
  "name": "game-deploy",
  "version": "1.0.0",
  "description": "多域名游戏iframe嵌套系统",
  "main": "index.js",
  "scripts": {
    "dev": "node scripts/deploy-preview.js",
    "add-game": "node scripts/update-config.js add-game",
    "add-domain": "node scripts/update-config.js add-domain",
    "deploy": "vercel --prod"
  },
  "keywords": ["games", "iframe", "vercel"],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "vercel": "^31.0.0"
  }
}
```

## 部署流程

### 初始部署

1. **安装Vercel CLI**：

```bash
npm install -g vercel
```

2. **登录Vercel**：

```bash
vercel login
```

3. **初始化项目**：

```bash
cd game-deploy
vercel
```

按照提示操作，将会询问以下问题：
- 是否要链接到现有项目？选择"否"
- 项目名称：输入"game-deploy"或其他名称
- 是否要覆盖配置？选择"是"
- 构建命令：留空
- 输出目录：留空
- 开发命令：`npm run dev`

4. **部署到生产环境**：

```bash
vercel --prod
```

### 持续部署

1. **连接GitHub仓库**：
   - 在Vercel控制台中，点击"Add New..."
   - 选择"Project"
   - 导入你的GitHub仓库
   - 配置部署设置
   - 点击"Deploy"

2. **自动部署**：
   - 每次推送到主分支，Vercel会自动部署最新版本
   - 每个PR会生成一个预览环境

## 域名配置

### 添加自定义域名

1. **在Vercel控制台中**：
   - 选择你的项目
   - 点击"Settings" > "Domains"
   - 点击"Add"
   - 输入你的域名（如`game.bearclicker.net`）
   - 点击"Add"

2. **配置DNS记录**：
   - 按照Vercel提供的说明配置DNS记录
   - 通常是添加CNAME记录，指向Vercel提供的值
   - 或者将域名的NS记录指向Vercel的名称服务器

### 多域名配置

对于每个域名，重复上述步骤。确保在`config/games.json`中正确配置了域名信息。

## 维护与更新

### 添加新游戏

使用提供的脚本添加新游戏：

```bash
npm run add-game "game-id" "游戏标题" "https://游戏源URL" "域名"
```

例如：

```bash
npm run add-game "my-clicker" "My Clicker Game" "https://example.com/game.html" "bearclicker.net"
```

### 添加新域名

使用提供的脚本添加新域名：

```bash
npm run add-domain "域名" "显示名称" "链接URL" [是否默认]
```

例如：

```bash
npm run add-domain "newdomain.com" "New Domain" "https://newdomain.com/" true
```

### 更新模板

如需更新游戏模板，修改`public/game-template.html`文件，然后重新部署：

```bash
vercel --prod
```

## 与现有项目集成

本节详细介绍如何将Vercel部署方案与现有的Bear Clicker项目进行集成，实现平滑过渡。

### 现有项目分析

当前的Bear Clicker项目使用以下技术和结构：

1. **主网站**：基于Flask的网站，托管在传统服务器上
2. **游戏嵌入**：使用Cloudflare Workers处理游戏iframe嵌套
3. **域名结构**：
   - 主域名：`bearclicker.net`
   - 游戏域名：`game.bearclicker.net`
4. **游戏URL格式**：`https://stimulationclicker.com/{game-id}.embed`

### 集成步骤

#### 1. 创建Vercel项目结构

在Bear Clicker项目根目录下创建`bearclicker-vercel`文件夹，包含以下结构：

```
bearclicker-vercel/
├── public/                    # 静态资源目录
│   └── game-template.html     # 游戏iframe嵌套模板
├── api/                       # Vercel API路由
│   └── [gameId].js            # 动态路由处理游戏请求
├── config/                    # 配置文件目录
│   └── games.json             # 游戏和域名配置
├── scripts/                   # 部署和管理脚本
│   ├── update-config.js       # 更新配置脚本
│   ├── deploy.sh              # 部署脚本
│   ├── deploy-preview.js      # 本地预览脚本
│   └── integrate-with-bearclicker.js  # 与现有项目集成的脚本
├── package.json               # 项目依赖和脚本
├── vercel.json                # Vercel配置文件
├── README.md                  # 项目说明文档
└── DEPLOYMENT_GUIDE.md        # 部署指南
```

#### 2. 从现有项目提取游戏数据

创建`integrate-with-bearclicker.js`脚本，自动从现有项目中提取游戏数据：

```javascript
// scripts/integrate-with-bearclicker.js
const fs = require('fs');
const path = require('path');

// 路径配置
const bearclickerRoot = path.join(__dirname, '../..');
const configPath = path.join(__dirname, '../config/games.json');

// 读取现有配置
let config = { games: [], domains: {} };
if (fs.existsSync(configPath)) {
  config = require(configPath);
} else {
  // 确保config目录存在
  const configDir = path.dirname(configPath);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  // 初始化域名配置
  config.domains = {
    "game.bearclicker.net": {
      "defaultDomain": true,
      "displayName": "Bear Clicker",
      "linkUrl": "https://bearclicker.net/"
    }
  };
}

// 从app.py中提取游戏路由
console.log('从app.py中提取游戏路由...');
try {
  const appPyPath = path.join(bearclickerRoot, 'app.py');
  const appPyContent = fs.readFileSync(appPyPath, 'utf8');
  
  // 使用正则表达式提取路由
  const routeRegex = /@app\.route\(\'\/(.*?)\'\)\s*\ndef\s+(.*?)\(\):/g;
  let match;
  
  while ((match = routeRegex.exec(appPyContent)) !== null) {
    const route = match[1];
    const routeFunction = match[2];
    
    // 跳过非游戏路由
    if (route.startsWith('static') || 
        route === '' || 
        route === 'favicon.ico' || 
        route === 'robots.txt' || 
        route === 'sitemap.xml') {
      continue;
    }
    
    // 查找对应的模板文件
    const templatePath = path.join(bearclickerRoot, 'templates', `${route}.html`);
    if (!fs.existsSync(templatePath)) {
      console.log(`跳过路由 ${route}，未找到对应的模板文件`);
      continue;
    }
    
    // 读取模板文件，查找game_url
    const templateContent = fs.readFileSync(templatePath, 'utf8');
    const gameUrlMatch = templateContent.match(/game_url="([^"]+)"/); 
    
    if (!gameUrlMatch) {
      console.log(`跳过路由 ${route}，未找到game_url`);
      continue;
    }
    
    // 提取游戏标题
    const titleMatch = templateContent.match(/title="([^"]+)"/); 
    const title = titleMatch ? titleMatch[1] : route;
    
    // 检查是否已存在于配置中
    const existingGameIndex = config.games.findIndex(g => g.id === route);
    
    if (existingGameIndex >= 0) {
      console.log(`更新游戏配置: ${route}`);
      config.games[existingGameIndex].title = title;
      config.games[existingGameIndex].sourceUrl = gameUrlMatch[1];
    } else {
      console.log(`添加游戏配置: ${route}`);
      config.games.push({
        id: route,
        title: title,
        sourceUrl: gameUrlMatch[1],
        domain: "game.bearclicker.net"
      });
    }
  }
  
  // 保存配置
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log('配置已保存');
  
} catch (error) {
  console.error('处理app.py时出错:', error);
  process.exit(1);
}

console.log('集成完成！');
```

#### 3. 创建游戏模板

创建`public/game-template.html`文件，用于嵌套游戏iframe：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{GAME_TITLE}} - Bear Clicker</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body, html {
            height: 100%;
            width: 100%;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        .game-container {
            position: relative;
            width: 100%;
            height: 100vh;
            overflow: hidden;
        }
        
        iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        
        .brand-bar {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 8px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
            font-size: 14px;
        }
        
        .brand-bar a {
            color: white;
            text-decoration: none;
            transition: opacity 0.2s;
        }
        
        .brand-bar a:hover {
            opacity: 0.8;
        }
        
        .brand-logo {
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .brand-bar {
                padding: 6px 10px;
                font-size: 12px;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="brand-bar">
            <a href="{{DOMAIN_LINK}}" class="brand-logo">{{DOMAIN_DISPLAY}}</a>
            <a href="{{DOMAIN_LINK}}" class="back-link">返回主页</a>
        </div>
        <iframe src="{{GAME_URL}}" allowfullscreen></iframe>
    </div>
</body>
</html>
```

#### 4. 适配现有URL格式

修改`api/[gameId].js`文件，确保能够正确处理现有的URL格式：

```javascript
// api/[gameId].js
const fs = require('fs');
const path = require('path');

// 加载游戏配置
const config = require('../config/games.json');

module.exports = (req, res) => {
  // 获取游戏ID（从URL路径中提取）
  const { gameId } = req.query;
  const gameIdClean = gameId.replace(/\.html$/, '');
  
  console.log(`处理游戏请求: ${gameIdClean}`);
  
  // 获取请求域名
  const hostname = req.headers.host;
  const domainParts = hostname.split('.');
  const mainDomain = domainParts.length >= 2 
    ? `${domainParts[domainParts.length-2]}.${domainParts[domainParts.length-1]}` 
    : hostname;
  
  console.log(`请求域名: ${mainDomain}`);
  
  // 查找游戏配置
  let gameConfig = config.games.find(g => g.id === gameIdClean);
  
  // 检查域名是否匹配
  if (gameConfig && gameConfig.domain && gameConfig.domain !== mainDomain) {
    console.log(`游戏域名不匹配: 游戏域名=${gameConfig.domain}, 请求域名=${mainDomain}`);
    gameConfig = null; // 如果域名不匹配，则将游戏配置设置为空
  }
  
  if (!gameConfig) {
    console.log(`未找到游戏配置: ${gameIdClean}`);
    return res.status(404).send('游戏未找到或在此域名下不可用');
  }
  
  // 获取域名配置
  const domainConfig = config.domains[gameConfig.domain || mainDomain] || {
    displayName: mainDomain,
    linkUrl: `https://${mainDomain}/`
  };
  
  // 读取模板文件
  const templatePath = path.join(process.cwd(), 'public', 'game-template.html');
  let templateContent = fs.readFileSync(templatePath, 'utf8');
  
  // 替换占位符
  templateContent = templateContent.replace(/\{\{GAME_TITLE\}\}/g, gameConfig.title);
  templateContent = templateContent.replace(/\{\{GAME_URL\}\}/g, gameConfig.sourceUrl);
  templateContent = templateContent.replace(/\{\{DOMAIN_DISPLAY\}\}/g, domainConfig.displayName);
  templateContent = templateContent.replace(/\{\{DOMAIN_LINK\}\}/g, domainConfig.linkUrl);
  
  // 设置缓存控制
  res.setHeader('Cache-Control', 'public, max-age=14400, s-maxage=2592000');
  res.setHeader('Content-Type', 'text/html; charset=UTF-8');
  
  // 返回处理后的HTML
  res.status(200).send(templateContent);
};
```

#### 5. 创建部署脚本

创建`scripts/deploy.sh`脚本，简化部署过程：

```bash
#!/bin/bash

# 确保在bearclicker-vercel目录中
cd "$(dirname "$0")/.." || exit

# 检查是否已登录Vercel
echo "检查Vercel登录状态..."
npx vercel whoami &>/dev/null
if [ $? -ne 0 ]; then
  echo "未登录Vercel，请先登录..."
  npx vercel login
fi

# 部署到Vercel
echo "开始部署到Vercel..."
npx vercel --prod

echo "部署完成！"
echo "请在Vercel控制台中配置自定义域名: game.bearclicker.net"
echo "https://vercel.com/dashboard"
```

#### 6. 过渡策略

为了确保平稳过渡，建议采用以下策略：

1. **并行运行**：在一段时间内同时保持Cloudflare Workers和Vercel部署
2. **流量分流**：逐步将流量从Cloudflare Workers转移到Vercel
3. **监控与回滚**：密切监控Vercel部署的性能和稳定性，如有问题可快速回滚

#### 7. DNS配置更新

最终将`game.bearclicker.net`的DNS记录从Cloudflare Workers更新为Vercel：

1. 在Vercel控制台中添加自定义域名`game.bearclicker.net`
2. 按照Vercel提供的说明更新DNS记录
3. 验证DNS配置生效后，可以完全切换到Vercel部署

## 常见问题

### Q: 如何查看访问日志？
A: 在Vercel控制台中，选择你的项目，点击"Analytics"查看访问统计和日志。

### Q: 如何处理跨域问题？
A: 在`vercel.json`中添加适当的CORS头部：

```json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" }
      ]
    }
  ]
}
```

### Q: 如何限制特定域名的访问？
A: 在API路由中添加域名检查逻辑，拒绝未授权的域名请求。

### Q: 如何监控性能？
A: Vercel提供内置的性能监控工具，在控制台的"Analytics"部分可以查看。

### Q: 迁移过程中如何确保服务不中断？
A: 采用蓝绿部署策略，先部署Vercel版本，验证无误后再切换DNS记录。

### Q: 如何处理现有游戏URL格式的变化？
A: 在API路由中添加兼容逻辑，支持多种URL格式，确保旧链接仍然可用。

## 参考资源

- [Vercel文档](https://vercel.com/docs)
- [Vercel API参考](https://vercel.com/docs/api)
- [Vercel CLI参考](https://vercel.com/docs/cli)
- [Vercel Serverless Functions](https://vercel.com/docs/functions/serverless-functions)
- [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions)

## 实施进展与优化

本节记录了Vercel部署方案的实际实施进展、优化和测试结果。

### 已完成工作

#### 1. 配置文件优化

在`config/games.json`中添加了域名相关配置：

```json
{
  "domain": "game.bearclicker.net",
  "brandName": "Bear Clicker",
  "brandUrl": "https://bearclicker.net",
  "games": [
    {
      "id": "astro-robot-clicker",
      "title": "Astro Robot Clicker",
      "url": "https://stimulationclicker.com/astro-robot-clicker.embed"
    },
    // 其他游戏...
  ]
}
```

#### 2. 集成脚本改进

修改了`integrate-with-bearclicker.js`脚本，使其能够从游戏HTML模板文件中提取`game_url`和`title`信息：

```javascript
// 提取游戏URL和标题
const gameUrlMatch = content.match(/game_url="([^"]+)"/); 
const titleMatch = content.match(/title="([^"]+)"/); 

if (gameUrlMatch && titleMatch) {
  const title = titleMatch[1];
  console.log(`找到游戏: ${title} (${route})`);
  
  // 添加到配置中
  config.games.push({
    id: route,
    title: title,
    url: gameUrlMatch[1]
  });
}
```

#### 3. API路由优化

在`api/[gameId].js`中使用配置文件中的域名设置替换模板中的占位符：

```javascript
// 替换模板中的占位符
let html = templateContent
  .replace(/{{GAME_TITLE}}/g, gameConfig.title)
  .replace(/{{GAME_URL}}/g, gameConfig.url)
  .replace(/{{DOMAIN_DISPLAY}}/g, config.brandName || 'Bear Clicker')
  .replace(/{{DOMAIN_LINK}}/g, config.brandUrl || 'https://bearclicker.net');
```

#### 4. 游戏模板UI优化

优化了游戏模板UI，移除了顶部导航栏，添加了更美观的底部游戏链接容器：

```html
<div class="bottom-bar">
  <div class="game-link-container">
    <div style="display: flex; align-items: center;">
      <div class="game-icon">
        <svg viewBox="0 0 24 24" fill="#ffd700">
          <path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
        </svg>
      </div>
      <a href="{{DOMAIN_LINK}}" class="link-button" target="_blank">
        More Games on BearClicker.net
        <span style="margin-left: 12px; display: inline-flex; align-items: center;">
          <svg viewBox="0 0 24 24" fill="#ffd700" width="24" height="24">
            <path d="M8,5.14V19.14L19,12.14L8,5.14Z" />
          </svg>
        </span>
      </a>
    </div>
  </div>
</div>
```

相应的CSS样式：

```css
.bottom-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.85);
  color: white;
  padding: 10px 20px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  z-index: 1000;
}

.game-icon {
  width: 24px;
  height: 24px;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.link-button {
  display: flex;
  align-items: center;
  background-color: transparent;
  padding: 4px 0;
  font-weight: bold;
  font-size: 16px;
  color: #FFD700;
  transition: opacity 0.2s;
}
```

#### 5. 本地预览脚本改进

修改了`deploy-preview.js`脚本，使其能够在不同端口上运行，并添加了配置文件检查功能：

```javascript
function main() {
  console.log('开始准备本地预览...');
  
  // 检查配置文件是否存在
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error(`配置文件不存在: ${CONFIG_PATH}`);
    console.log('请先运行 integrate-with-bearclicker.js 脚本提取游戏信息');
    process.exit(1);
  }

  // 使用现有配置启动预览服务器
  console.log('使用现有配置启动预览服务器...');
  startPreviewServer();
}
```

#### 6. 文档更新

更新了项目README文件，添加了自定义域名配置指南和访问方式对比：

- **自定义域名配置**：详细说明了如何配置`game.bearclicker.net`域名
- **访问方式对比**：对比了`game.bearclicker.net`和`bearclicker.net`两种访问方式的区别

### 测试结果

本地测试显示，所有功能正常工作：

- 游戏页面能够正确加载
- 底部导航栏显示美观，并能正确链接到主站
- 响应式设计在不同屏幕尺寸下表现良好

### 后续步骤

1. **部署到Vercel平台**：使用`vercel`命令将项目部署到Vercel
2. **配置自定义域名**：在Vercel控制台添加`game.bearclicker.net`作为自定义域名
3. **设置DNS记录**：在DNS提供商处添加CNAME记录，将`game.bearclicker.net`指向Vercel提供的域名
4. **监控与优化**：部署后监控性能和用户体验，根据反馈进行进一步优化
