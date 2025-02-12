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

def get_faqs_for_page(page_name):
    faqs_data = {
        'banana': {
            'faqs': [
                {
                    'question': 'What is Sprunki Banana?',
                    'answer': 'Sprunki Banana is a unique mod featuring banana-themed characters and tropical soundscapes in the Sprunki universe.'
                },
                {
                    'question': 'What makes Banana mod special?',
                    'answer': 'The Banana mod brings a fun and tropical twist to Sprunki, with unique sound effects and cheerful character designs.'
                },
                {
                    "question": "What makes the Sprunki Sprungle Banana Mod special?",
                    "answer": "It brings a whimsical twist to classic Sprunki gameplay by immersing players in a banana-themed world. Every Sprunki character is transformed into vibrant yellow avatars with banana-inspired outfits, accessories, and animations, accompanied by lighthearted sound effects and fun melodies."
                },
                {
                    "question": "How do you play the Sprunki Sprungle Banana Mod?",
                    "answer": "To play, first select characters by dragging and dropping banana-themed Sprunki avatars onto the stage to create your unique mix. Then build tracks by combining different characters to layer beats, melodies, and effects for a tropical-inspired musical experience. Also, discover bonuses by experimenting with various combinations and save and share your fun, banana-infused tracks with the Sprunki community."
                },
                {
                    "question": "What are the features of the Sprunti Sprungle Banana Mod?",
                    "answer": "The features include banana-themed characters that are creatively redesigned with banana-inspired visuals, tropical sound effects that are upbeat and cheerful tunes adding a sunny vibe to your compositions, a bright aesthetic with a vibrant yellow interface enhancing the playful theme, and interactive gameplay allowing you to explore the joy of mixing lighthearted sounds in a fresh, fruity setting."
                },
                {
                    "question": "Why is the Sprunki Sprungle Banana Mod suitable for some players?",
                    "answer": "It's a fun and cheerful take on the Sprunki universe, perfect for players seeking a lighthearted musical adventure!"
                }
            ],
            'conclusion': 'Sprunki Banana offers a delightful and tropical musical experience that stands out in the Sprunki universe.'
        },
        'garnold': {
            'faqs': [
                {
                    'question': 'Who is Garnold in Sprunki?',
                    'answer': 'Garnold (Gold) is one of the main characters in Sprunki, known for his distinctive golden appearance and unique sound effects.'
                },
                {
                    'question': 'What are Garnold\'s special features?',
                    'answer': 'Garnold brings unique golden-themed sound effects and visual elements to the game, creating a premium music experience.'
                }
            ],
            'conclusion': 'Garnold adds a touch of golden luxury to the Sprunki universe with his unique sound effects and visual elements.'
        },
        'ketchup': {
            'faqs': [
                {
                    'question': 'What is Sprunki Ketchup mod?',
                    'answer': 'Sprunki Ketchup is a creative mod that adds a fun food-themed twist to the game with unique characters and sounds.'
                },
                {
                    'question': 'What makes Ketchup mod unique?',
                    'answer': 'The Ketchup mod features food-inspired characters and sound effects, creating a playful and appetizing musical experience.'
                },
                {
                    "question": "What new aspects does Sprunki Ketchup 2 Mod bring compared to its predecessor?",
                    "answer": "Sprunki Ketchup 2 Mod ventures deeper into the unsettling realm, heightening the horror elements and tension. The atmosphere is darker, the visuals are more haunting, and the loops are more unnerving. It replaces catchy beats with eerie whispers, hollow tones, and unsettling rhythms."
                },
                {
                    "question": "What are the key features of Sprunki Ketchup 2 Mod?",
                    "answer": "The key features include intensified horror aesthetics with characters having a more menacing look, sharper silhouettes, ominous color schemes, and disquieting animations. It also has darker soundscapes with loops and effects like distant shrieks, low drones, and heart-thumping percussion, and heightened suspense that makes every arrangement feel like a step into the unknown."
                },
                {
                    "question": "How do you play Sprunki Ketchup 2 Mod?",
                    "answer": "To play, first select characters that seem haunted, each representing loops from quietly unnerving to outright chilling. Then drag and drop them on the screen to layer spooky elements until your track hums with tension. After that, experiment and refine by adjusting volumes, adding effects, and shuffling characters. Finally, save and share your haunting composition with other brave players."
                },
                {
                    "question": "Why would players choose to play Sprunki Ketchup 2 Mod?",
                    "answer": "Players who enjoy a challenging and spooky music-making experience, and those who want to explore the intensified horror elements and share their creations with like-minded brave players would choose this mod."
                }
            ],
            'conclusion': 'Sprunki Ketchup brings a tasty twist to music creation with its food-themed characters and sounds.'
        },
        'lily': {
            'faqs': [
                {
                    'question': 'Who is Lily in Sprunki?',
                    'answer': 'Lily is a beloved character in the Sprunki universe, bringing a unique blend of floral themes and melodic sounds.'
                },
                {
                    'question': 'What are Lily\'s special features?',
                    'answer': 'Lily\'s mod includes nature-inspired sounds and visual elements, creating a peaceful and harmonious musical atmosphere.'
                },
                {
                    "question": "Where can I find most of the Spurunki Lily features?",
                    "answer": "Most features are in the settings menu, so you should go there."
                },
                {
                    "question": "What are the transparent icons in the Spurunki Lily and how can I toggle them?",
                    "answer": "The transparent icons are experimental icons. You can toggle them by pressing [\], or typing 'imsosprunki'."
                },
                {
                    "question": "How can I change the flash speed in the Spurunki Lily game?",
                    "answer": "You can change the flash speed by holding L and pressing the arrow keys."
                },
                {
                    "question": "What happens when I re-focus the Spurunki Lily window?",
                    "answer": "There is a 1 in 5 chance when you re-focus the window, the phase switches."
                },
                {
                    "question": "How can I set a custom speed in the Spurunki Lily game?",
                    "answer": "If you shift-click the speed button, you can set a custom speed!"
                },
                {
                    "question": "How do I remove the characters on the stage of the Spurunki Lily game?",
                    "answer": "Shift + Delete removes the characters up on the stage. Also, shift-click the switch button to remove the characters as well."
                },
                {
                    "question": "How do I turn on advanced mode in the Spurunki Lily game?",
                    "answer": "Shift-click the info button to turn on advanced mode."
                },
                {
                    "question": "How can I add a new costume for the custom cursor in the Spurunki Lily game?",
                    "answer": "Control-click the custom cursor button to add a new costume."
                },
                {
                    "question": "How can I switch my custom cursor and rearrange the downloaded cursors in the Spurunki Lily game?",
                    "answer": "Hold C and the arrow keys to switch your custom cursor. Shift-click to rearrange the downloaded cursors."
                },
                {
                    "question": "What's the plan for the goreless characters in Phase 2 in the Spurunki Lily game?",
                    "answer": "The goreless characters in Phase 2 are planned to have gore, or survive. That is the characters will receive that in any later update. (Don't take this the wrong way)"
                },
                {
                    "question": "How up-to-date is the game description in the Spurunki Lily game?",
                    "answer": "The description of this game is accordingly up to date of unreleased updates."
                },
                {
                    "question": "How can I undo spawned character in the Spurunki Lily game?",
                    "answer": "Shift-click the spawn character button to undo spawned character."
                },
                {
                    "question": "What should I do when starting a polo to stack in the Spurunki Lily game?",
                    "answer": "Press Control while starting a polo to stack."
                },
                {
                    "question": "What are the names of the extra characters and in what order in the Spurunki Lily game?",
                    "answer": "Extra Characters' Names in order: Turquoise (Tyla), Dark purple (Evi, Evelyn), Saturated orange (SmithTails), Rose (Ellie), Lilac (Lily), Cream/Butter (Smol, Butterscotch), Brownish gray (Estyne, grud), White (Baba), Dark purple (Elpruia), Light blurple (Elprud), Dark indigo (Echo), Cyan (Bubbles), Tan (Izuku Midoriya, Deku), Purple (Iridiana)"
                },
                {
                    "question": "How do I open the file to play in the Spurunki Lily game?",
                    "answer": "To open the file, use Turbowarp and load the file in the editor by pressing 'File', then 'Load from your computer'. Locate the file and load it. Then, play!"
                }
            ],
            'conclusion': 'Lily brings a touch of natural beauty and harmony to the Sprunki universe.'
        },
        'fiddlebops': {
            'faqs': [
                {
                    "question": "What is FiddleBops?",
                    "answer": "FiddleBops is a fan-made project inspired by the Incredibox universe, hosted on PlayMiniGames. It's an interactive music creator that combines imaginative storytelling, unique characters, and dynamic gameplay for an exciting musical adventure."
                },
                {
                    "question": "Why should one play the FiddleBops game?",
                    "answer": "One should play it because of its unique characters with distinct personalities and sounds, fresh narratives beyond Incredibox lore, enhanced gameplay with storytelling elements, being free to play online without downloads, and having a vibrant community for engagement and collaboration."
                },
                {
                    "question": "How is the gameplay of Sprunki FiddleBops?",
                    "answer": "To play, first choose your characters from the lineup. Then use drag and drop to build your track and remove characters by dragging them down or double-clicking. You can enhance tracks by adjusting pitch, layering sounds, etc. Also, explore narratives as you hit milestones and save and share your tracks with the community."
                },
                {
                    "question": "What are the key features of FiddleBops?",
                    "answer": "The key features include original characters with unique sound profiles, an expanded sound library with a wide range of musical elements, interactive storytelling where musical choices affect narratives, the ability to remix and collaborate, and being community-friendly for sharing and participating in challenges."
                },
                {
                    "question": "What are the benefits of playing FiddleBops?",
                    "answer": "The benefits are boosting creativity in music-making, improving cognitive skills like memory and problem-solving, building connections with a community of music enthusiasts, having free accessibility to play online, and enjoying endless fun with limitless remix options."
                }
            ],
            'conclusion': 'FiddleBops, a fan-made gem inspired by Incredibox! an interactive music creator. meet unique characters, and engage in dynamic gameplay.'
        },
        'megalovania': {
            'faqs': [
                {
                    'question': 'What is Sprunki Megalovania?',
                    'answer': 'Sprunki Megalovania is an epic crossover mod that brings the iconic Undertale track into the Sprunki universe.'
                },
                {
                    'question': 'How does Megalovania mod work?',
                    'answer': 'This mod allows players to create remixes and variations of the famous Megalovania theme using Sprunki\'s unique sound system.'
                },
                {
                    "question": "What is special about Sprunki MEGALOVANIA Mod?",
                    "answer": "Sprunki MEGALOVANIA Mod brings the iconic 'Megalovania' track into the Sprunki universe, transforming the standard Sprunki environment into a high-octane music lab where characters and loops pay homage to the track's signature intensity."
                },
                {   
                    "question": "What are the key features of Sprunki MEGALOVANIA Mod?",
                    "answer": "The key features include Megalovania-Themed Characters where each represents a sonic element like driving percussion, eerie synth lines, and rapid-fire motifs. It also has High-Energy Soundscapes that encourage experimenting with fast beats, bold melodies, and layered harmonies, and a Distinct Visual Flair with flashes of bold colors and references for a dynamic experience."
                },
                {
                    "question": "How do you play Sprunki MEGALOVANIA Mod?",
                    "answer": "To play, first select characters from a cast aligned with Megalovania's pacing and tonality. Then drag and drop them to form loops that echo the tune's famous patterns or create new variations. After that, refine your mix by adjusting volumes and effects to balance intensity with clarity. Finally, save and share your Megalovania-inspired masterpiece with the community."
                },
                {
                    "question": "Why would players be interested in Sprunki MEGALOVANIA Mod?",
                    "answer": "Players would be interested because it allows them to craft their own twists on the legendary 'Megalovania' theme, combining the excitement of the original composition with the creative freedom in the Sprunki universe, and share their unique creations with the community."
                }
            ],
            'conclusion': 'Experience the legendary Megalovania in a whole new way with this unique Sprunki mod.'
        },
        'parodybox': {
            'faqs': [
                {
                    "question": "What is Parodybox Sprunki?",
                    "answer": "Parodybox Sprunki is a creative music remix game where you can mix different character sounds and beats to create unique musical compositions. It has both Normal and Horror modes with distinctive characters and sounds."
                },
                {
                    "question": "How do I play Parodybox Sprunki?",
                    "answer": "Simply click on different characters to add their unique sounds to the mix. You can combine multiple characters to create your own musical masterpiece. Try both Normal and Horror modes for different experiences."
                },
                {
                    "question": "Is Parodybox Sprunki free to play?",
                    "answer": "Yes! Parodybox Sprunki is completely free to play in your web browser. No downloads or installations are required."
                },
                {
                    "question": "Can I create my own Sprunki mods?",
                    "answer": "Yes! The community actively creates and shares custom mods. You can create your own characters, animations, and sounds to share with other players."
                },
                {
                    "question": "What's the difference between Normal and Horror modes?",
                    "answer": "Normal mode features cheerful melodies and upbeat characters, while Horror mode transforms the experience with darker themes, unique animations, and spooky sound effects."
                },
                {
                    "question": "Who are the main characters in Sprunki?",
                    "answer": "Popular characters include Clukr, Wenda, OWAKCX, Durple, and many others. Each character has their own unique sounds and animations in both Normal and Horror modes."
                },
                {
                    "question": "How can I share my Parodybox creations?",
                    "answer": "You can record your mixes and share them with the community through our platform or social media. Many players also create videos showcasing their creative remixes."
                },
                {
                    "question": "What are the system requirements?",
                    "answer": "Parodybox Sprunki runs in any modern web browser with audio support. Make sure your sound is enabled for the best experience."
                },
                {
                    "question": "Can I play Parodybox Sprunki offline?",
                    "answer": "Currently, Parodybox Sprunki requires an internet connection to play as it's a browser-based game. However, you can access it from any device with a web browser."
                },
                {
                    "question": "How often are new mods released?",
                    "answer": "The Parodybox Sprunki community regularly creates and shares new mods. Check our community section frequently to discover the latest fan-made content and updates."
                }
            ],
            'conclusion': 'Join the Sprunki community and start creating your own unique music today!'
        },
        'pyramixed': {
            'faqs': [
                {
                    'question': 'What is PyraMixed?',
                    'answer': 'PyraMixed is a unique version that combines pyramid-themed elements with music creation, offering a distinctive visual and audio experience.'
                },
                {
                    'question': 'What makes PyraMixed special?',
                    'answer': 'PyraMixed features Egyptian-inspired characters, desert soundscapes, and mystical themes that create an immersive musical journey.'
                },
                {
                    "question": "What makes Sprunki Pyramixed Mod unique?",
                    "answer": "Sprunki Pyramixed Mod introduces a twist to the Sprunki universe with characters and themes inspired by ancient pyramids and Egyptian culture, blending music-making gameplay with a mysterious and historical aesthetic for an immersive experience."
                },
                {
                    "question": "How can I unlock the locked character in Sprunki Pyramixed Mod?",
                    "answer": "Write a Pyramix in the below bar to unlock the Sprunki Pyramixed Character."
                },
                {
                    "question": "What are the features of Sprunki Pyramixed Game?",
                    "answer": "The features include Ancient-Themed Characters designed with pyramid-inspired outfits, symbols, and animations and having unique sound loops; Mystical Soundscapes inspired by ancient Egyptian music; Atmospheric Visuals with desert backdrops, pyramids, and golden tones; and Interactive Gameplay that encourages sound combination experimentation."
                },
                {
                    "question": "How do you play Sprunki Pyramixed Mod?",
                    "answer": "To play, first select characters from the pyramid-inspired roster with distinct sound loops and animations. Then drag and drop them on the stage to layer melodies, rhythms, and effects into cohesive compositions. After that, experiment and adjust by mixing loops creatively, exploring sound combinations, and adjusting volumes to create tracks with a mystical vibe. Finally, save and share your creations with the Sprunki community."
                },
                {
                    "question": "Why is Sprunki Pyramixed Mod suitable for certain fans?",
                    "answer": "It's suitable for fans seeking a blend of history and creativity in their music-making adventures as it allows them to uncover the mysteries of the pyramids through sound and imagination."
                }
            ],
            'conclusion': 'Discover the mysteries of ancient Egypt through music with PyraMixed.'
        },
        'retake-but-human': {
            'faqs': [
                {
                    'question': 'What is Retake But Human mod?',
                    'answer': 'Retake But Human is a unique mod that reimagines Sprunki characters with a more humanized approach.'
                },
                {
                    'question': 'What makes this Retake But Human mod different?',
                    'answer': 'This mod offers a fresh perspective on familiar characters, with human-like characteristics while maintaining the core Sprunki experience.'
                },
                {
                    "question": "What are the main features of the Sprunki But Human (ALL CHARACTERS) Mod?",
                    "answer": "The main features include humanized characters, where each beloved Sprunki character is redesigned as a human with unique outfits, expressions, and styles inspired by their originals. It also has enhanced visuals, providing detailed and realistic elements while keeping core personalities intact. Additionally, there's a familiar soundscape with a twist, as the sounds stay true to the classic Sprunki vibes but blend with a touch of realism."
                },
                {
                    "question": "How do you play the Sprunki But Human (ALL CHARACTERS) Mod?",
                    "answer": "To play, first select characters from a variety of newly humanized ones, each bringing a unique musical sound. Then, drag and drop sounds to your chosen characters to create your own music mix. Finally, combine humanized characters and sounds to explore a realistic yet classic Sprunki experience."
                },
                {
                    "question": "Why is the Sprunki But Human (ALL CHARACTERS) Mod appealing to players?",
                    "answer": "This mod is appealing because it offers a new way for players to connect with the Sprunki characters they know and love. By reimagining the cast as human, it adds a creative twist, bringing depth and relatability to the iconic Incredibox style, making it engaging for both new and longtime fans."
                },
                {
                    "question": "What kind of visual changes does the Sprunki But Human (ALL CHARACTERS) Mod bring?",
                    "answer": "The mod brings enhanced visuals. It transforms all the quirky, animated Sprunki characters into lifelike human forms, adding a new visual dimension. The humanized characters have detailed designs with unique outfits, expressions, and styles that are inspired by their original forms."
                },
                {
                    "question": "How does the soundscape in the Sprunki But Human (ALL CHARACTERS) Mod differ from the original?",
                    "answer": "While the characters have taken on a human look, the sounds in the Sprunki But Human (ALL CHARACTERS) Mod stay true to the classic Sprunki vibes. It blends iconic beats with a touch of realism, maintaining familiarity while adding something new."
                }
            ],
            'conclusion': 'Experience Sprunki characters in a whole new light with the Retake But Human mod.'
        },
        'sprunksters': {
            'faqs': [
                {
                    "question": "What is Sprunki Sprunksters?",
                    "answer": "Sprunki Sprunksters is a platform that revolutionizes music creation. It combines advanced sound engineering with intuitive gameplay, offering a rewarding experience for musicians of all levels. It has a carefully designed interface and an extensive sound library to foster creativity."
                },
                {
                    "question": "What makes Sprunki Sprunksters special?",
                    "answer": "It has an extensive sound library, unique characters, a user - friendly mixing interface, a vibrant community, and a thoughtful design that provides an accessible entry point while maintaining depth for advanced exploration."
                },
                {
                    "question": "How do you play Sprunki Sprunksters?",
                    "answer": "First, discover your voice by exploring the diverse characters for unique sonic elements. Then, craft your mix by blending sound elements. Next, experiment with combinations to find unique harmonies. Refine your work to capture your artistic vision, and finally, showcase your creation in the community."
                },
                {
                    "question": "What are the essential tips for playing Sprunki Sprunksters?",
                    "answer": "Start simple, experiment freely, draw inspiration from other creators, and appreciate the journey of musical expression."
                },
                {
                    "question": "What can players do in the Sprunki Sprunksters community?",
                    "answer": "Players can collaborate with others, share their musical creations, participate in community events, and engage with fellow artists to enrich their experience and strengthen the community."
                },
                {
                    "question": "What are the latest updates and news for Sprunki Sprunksters?",
                    "answer": "There are regular content updates like new characters, sound collections, and time - limited challenges. The team also innovates with new features and engaging community activities."
                }
            ],
            'conclusion': 'Sprunki Sprunksters captivates players with its blend of innovation and accessibility. It has an enthusiastic community and welcomes all forms of musical creativity from beginners to experts.'
        },
        'agents': {
            'faqs': [
                {
                    "question": "What is Sprunkis Agent Mod?",
                    "answer": "Sprunkis Agent Mod brings a spy - inspired twist to the Sprunki universe. It transforms characters into secret agents with sleek designs, mysterious personas, and action - packed soundscapes, immersing players in an espionage - themed world for the music - making experience."
                },
                {
                    "question": "What are the features of Sprunki Agent Game?",
                    "answer": "The features include agent - themed characters reimagined as secret agents with unique sound loops, stealthy soundscapes with tense rhythms and suspenseful melodies, dynamic visuals creating an immersive spy atmosphere, and exciting gameplay due to the combination of stealth - themed elements."
                },
                {
                    "question": "How do you play Sprunkis Agent Mod?",
                    "answer": "First, select characters from the agent - themed lineup. Then, use the drag - and - drop method to arrange them on the screen to layer spy - inspired sounds. Next, experiment and adjust by mixing loops, tweaking volumes, and exploring combinations. Finally, save your track and share it with the Sprunki community."
                },
                {
                    "question": "Who is Sprunkis Agent Mod suitable for?",
                    "answer": "Sprunkis Agent Mod is suitable for players who love thrilling and adventurous themes, as it offers a fresh and exciting way to create music in an espionage - themed setting."
                }
            ],
            'conclusion': 'Sprunki Agent Gives the Sprunki world an epic spy - themed makeover! Characters turn into super cool secret agents. They got sleek looks, mysterious personalities, and the sound is so exciting, it will get your heart pounding!'
        },
        'banana-porridge': {
            'faqs': [
                {
                    "question": "What is the Sprunki Banana Porridge Mod?",
                    "answer": "The Sprunki Banana Porridge Mod is a fun and flavorful addition to the Sprunki universe. It combines smooth beats with banana - infused visuals, offering a light - hearted and wacky musical experience."
                },
                {
                    "question": "What are the features of the Sprunki Banana Porridge Mod?",
                    "answer": "Features include banana - themed Sprunki characters with yellow - tinted designs and breakfast - inspired animations, smooth & creamy soundscapes blending warm melodies with funky percussion, playful and vibrant visuals filled with bananas, and wacky sound effects like banana peel slips and slurping porridge sounds."
                },
                {
                    "question": "How do you play the Sprunki Banana Porridge Mod?",
                    "answer": "First, select banana - infused characters from the porridge - loving Sprunki lineup. Then, create tasty tunes by dragging and dropping characters onto the stage to mix sweet melodies with banana rhythms. Next, experiment with different banana - themed character interactions to unlock hidden musical surprises. Finally, save and share your tracks with the Sprunki community."
                },
                {
                    "question": "Why should one play the Sprunki Banana Porridge Mod?",
                    "answer": "One should play it for a light - hearted, fun experience, as it's silly and creative. It's also great for fans of quirky music mods who love playful themes and goofy visuals. Additionally, it offers a deliciously unique sound with its smooth, bouncy beats that bring a fresh twist to Sprunki gameplay."
}
            ],
            'conclusion': 'Sprunki Banana Porridge Mod: Groovy food beats! Wacky banana visuals & smooth rhythms. Taste the fun!'
        },
        'sprunkr': {
            'faqs': [
                {
                    'question': 'What is Bear Clicker?',
                    'answer': 'Bear Clicker is the main platform for all Bear Clicker mods and games, offering a unique horror-themed music creation experience.'
                },
                {
                    'question': 'What can I do on Bear Clicker?',
                    'answer': 'On Bear Clicker, you can play various Bear Clicker mods, create music, share your creations, and join a community of music enthusiasts.'
                },
                {
                    "question": "What is Bear Clicker But Sprunki Mod?",
                    "answer": "Bear Clicker But Sprunki Mod is a creative twist on the original Bear Clicker mod. It replaces existing characters with Sprunki figures, retains Bear Clicker's gameplay charm, and introduces Sprunki-inspired designs, bridging two popular worlds with vibrant visuals and dynamic soundscapes."
                },
                {
                    "question": "What are the features of Bear Clicki But Sprunkr Game?",
                    "answer": "The features include Sprunki Characters that replace the original Bear Clicker ones, each with unique sound loops and animations; Dynamic Soundscapes with rhythmic beats and melodies of a distinct Sprunki flair; Bright Visuals enhanced by Sprunki-themed designs and animations; and Engaging Gameplay that combines Bear Clicker's mechanics with Sprunki characters' creativity."
                },
                {
                    "question": "How do you play Bear Clicker But Sprunki Mod?",
                    "answer": "To play, first select characters from the Sprunki-themed roster, each offering unique sounds and animations. Then drag and drop them on the stage to layer beats, melodies, and effects into cohesive compositions. After that, experiment and refine by mixing loops creatively and exploring new combinations. Finally, save and share your tracks with the Bear Clicker community."
                },
                {
                    "question": "Why is Bear Clicker But Sprunki Mod appealing?",
                    "answer": "It's appealing because it's a delightful crossover that adds a refreshing twist to the original gameplay, allowing players to experience the best of both worlds."
                }
            ],
            'conclusion': 'Join Bear Clicker today and become part of our growing community of music creators!'
        },
        'index': {
            'faqs': [
                {
    "question": "What makes Bear Clicker special?",
    "answer": "Bear Clicker is special as it combines casual gameplay with strategic depth. It has a diverse bear collection of over 500 unique bears, strategic progression balancing active tapping and idle honey production, social features like global leaderboards, regular monthly updates, and cross - platform play across mobile and web browsers."
},
{
    "question": "How do you get started with Bear Clicker?",
    "answer": "To get started, first master the basics: tap to generate honey, unlock auto - production, evolve your bears using the merge system, and complete daily quests. Then, for advanced strategies, optimize your collection by focusing on high honey - producing bears, participate in events for limited - edition bears, join a guild for bonus rewards, and customize your sanctuary."
},
{
    "question": "What are the latest features in Bear Clicker for 2025?",
    "answer": "The latest features include enhanced graphics for all animations, cloud saves for seamless progress syncing across accounts, weekly challenges for exclusive rewards, and community - driven events in the game universe."
},
{
    "question": "Is Bear Clicker free to play?",
    "answer": "Yes, Bear Clicker is completely free to download and play. Optional in - app purchases are available but not required to enjoy the full experience."
},
{
    "question": "How often does Bear Clicker update?",
    "answer": "Bear Clicker receives monthly updates with new content such as fresh bear varieties, seasonal events, gameplay improvements, and community - requested features."
},
{
    "question": "Can you play Bear Clicker offline?",
    "answer": "Yes, while some features need an internet connection, the core gameplay mechanics work offline, allowing you to accumulate honey and progress."
},
{
    "question": "What is Bear Clicker?",
    "answer": "Bear Clicker is a charming idle clicker game. It combines addictive tapping with strategic resource management. Players collect bears by tapping to generate honey, invest in upgrades, use merge mechanics to create rare hybrids, and participate in seasonal events and daily challenges. It has community features, vibrant visuals, and an offline progression system."
},
{
    "question": "How do you play Bear Clicker?",
    "answer": "Start by tapping the central bear to generate honey, unlock power - ups like the “Golden Paw”. Use honey to upgrade bears, such as buying auto - tappers, honey multipliers, and evolution chambers. Merge identical bears to create evolved species. Complete daily quests and seasonal events. Optimize your strategy by prioritizing auto - tappers, saving gems for permanent boosts, and joining guilds."
},
{
    "question": "What are the features of Bear Clicker?",
    "answer": "There are 500+ bears to collect, a balance of idle and active play, customization options for habitats and bear accessories, social competition through leaderboards and guilds, merge mechanics to create over 50 hybrids, offline progression, and regular monthly updates with new events, bears, and challenges."
},
{
    "question": "How do you merge bears in Bear Clicker?",
    "answer": "Drag two identical bears into the Evolution Chamber. Merging common bears unlocks rare species, and merging rares creates legendaries."
},
{
    "question": "What's the best way to earn gems in Bear Clicker?",
    "answer": "The best ways are to complete daily quests, watch ads, or rank high on leaderboards. Gems can be used to buy permanent upgrades and exclusive bears."
},
{
    "question": "Are there ads in Bear Clicker?",
    "answer": "There are optional rewarded ads that can double rewards or unlock bonus honey. Ads can be disabled via a one - time purchase."
},
{
    "question": "Can you sync progress across devices in Bear Clicker?",
    "answer": "Yes, you can link your account to Google Play, Apple ID, or Facebook to save and sync progress across devices."
},
{
    "question": "How often are new bears added in Bear Clicker?",
    "answer": "New bears are added monthly, with seasonal variants during holidays like Halloween and Christmas."
} 
    ],
    'conclusion': "BearClicker, A New Bear Clicker Game Online, Create unique bear compositions, experience fun sound effects, and immerse yourself on bearclicker net"
},
        'spruted': {
            'faqs': [
                {
                    'question': 'What is Sprunki Spruted?',
                    'answer': 'Sprunki Spruted is a nature-themed mod that brings plant and growth elements into the Sprunki universe.'
                },
                {
                    'question': 'What makes Spruted unique?',
                    'answer': 'Spruted features organic sound effects and growth-themed visuals, creating a natural and evolving musical experience.'
                },
                {
                    "question": "What makes Sprunki Spruted Mod unique?",
                    "answer": "Sprunki Spruted Mod transforms characters into slim, baby-like versions of themselves, introducing a playful twist to the Sprunki universe. It gives them a fresh, adorable appearance while retaining the original charm, along with updated visuals, lighthearted soundscapes, and a fun theme."
                },
                {
                    "question": "What are the key features of Sprunki Spruted Mod?",
                    "answer": "The key features include baby-like characters that are redesigned to be slim and youthful, adding a cute aesthetic; playful soundscapes with light, cheerful beats and melodies; vibrant visuals with bright and colorful animations complementing the character designs; and lighthearted gameplay that encourages creativity and is accessible to all ages."
                },
                {
                    "question": "How do you play Sprunki Spruted Mod?",
                    "answer": "To play, first select characters from the slim, baby-like lineup, each offering unique loops and effects. Then drag and drop them on the screen to layer playful beats, melodies, and rhythms into your track. After that, experiment and adjust by combining loops creatively, tweaking volumes, and exploring sound combinations. Finally, save and share your track with the Sprunki community."
                },
                {
                    "question": "Why is Sprunki Spruted Mod suitable for fans of all ages?",
                    "answer": "It's suitable because of its lighthearted gameplay that encourages creativity and fun, along with its cute and engaging design elements like the baby-like characters, playful soundscapes, and vibrant visuals."
                }   
            ],
            'conclusion': 'Let your music grow and evolve with Sprunki Spruted!'
        }
    }
    return faqs_data.get(page_name, {'faqs': [], 'conclusion': ''})

@app.route('/')
def home():
    translations_data = get_translations()
    faq_data = get_faqs_for_page('index')  # 使用sprunkr的FAQ数据作为主页FAQ
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
        return render_template('faq.html',
                         title='FAQ - Bear Clicker',
                         translations=trans)
    except Exception as e:
        app.logger.error(f"Error in faq route: {e}")
        return render_template('faq.html',
                         title='FAQ - Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         })

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/sprunki-lily')
def sprunki_lily():
    faq_data = get_faqs_for_page('lily')
    return render_template('sprunki-lily.html',
                         page_title='Sprunki Lily',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-fiddlebops')
def sprunki_fiddlebops():
    faq_data = get_faqs_for_page('fiddlebops')
    return render_template('sprunki-fiddlebops.html',
                         page_title='Sprunki Fiddlebops',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-megalovania')
def sprunki_megalovania():
    faq_data = get_faqs_for_page('megalovania')
    return render_template('sprunki-megalovania.html',
                         page_title='Sprunki Megalovania',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-sprunkr')
def sprunki_sprunkr():
    faq_data = get_faqs_for_page('sprunkr')
    return render_template('sprunki-sprunkr.html',
                         page_title='Bear Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-spruted')
def sprunki_spruted():
    faq_data = get_faqs_for_page('spruted')
    return render_template('sprunki-spruted.html',
                         page_title='Sprunki Spruted',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-banana')
def sprunki_banana():
    faq_data = get_faqs_for_page('banana')
    return render_template('sprunki-banana.html',
                         page_title='Sprunki Banana',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-garnold')
def sprunki_garnold():
    faq_data = get_faqs_for_page('garnold')
    return render_template('sprunki-garnold.html',
                         page_title='Sprunki Garnold',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-ketchup')
def sprunki_ketchup():
    faq_data = get_faqs_for_page('ketchup')
    return render_template('sprunki-ketchup.html',
                         page_title='Sprunki Ketchup',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-sprunksters')
def sprunki_sprunksters():
    faq_data = get_faqs_for_page('sprunksters')
    return render_template('sprunki-sprunksters.html',
                         page_title='Sprunki Sprunksters',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/sprunki-agents')
def sprunki_agents():
    faq_data = get_faqs_for_page('agents')
    return render_template('sprunki-agents.html',
                         page_title='Sprunki Agents',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/sprunki-banana-porridge')
def sprunki_banana_porridge():
    faq_data = get_faqs_for_page('banana-porridge')
    return render_template('sprunki-banana-porridge.html',
                         page_title='Sprunki Banana Porridge',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/sprunki-retake-but-human')
def sprunki_retake_but_human():
    faq_data = get_faqs_for_page('retake-but-human')
    return render_template('sprunki-retake-but-human.html',
                         page_title='Sprunki Retake But Human',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-parodybox')
def sprunki_parodybox():
    faq_data = get_faqs_for_page('parodybox')
    return render_template('sprunki-parodybox.html',
                         page_title='Sprunki ParodyBox',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-pyramixed')
def sprunki_pyramixed():
    faq_data = get_faqs_for_page('pyramixed')
    return render_template('sprunki-pyramixed.html',
                         page_title='Sprunki PyraMixed',
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
    app.run(debug=True, port=5001)
