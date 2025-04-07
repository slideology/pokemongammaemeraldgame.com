/**
 * 与现有项目集成的脚本
 * 用于将Vercel部署方案与现有的Bear Clicker项目集成
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 项目路径配置
const BEARCLICKER_ROOT = path.resolve(__dirname, '../../');
const VERCEL_ROOT = path.resolve(__dirname, '../');
const CONFIG_PATH = path.join(VERCEL_ROOT, 'config', 'games.json');

/**
 * 从现有项目中提取游戏信息
 */
function extractGamesFromBearClicker() {
  console.log('正在从现有项目中提取游戏信息...');
  
  const games = [];
  
  try {
    // 检查templates目录，查找所有游戏HTML文件
    const templatesDir = path.join(BEARCLICKER_ROOT, 'templates');
    if (fs.existsSync(templatesDir)) {
      // 获取templates目录下的所有HTML文件
      const files = fs.readdirSync(templatesDir)
        .filter(file => file.endsWith('.html') && !file.startsWith('base') && !file.startsWith('index'));
      
      // 遍历所有HTML文件
      for (const file of files) {
        const filePath = path.join(templatesDir, file);
        const content = fs.readFileSync(filePath, 'utf8');
        
        // 提取game_url和title
        const gameUrlMatch = content.match(/game_url="([^"]+)"/); 
        const titleMatch = content.match(/title="([^"]+)"/); 
        
        if (gameUrlMatch && titleMatch) {
          const gameUrl = gameUrlMatch[1];
          const title = titleMatch[1];
          
          // 从文件名生成ID
          const gameId = file.replace('.html', '');
          
          // 添加到游戏列表
          games.push({
            id: gameId,
            title: title,
            url: gameUrl
          });
          
          console.log(`找到游戏: ${title} (${gameId})`);
        }
      }
    }
  } catch (error) {
    console.error('提取游戏信息时出错:', error);
  }
  
  console.log(`成功提取 ${games.length} 个游戏的信息`);
  return games;
}

/**
 * 更新配置文件
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
  console.log('开始与现有项目集成...');
  
  // 确保配置目录存在
  const configDir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  // 提取游戏信息并更新配置
  const games = extractGamesFromBearClicker();
  if (games.length > 0) {
    updateConfig(games);
    console.log('集成完成！');
  } else {
    // 尝试从trending_games.html文件中提取游戏信息
    console.log('尝试从trending_games.html文件中提取游戏信息...');
    const trendingGamesPath = path.join(BEARCLICKER_ROOT, 'templates', 'components', 'trending_games.html');
    
    if (fs.existsSync(trendingGamesPath)) {
      const content = fs.readFileSync(trendingGamesPath, 'utf8');
      
      // 提取所有游戏链接和标题
      const gameLinks = content.match(/<a href="https:\/\/bearclicker\.net\/([^"]+)"[\s\S]*?<p[^>]*>[\s\S]*?<\/p>/g);
      
      if (gameLinks && gameLinks.length > 0) {
        const extractedGames = [];
        
        for (const link of gameLinks) {
          const idMatch = link.match(/<a href="https:\/\/bearclicker\.net\/([^"]+)"/); 
          const imgMatch = link.match(/alt="([^"]+) img"/); 
          
          if (idMatch) {
            const gameId = idMatch[1];
            const title = imgMatch ? imgMatch[1] : gameId.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            // 添加到游戏列表
            extractedGames.push({
              id: gameId,
              title: title,
              url: `https://stimulationclicker.com/${gameId}.embed`
            });
            
            console.log(`从trending_games.html找到游戏: ${title} (${gameId})`);
          }
        }
        
        if (extractedGames.length > 0) {
          updateConfig(extractedGames);
          console.log('集成完成！');
          return;
        }
      }
    }
    
    console.error('没有找到游戏信息，集成失败');
  }
}

// 执行主函数
main();