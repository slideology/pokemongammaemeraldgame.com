# Bear Clicker Vercel

基于Vercel平台的游戏iframe嵌套系统，用于替代原有的Cloudflare Workers方案。

## 项目概述

本项目是Bear Clicker游戏平台的Vercel部署方案，提供了一个简单高效的方式来托管和展示游戏内容。系统通过Vercel的Serverless Functions和静态文件托管功能，实现了与原有Cloudflare Workers相同的游戏iframe嵌套功能。

### 主要功能

- **游戏iframe嵌套**：将游戏内容嵌入到自定义的HTML模板中
- **动态HTML生成**：根据游戏ID生成适配的iframe页面
- **品牌链接定制**：显示Bear Clicker品牌和外部链接
- **简单的配置管理**：通过JSON文件管理游戏配置

## 项目结构

```
bearclicker-vercel/
├── public/                    # 静态资源目录
│   └── game-template.html     # 游戏iframe嵌套模板
├── api/                       # Vercel API路由
│   └── [gameId].js           # 处理游戏请求的动态路由
├── config/                    # 配置文件目录
│   └── games.json            # 游戏配置文件
├── scripts/                   # 部署和管理脚本
│   ├── update-config.js      # 更新配置脚本
│   ├── deploy.sh             # 部署脚本
│   ├── deploy-preview.js     # 本地预览脚本
│   └── integrate-with-bearclicker.js  # 与现有项目集成的脚本
├── package.json              # 项目依赖和脚本
└── vercel.json               # Vercel配置文件
```

## 安装和设置

### 前提条件

- Node.js 14.x 或更高版本
- npm 或 yarn
- Vercel CLI (可选，用于本地开发)

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/yourusername/bearclicker-vercel.git
cd bearclicker-vercel
```

2. 安装依赖

```bash
npm install
```

3. 与现有项目集成

```bash
node scripts/integrate-with-bearclicker.js
```

## 使用指南

### 本地开发

启动本地预览服务器：

```bash
node scripts/deploy-preview.js
```

服务器将在 http://localhost:3000 上运行，控制台会显示可用的游戏链接。

### 自定义域名配置

要使用自定义域名（如 `game.bearclicker.net`）访问部署的游戏，需要完成以下步骤：

1. 在 `config/games.json` 文件中添加域名配置：

```json
{
  "domain": "game.bearclicker.net",
  "brandName": "Bear Clicker",
  "brandUrl": "https://bearclicker.net",
  "games": [...]
}
```

2. 在 Vercel 平台上配置自定义域名：
   - 登录 Vercel 控制台
   - 选择您的项目
   - 进入 "Settings" > "Domains"
   - 添加 `game.bearclicker.net` 作为自定义域名
   - 按照 Vercel 提供的验证说明操作

3. 在您的 DNS 提供商处添加 CNAME 记录：
   - 名称：`game`
   - 值：Vercel 提供的目标值（通常是 `cname.vercel-dns.com`）
   - TTL：建议 3600（1小时）或更低

### 添加新游戏

1. 将游戏文件添加到Bear Clicker项目的`static/games/`目录中
2. 运行集成脚本更新配置：

```bash
node scripts/integrate-with-bearclicker.js
```

或者手动编辑`config/games.json`文件，添加新游戏的配置。

### 部署到Vercel

使用部署脚本：

```bash
./scripts/deploy.sh
```

或者手动部署：

```bash
npx vercel --prod
```

## 配置文件说明

### games.json

```json
{
  "domain": "game.bearclicker.net",
  "brandName": "Bear Clicker",
  "brandUrl": "https://bearclicker.net",
  "games": [
    {
      "id": "game-id",
      "title": "游戏标题",
      "url": "https://example.com/game-url/"
    }
  ]
}
```

- **domain**: 部署后使用的自定义域名
- **brandName**: 显示在游戏页面上的品牌名称
- **brandUrl**: 品牌链接的URL
- **id**: 游戏的唯一标识符，用于URL路径
- **title**: 游戏的显示标题
- **url**: 游戏的源URL

## 故障排除

### 常见问题

1. **游戏无法加载**
   - 检查游戏URL是否正确
   - 确认游戏源服务器是否允许iframe嵌套

2. **部署失败**
   - 检查Vercel账号配置
   - 确认项目中没有语法错误

3. **本地预览问题**
   - 确保已安装所有依赖
   - 检查端口3000是否被占用

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 访问方式对比

使用 Vercel 部署方案后，游戏可以通过两种不同的 URL 访问，它们有以下区别：

### game.bearclicker.net/astro-robot-clicker vs bearclicker.net/astro-robot-clicker.html

#### 1. 服务平台不同

- **game.bearclicker.net/astro-robot-clicker**：
  - 由 Vercel 平台提供服务
  - 使用新开发的游戏 iframe 嵌套系统
  - 通过 API 路由动态生成 HTML 页面

- **bearclicker.net/astro-robot-clicker.html**：
  - 由原有的服务器（Flask 应用）提供服务
  - 使用现有的 Jinja2 模板系统
  - 通过 Flask 路由处理请求

#### 2. 页面结构和内容差异

- **game.bearclicker.net/astro-robot-clicker**：
  - 简化的页面结构，专注于游戏体验
  - 只包含品牌栏和游戏 iframe
  - 不包含其他额外内容（如 trending_games、FAQ 等）

- **bearclicker.net/astro-robot-clicker.html**：
  - 完整的网站体验，包含多个组件
  - 包含游戏 iframe、trending_games 部分和 FAQ 部分
  - 有更多的样式和交互元素

#### 3. 性能和用户体验

- **game.bearclicker.net/astro-robot-clicker**：
  - 加载更快，页面更简洁
  - 专注于游戏体验，减少干扰
  - 使用 Vercel 的全球 CDN，访问速度更快

- **bearclicker.net/astro-robot-clicker.html**：
  - 加载可能稍慢，因为包含更多内容
  - 提供更丰富的网站体验和导航选项

#### 4. 维护和更新方式

- **game.bearclicker.net/astro-robot-clicker**：
  - 通过更新 `config/games.json` 文件更新游戏信息
  - 使用 `deploy.sh` 脚本一键部署
  - 可以独立于主网站进行更新和维护

- **bearclicker.net/astro-robot-clicker.html**：
  - 需要更新模板文件来修改游戏信息
  - 可能需要重启 Flask 应用来应用更改
  - 与主网站的更新和维护绑定在一起

## 许可证

本项目采用 MIT 许可证 - 详情见 [LICENSE](LICENSE) 文件
