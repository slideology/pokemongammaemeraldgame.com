from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, session, g
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import json
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'bearclicker-secret-key-2024')

# 导入日志配置
from config.logging_config import setup_logging

# 设置日志系统
setup_logging(app)

def get_translations():
    """Get translations dictionary."""
    try:
        translations_path = os.path.join(app.static_folder, 'data', 'translations.json')
        with open(translations_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            return translations.get('en', {})
    except Exception as e:
        app.logger.error(f"Error getting translations: {e}")
        return {
            'nav': {
                'home': 'Home',
                'guide': 'Game Guide',
                'faq': 'FAQ',
                'play': 'Play',
                'about': 'About',
                'contact': 'Contact',
                'games': 'Games'
            },
            "hero": {
                "title_highlight": "Create Music",
                "title_regular": "Like Never Before",
                "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
            },
            "game": {
                "title": "Bear Clicker",
                "subtitle": "The Ultimate Bear Clicker Game",
                "description": "Unleash haunting melodies with our special glitch music system. Stack sounds, witness their digital distortion transformation. Embrace Horror Aesthetics."
            },
            "trending": {
                "title": "Trending Games",
                "bear_lily": "Bear - Lily",
                "bear_megalovania": "Bear - Megalovania",
                "bear_spruted": "Bear - Spruted"
            }
        }

def load_faqs():
    """
    从JSON文件加载FAQ数据
    
    Returns:
        dict: FAQ数据字典
    """
    try:
        faqs_path = os.path.join(app.static_folder, 'data', 'faqs.json')
        
        with open(faqs_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading FAQs: {e}")
        # 返回空字典作为默认值
        return {}

def get_faqs_for_page(page_name):
    """
    获取特定页面的FAQ数据
    
    Args:
        page_name (str): 页面名称
        
    Returns:
        dict: 包含FAQ问答和结论的字典
    """
    faqs_data = load_faqs()
    
    # 如果找不到对应页面的FAQ，返回默认值
    if page_name not in faqs_data:
        return {
            'faqs': [],
            'conclusion': ''
        }
    
    return faqs_data[page_name]

@app.route('/')
def home():
    translations_data = get_translations()
    faq_data = get_faqs_for_page('index')  
    return render_template('index.html',
                         page_title='Bear Clicker',
                         title='Bear Clicker - Interactive Music Experience',
                         description='Create amazing music with Bear Clicker! Mix beats, compose tunes, and share your musical creations.',
                         translations=translations_data,
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'])

@app.route('/about')
def about():
    try:
        trans = get_translations()
        return render_template('about.html', 
                         title='About Bear Clicker',
                         translations=trans)
    except Exception as e:
        app.logger.error(f"Error in about route: {e}")
        return render_template('about.html',
                         title='About Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         })

@app.route('/game')
def game():
    try:
        trans = get_translations()
        return render_template('game.html',
                         title='Play Bear Clicker',
                         translations=trans)
    except Exception as e:
        app.logger.error(f"Error in game route: {e}")
        return render_template('game.html',
                         title='Play Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         })

@app.route('/introduction')
def introduction():
    try:
        trans = get_translations()
        return render_template('introduction.html',
                         title='Game Guide - Bear Clicker',
                         translations=trans)
    except Exception as e:
        app.logger.error(f"Error in introduction route: {e}")
        return render_template('introduction.html',
                         title='Game Guide - Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         })

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        trans = get_translations()
        if request.method == 'POST':
            return send_message()
        return render_template('contact.html',
                         title='Contact Bear Clicker',
                         translations=trans)
    except Exception as e:
        app.logger.error(f"Error in contact route: {e}")
        return render_template('contact.html',
                         title='Contact Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         })

@app.route('/faq')
def faq():
    try:
        trans = get_translations()
        faq_data = get_faqs_for_page('index')  # 使用index页面的FAQ数据
        return render_template('faq.html',
                         title='FAQ - Bear Clicker',
                         page_title='Bear Clicker',
                         translations=trans,
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'])
    except Exception as e:
        app.logger.error(f"Error in faq route: {e}")
        return render_template('faq.html',
                         title='FAQ - Bear Clicker',
                         page_title='Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         dynamic_faqs=[],
                         conclusion="No FAQ data available at this time.")

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/capybara-clicker')
def capybara_clicker():
    faq_data = get_faqs_for_page('capybara-clicker')
    return render_template('capybara-clicker.html',
                         page_title='Capybara Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/stimulation-clicker')
def stimulation_clicker():
    faq_data = get_faqs_for_page('stimulation-clicker')
    return render_template('stimulation-clicker.html',
                         page_title='Stimulation Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations()) 
@app.route('/unchill-guy-clicker')
def unchill_guy_clicker():
    faq_data = get_faqs_for_page('unchill-guy-clicker')
    return render_template('unchill-guy-clicker.html',
                         page_title='Unchill Guy Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations()) 

@app.route('/chill-girl-clicker')
def chill_girl_clicker():
    faq_data = get_faqs_for_page('chill-girl-clicker')
    return render_template('chill-girl-clicker.html',
                         page_title='Chill Girl Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations()) 
@app.route('/chill-clicker')
def chill_clicker():
    faq_data = get_faqs_for_page('chill-clicker')
    return render_template('chill-clicker.html',
                         page_title='Chill Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())                     

@app.route('/cat-clicker')
def cat_clicker():
    faq_data = get_faqs_for_page('cat-clicker')
    return render_template('cat-clicker.html',
                         page_title='Cat Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/ice-cream-clicker')
def ice_cream_clicker():
    faq_data = get_faqs_for_page('ice-cream-clicker')
    return render_template('ice-cream-clicker.html',
                         page_title='Ice Cream Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/panda-clicker')
def panda_clicker():
    faq_data = get_faqs_for_page('panda-clicker')
    return render_template('panda-clicker.html',
                         page_title='Panda Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/planet-clicker')
def planet_clicker():
    faq_data = get_faqs_for_page('planet-clicker')
    return render_template('planet-clicker.html',
                         page_title='Planet Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/tube-clicker')
def tube_clicker():
    faq_data = get_faqs_for_page('tube-clicker')
    return render_template('tube-clicker.html',
                         page_title='Tube Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/titans-clicker')
def titans_clicker():
    faq_data = get_faqs_for_page('titans-clicker')
    return render_template('titans-clicker.html',
                         page_title='Titans Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())                      

@app.route('/kiwi-clicker')
def kiwi_clicker():
    faq_data = get_faqs_for_page('kiwi-clicker')
    return render_template('kiwi-clicker.html',
                         page_title='Kiwi Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())                     

@app.route('/muscle-clicker')
def muscle_clicker():
    faq_data = get_faqs_for_page('muscle-clicker')
    return render_template('muscle-clicker.html',
                         page_title='Muscle Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/money-clicker')
def money_clicker():
    faq_data = get_faqs_for_page('money-clicker')
    return render_template('money-clicker.html',
                         page_title='Money Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-clicker')
def sprunki_clicker():
    faq_data = get_faqs_for_page('sprunki-clicker')
    return render_template('sprunki-clicker.html',
                         page_title='Sprunki Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cookie-clicker')
def cookie_clicker():
    faq_data = get_faqs_for_page('cookie-clicker')
    return render_template('cookie-clicker.html',
                         page_title='Cookie Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())                     
@app.route('/paper')
def paper():
    # 读取文档数据
    with open('static/data/paper.json', 'r', encoding='utf-8') as f:
        paper_data = json.load(f)
    return render_template('paper.html', paper=paper_data)

@app.route('/privacy-policy')
def privacy_policy():
    try:
        translations_data = get_translations()
        return render_template('privacy-policy.html', translations=translations_data)
    except Exception as e:
        app.logger.error(f"Error in privacy policy route: {e}")
        return render_template('error.html', error="An error occurred loading the privacy policy page.")

@app.route('/terms-of-service')
def terms_of_service():
    try:
        translations_data = get_translations()
        return render_template('terms-of-service.html', translations=translations_data)
    except Exception as e:
        app.logger.error(f"Error in terms of service route: {e}")
        return render_template('error.html', error="An error occurred loading the terms of service page.")

def send_message():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([name, email, subject, message]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('contact'))
        
        try:
            email_user = os.getenv('EMAIL_USER')
            email_password = os.getenv('EMAIL_PASSWORD')
            
            if not email_user or not email_password:
                flash('Email configuration is not set up', 'error')
                return redirect(url_for('contact'))
            
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_user  # Send to yourself
            msg['Subject'] = f"Sprunkr: {subject} - from {name}"
            
            body = f"""
            Name: {name}
            Email: {email}
            Subject: {subject}
            Message: {message}
            """
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
            server.quit()
            
            flash('Thank you for your message! We will get back to you soon.', 'success')
        except Exception as e:
            app.logger.error(f"Error sending message: {str(e)}")
            flash('Sorry, there was a problem sending your message. Please try again later.', 'error')
    except Exception as e:
        app.logger.error(f"Error in send_message: {e}")
        flash('Sorry, there was a problem sending your message. Please try again later.', 'error')
    
    return redirect(url_for('contact'))

# 添加全局错误处理器
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return render_template('error.html', 
                         error_code=500,
                         error_message="Internal Server Error",
                         translations=get_translations()), 500

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f'Page not found: {error}')
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page Not Found",
                         translations=get_translations()), 404

if __name__ == '__main__':
    app.run(debug=True, port=5002)
