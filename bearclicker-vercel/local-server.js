const http = require('http');
const url = require('url');
const path = require('path');
const fs = require('fs');

// 导入API路由处理函数
const gameApiHandler = require('./api/[gameId].js');

// 创建HTTP服务器
const server = http.createServer((req, res) => {
  // 解析请求URL
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  
  console.log(`\n--- 收到请求 ---`);
  console.log(`路径: ${pathname}`);
  console.log(`方法: ${req.method}`);
  
  // 处理静态文件请求
  if (pathname.startsWith('/public/')) {
    const filePath = path.join(__dirname, pathname);
    
    // 检查文件是否存在
    fs.access(filePath, fs.constants.F_OK, (err) => {
      if (err) {
        console.log(`文件不存在: ${filePath}`);
        res.statusCode = 404;
        res.end('File not found');
        return;
      }
      
      // 读取并返回文件内容
      fs.readFile(filePath, (err, data) => {
        if (err) {
          console.error(`读取文件错误: ${err.message}`);
          res.statusCode = 500;
          res.end('Internal server error');
          return;
        }
        
        // 设置Content-Type
        const ext = path.extname(filePath);
        let contentType = 'text/plain';
        
        switch (ext) {
          case '.html':
            contentType = 'text/html';
            break;
          case '.css':
            contentType = 'text/css';
            break;
          case '.js':
            contentType = 'application/javascript';
            break;
          case '.json':
            contentType = 'application/json';
            break;
          case '.png':
            contentType = 'image/png';
            break;
          case '.jpg':
          case '.jpeg':
            contentType = 'image/jpeg';
            break;
        }
        
        res.setHeader('Content-Type', contentType);
        res.end(data);
      });
    });
    return;
  }
  
  // 处理API路由
  if (pathname !== '/' && pathname !== '/favicon.ico') {
    // 提取游戏ID
    const gameId = pathname.substring(1); // 移除开头的斜杠
    
    // 模拟Vercel的API路由请求
    req.query = { gameId };
    
    // 模拟Vercel的res.status和res.send方法
    res.status = function(code) {
      this.statusCode = code;
      return this;
    };
    
    res.send = function(data) {
      if (typeof data === 'string') {
        this.setHeader('Content-Type', 'text/html; charset=utf-8');
        this.end(data);
      } else {
        this.setHeader('Content-Type', 'application/json; charset=utf-8');
        this.end(JSON.stringify(data));
      }
    };
    
    // 调用API路由处理函数
    console.log(`调用API处理函数，游戏ID: ${gameId}`);
    try {
      gameApiHandler(req, res);
    } catch (error) {
      console.error(`API处理错误: ${error.message}`);
      res.statusCode = 500;
      res.end(`Server Error: ${error.message}`);
    }
    return;
  }
  
  // 处理根路径请求
  if (pathname === '/') {
    res.setHeader('Content-Type', 'text/html');
    res.end(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Bear Clicker Game Server</title>
        <style>
          body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
          h1 { color: #333; }
          ul { list-style-type: none; padding: 0; }
          li { margin-bottom: 10px; }
          a { color: #0066cc; text-decoration: none; }
          a:hover { text-decoration: underline; }
          .embed { color: #999; font-size: 0.8em; margin-left: 10px; }
        </style>
      </head>
      <body>
        <h1>Bear Clicker Game Server</h1>
        <p>本地测试服务器运行在端口 3006</p>
        <h2>可用游戏:</h2>
        <ul>
          ${getGamesList()}
        </ul>
      </body>
      </html>
    `);
    return;
  }
  
  // 处理其他请求
  res.statusCode = 404;
  res.end('Not found');
});

// 获取游戏列表HTML
function getGamesList() {
  try {
    const configPath = path.join(__dirname, 'config', 'games.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    
    return config.games.map(game => `
      <li>
        <a href="/${game.id}">${game.title}</a>
        <a href="/${game.id}.embed" class="embed">(embed版本)</a>
      </li>
    `).join('');
  } catch (error) {
    console.error(`加载游戏列表失败: ${error.message}`);
    return '<li>加载游戏列表失败</li>';
  }
}

// 启动服务器
const PORT = process.env.PORT || 3007;
server.listen(PORT, () => {
  console.log(`\n=== 本地服务器已启动 ===`);
  console.log(`服务器运行在: http://localhost:${PORT}`);
  console.log(`按 Ctrl+C 停止服务器\n`);
});
