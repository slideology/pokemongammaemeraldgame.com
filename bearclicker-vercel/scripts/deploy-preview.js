/**
 * 本地预览脚本
 * 用于在本地测试Vercel项目
 */

const { execSync } = require('child_process');
const path = require('path');
const http = require('http');
const fs = require('fs');
const { parse } = require('url');

// 项目路径
const PROJECT_DIR = path.resolve(__dirname, '..');

// 游戏配置
const CONFIG_PATH = path.join(PROJECT_DIR, 'config', 'games.json');
const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));

// API处理函数
const apiHandler = require(path.join(PROJECT_DIR, 'api', '[gameId].js'));

/**
 * 启动本地预览服务器
 */
function startPreviewServer() {
  let PORT = 3006;
  
  // 检查端口是否被占用
  function isPortAvailable(port) {
    try {
      const server = http.createServer();
      server.listen(port, '127.0.0.1');
      server.close();
      return true;
    } catch (e) {
      return false;
    }
  }
  
  // 如果端口3000被占用，尝试其他端口
  if (!isPortAvailable(PORT)) {
    for (let i = 3001; i < 3010; i++) {
      if (isPortAvailable(i)) {
        PORT = i;
        break;
      }
    }
    console.log(`端口3006已被占用，将使用端口${PORT}`);
  }
  
  // 创建HTTP服务器
  const server = http.createServer((req, res) => {
    const { pathname } = parse(req.url, true);
    
    // 处理静态文件
    if (pathname.startsWith('/public/')) {
      const filePath = path.join(PROJECT_DIR, pathname);
      if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        const content = fs.readFileSync(filePath);
        res.writeHead(200);
        res.end(content);
        return;
      }
    }
    
    // 处理API请求
    const gameId = pathname.substring(1); // 移除开头的'/'
    
    // 模拟 Vercel 的请求和响应对象
    const mockReq = {
      query: { gameId },
      headers: req.headers
    };
    
    const mockRes = {
      status: (code) => {
        res.statusCode = code;
        return mockRes;
      },
      setHeader: (name, value) => {
        res.setHeader(name, value);
        return mockRes;
      },
      send: (body) => {
        res.end(body);
        return mockRes;
      }
    };
    
    // 调用API处理函数
    apiHandler(mockReq, mockRes);
  });
  
  // 启动服务器
  server.listen(PORT, () => {
    console.log(`本地预览服务器已启动: http://localhost:${PORT}`);
    console.log('可用的游戏链接:');
    
    // 显示可用的游戏链接
    config.games.forEach(game => {
      console.log(`- ${game.title}: http://localhost:${PORT}/${game.id}`);
    });
    
    console.log('按 Ctrl+C 停止服务器');
  });
}

/**
 * 主函数
 */
function main() {
  console.log('开始准备本地预览...');
  
  // 注释掉更新配置的步骤，因为我们已经通过integrate-with-bearclicker.js提取了游戏信息
  // try {
  //   console.log('正在更新游戏配置...');
  //   execSync('node scripts/update-config.js', { stdio: 'inherit', cwd: PROJECT_DIR });
  // } catch (error) {
  //   console.warn('更新游戏配置时出错，使用现有配置继续...');
  // }
  console.log('使用现有配置启动预览服务器...');
  
  // 检查配置文件是否存在
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error(`配置文件不存在: ${CONFIG_PATH}`);
    console.log('请先运行 integrate-with-bearclicker.js 脚本提取游戏信息');
    process.exit(1);
  }

  // 启动预览服务器
  startPreviewServer();
}

// 执行主函数
main();
