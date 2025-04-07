/**
 * 配置更新脚本
 * 从现有的Bear Clicker项目中提取游戏信息并更新配置文件
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 项目路径配置
const BEARCLICKER_ROOT = path.resolve(__dirname, '../../');
const VERCEL_ROOT = path.resolve(__dirname, '../');
const CONFIG_PATH = path.join(VERCEL_ROOT, 'config', 'games.json');

// 游戏源目录
const GAMES_DIR = path.join(BEARCLICKER_ROOT, 'static', 'games');

/**
 * 从游戏目录中提取游戏信息
 * @returns {Array} 游戏配置数组
 */
function extractGamesInfo() {
  console.log('正在从游戏目录提取游戏信息...');
  
  try {
    // 获取游戏目录列表
    const gameDirs = fs.readdirSync(GAMES_DIR)
      .filter(dir => fs.statSync(path.join(GAMES_DIR, dir)).isDirectory());
    
    // 提取每个游戏的信息
    const games = gameDirs.map(dir => {
      // 尝试读取游戏目录中的index.html文件获取标题
      let title = dir; // 默认使用目录名作为标题
      
      const indexPath = path.join(GAMES_DIR, dir, 'index.html');
      if (fs.existsSync(indexPath)) {
        const content = fs.readFileSync(indexPath, 'utf8');
        const titleMatch = content.match(/<title>(.*?)<\/title>/);
        if (titleMatch && titleMatch[1]) {
          title = titleMatch[1].replace(' - Bear Clicker', '').trim();
        }
      }
      
      return {
        id: dir,
        title: title,
        url: `https://bearclicker.com/games/${dir}/`
      };
    });
    
    console.log(`成功提取 ${games.length} 个游戏的信息`);
    return games;
  } catch (error) {
    console.error('提取游戏信息时出错:', error);
    return [];
  }
}

/**
 * 更新配置文件
 * @param {Array} games 游戏配置数组
 */
function updateConfig(games) {
  console.log('正在更新配置文件...');
  
  try {
    // 创建配置对象
    const config = {
      games: games
    };
    
    // 写入配置文件
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf8');
    
    console.log(`配置文件已更新: ${CONFIG_PATH}`);
  } catch (error) {
    console.error('更新配置文件时出错:', error);
  }
}

/**
 * 主函数
 */
function main() {
  console.log('开始更新游戏配置...');
  
  // 确保配置目录存在
  const configDir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  // 提取游戏信息并更新配置
  const games = extractGamesInfo();
  if (games.length > 0) {
    updateConfig(games);
  } else {
    console.error('没有找到游戏信息，配置未更新');
  }
}

// 执行主函数
main();
