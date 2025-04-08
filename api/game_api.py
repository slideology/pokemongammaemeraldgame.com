from flask import request, redirect, render_template_string
import json
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 读取游戏配置文件
def load_game_config():
    try:
        # 首先尝试从新路径加载
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'game-config', 'games.json')
        logger.info(f"尝试从新路径读取配置文件: {config_path}")
        
        # 如果新路径不存在，尝试从原始路径加载
        if not os.path.exists(config_path):
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bearclicker-vercel', 'config', 'games.json')
            logger.info(f"尝试从原始路径读取配置文件: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"配置加载成功, 包含 {len(config['games'])} 个游戏")
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        return {"games": [], "brandName": "Bear Clicker", "brandUrl": "https://bearclicker.net"}

# 读取游戏模板文件
def load_template():
    try:
        # 首先尝试从新路径加载
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'game-templates', 'game-template.html')
        logger.info(f"尝试从新路径读取模板文件: {template_path}")
        
        # 如果新路径不存在，尝试从原始路径加载
        if not os.path.exists(template_path):
            template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bearclicker-vercel', 'public', 'game-template.html')
            logger.info(f"尝试从原始路径读取模板文件: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        logger.info("模板加载成功")
        return template_content
    except Exception as e:
        logger.error(f"加载模板文件失败: {str(e)}")
        return '<!DOCTYPE html><html><body><h1>Error loading template</h1></body></html>'

# 游戏API处理函数
def game_api(game_id=None):
    try:
        # 记录请求信息
        logger.info("\n--- 新请求 ---")
        logger.info(f"请求URL: {request.url}")
        logger.info(f"请求方法: {request.method}")
        logger.info(f"请求域名: {request.host}")
        
        # 加载配置和模板
        config = load_game_config()
        template_content = load_template()
        
        logger.info(f"配置域名: {config.get('domain', 'game.bearclicker.net')}")
        logger.info(f"Referer: {request.referrer or 'none'}")
        logger.info(f"User-Agent: {request.user_agent.string}")
        
        # 如果没有传入game_id，则从查询参数中获取
        if game_id is None:
            game_id = request.args.get('gameId')
        logger.info(f"原始游戏ID: {game_id}")
        
        # 清理游戏ID，移除.html后缀和非法字符
        if game_id:
            game_id_clean = game_id.replace('.html', '')
            # 移除非字母、数字、连字符和下划线的字符
            game_id_clean = ''.join(c for c in game_id_clean if c.isalnum() or c in '-_')
        else:
            game_id_clean = ''
        logger.info(f"清理后的游戏ID: {game_id_clean}")
        
        # 查找游戏配置
        game_config = next((g for g in config['games'] if g['id'] == game_id_clean), None)
        
        # 如果找不到游戏配置，返回404
        if not game_config:
            logger.info(f"未找到游戏配置: {game_id_clean}")
            return f"Game not found: {game_id_clean}", 404
        
        logger.info(f"找到游戏: {game_config['title']}")
        logger.info(f"游戏URL: {game_config['url']}")
        

        
        # 检查请求路径
        logger.info(f"请求路径: {request.path}")
        
        # 检查是否是本地测试环境
        is_local_testing = request.host in ['localhost:3007', '127.0.0.1:3007']
        logger.info(f"是否本地测试: {is_local_testing}")
        
        # 如果是本地测试环境，使用游戏模板
        # 如果是线上环境，则根据路径判断：/game/前缀的请求使用游戏模板
        is_game_request = is_local_testing or request.path.startswith('/game/')
        logger.info(f"是否游戏请求: {is_game_request}")
        
        # 如果不是游戏请求，重定向到主站对应的页面
        if not is_game_request and not is_local_testing:
            redirect_url = f"{config.get('brandUrl', 'https://bearclicker.net')}/{game_id_clean}"
            logger.info(f"非游戏请求，重定向到主站: {redirect_url}")
            return redirect(redirect_url, code=302)
        
        # 替换模板中的占位符
        html = template_content
        html = html.replace('{{GAME_TITLE}}', game_config['title'])
        html = html.replace('{{GAME_URL}}', game_config['url'])
        html = html.replace('{{DOMAIN_DISPLAY}}', config.get('brandName', 'Bear Clicker'))
        html = html.replace('{{DOMAIN_LINK}}', config.get('brandUrl', 'https://bearclicker.net'))
        
        # 添加调试信息到HTML
        debug_info = f"""
          <!-- Debug Info:
          Request URL: {request.url}
          Game ID: {game_id_clean}
          Game Title: {game_config['title']}
          Game URL: {game_config['url']}
          Host: {request.host}
          Timestamp: {__import__('datetime').datetime.now().isoformat()}
          -->
        """
        html = html.replace('</head>', f"{debug_info}</head>")
        
        logger.info('响应准备完成，发送HTML')
        
        # 返回HTML响应
        return html
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        logger.exception(e)
        return f"Internal Server Error: {str(e)}", 500
