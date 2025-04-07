const fs = require('fs');
const path = require('path');

// 读取游戏配置文件
const config = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'config', 'games.json'), 'utf8'));

// 读取游戏模板文件
const templateContent = fs.readFileSync(path.join(process.cwd(), 'public', 'game-template.html'), 'utf8');

/**
 * 处理游戏请求的API路由函数
 * @param {Object} req - 请求对象
 * @param {Object} res - 响应对象
 */
module.exports = (req, res) => {
  try {
    // 获取请求的游戏ID
    const { gameId } = req.query;
    
    // 清理游戏ID，移除.html后缀和非法字符
    const gameIdClean = gameId ? gameId.replace(/\.html$/, '').replace(/[^a-zA-Z0-9-_]/g, '') : '';
    
    // 查找游戏配置
    const gameConfig = config.games.find(g => g.id === gameIdClean);
    
    // 如果找不到游戏配置，返回404
    if (!gameConfig) {
      return res.status(404).send('Game not found');
    }
    
    // 替换模板中的占位符
    let html = templateContent
      .replace(/{{GAME_TITLE}}/g, gameConfig.title)
      .replace(/{{GAME_URL}}/g, gameConfig.url)
      .replace(/{{DOMAIN_DISPLAY}}/g, config.brandName || 'Bear Clicker')
      .replace(/{{DOMAIN_LINK}}/g, config.brandUrl || 'https://bearclicker.net');
    
    // 设置响应头部
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=14400, s-maxage=2592000');
    
    // 发送响应
    res.status(200).send(html);
  } catch (error) {
    console.error('Error processing game request:', error);
    res.status(500).send('Internal Server Error');
  }
};
