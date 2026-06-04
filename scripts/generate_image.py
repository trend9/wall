import os
import json
import random
import time
import urllib.parse
import requests

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'wallpapers.json')
WALLPAPERS_DIR = os.path.join(BASE_DIR, 'wallpapers')

# Ensure wallpapers directory exists
os.makedirs(WALLPAPERS_DIR, exist_ok=True)

# Categories definition
CATEGORIES = [
    {
        "id": "cyberpunk",
        "name_en": "Cyberpunk",
        "name_ja": "サイバーパンク",
        "subjects": [
            {"en": "a futuristic rainy alleyway illuminated by pink and cyan neon signs", "ja": "ピンクとシアンのネオン看板に照らされた未来の雨の路地裏"},
            {"en": "a high-tech cyberpunk hacker den with multiple glowing holographic screens", "ja": "複数の光るホログラフィック画面があるハイテクなサイバーパンクのハッカーの隠れ家"},
            {"en": "a massive futuristic metropolis with flying cars zooming between skyscrapers at dusk", "ja": "夕暮れ時に超高層ビルの間を飛び交う空飛ぶ車と巨大な未来都市"},
            {"en": "a cyberpunk street market with glowing street food stalls and robotic sellers", "ja": "光るストリートフードの屋台とロボットの売り手がいるサイバーパンクの夜市"},
            {"en": "a futuristic train speeding through a neon-lit cyberpunk city canyon", "ja": "ネオンに照らされたサイバーパンクの都市の谷間を疾走する未来的な列車"}
        ],
        "styles": [
            "futuristic, synthwave aesthetic, neon glow, wet reflections, highly detailed, octane render, 8k resolution, cinematic lighting",
            "cyberpunk 2077 style, blade runner aesthetic, realistic textures, volumetric fog, dramatic contrast, unreal engine 5 render"
        ]
    },
    {
        "id": "nature",
        "name_en": "Nature",
        "name_ja": "自然",
        "subjects": [
            {"en": "a serene misty pine forest at sunrise with soft golden light rays filtering through the trees", "ja": "木々の間から柔らかな金色の光が差し込む、日の出の静かな霧深い松林"},
            {"en": "a magnificent glowing bioluminescent waterfall deep inside a magical night jungle", "ja": "魔法の夜のジャングルの奥深くにある、見事な発光するバイオルミネッセンスの滝"},
            {"en": "majestic snow-capped mountain peaks reflecting perfectly in a crystal-clear alpine lake", "ja": "澄み切った高山湖に完璧に映り込む、雄大な雪を頂いた山の頂"},
            {"en": "a peaceful cherry blossom path in full bloom with petals gently floating in the spring breeze", "ja": "春のそよ風に花びらが優しく舞う、満開の静かな桜並木"},
            {"en": "an epic sunset over a calm ocean with vibrant pink, purple, and orange clouds", "ja": "鮮やかなピンク、紫、オレンジ色の雲が広がる、穏やかな海に沈む壮大な夕日"}
        ],
        "styles": [
            "breathtaking nature photography, soft lighting, award-winning, highly detailed, realistic, National Geographic style, 8k",
            "magical realism, ethereal atmosphere, vivid colors, cinematic depth of field, masterpiece"
        ]
    },
    {
        "id": "anime",
        "name_en": "Anime",
        "name_ja": "アニメ",
        "subjects": [
            {"en": "a cozy anime-style study room with a window overlooking a summer sky and fluffy white clouds", "ja": "夏の空とふわふわした白い雲を見渡す窓がある、居心地の良いアニメ風の書斎"},
            {"en": "a beautiful anime shrine entrance under a massive ancient sakura tree in full bloom at twilight", "ja": "黄昏時に満開の巨大な古い桜の木の下にある、美しいアニメ風の神社入り口"},
            {"en": "an industrial retro-futuristic steampunk airship floating over a sea of clouds at sunset", "ja": "夕暮れ時の雲海に浮かぶ、インダストリアルでレトロフューチャーなスチームパンクの飛行船"},
            {"en": "a magical starry night sky over a peaceful countryside hill with a single glowing tree", "ja": "一本の光る木が立つ静かな田舎の丘の上の、魔法のような星空の夜空"},
            {"en": "a futuristic anime city with clean modern streets, green foliage, and high-tech monorail", "ja": "クリーンでモダンな通り、緑の木々、ハイテクなモノレールがある未来のアニメ都市"}
        ],
        "styles": [
            "studio ghibli aesthetic, hand-drawn anime style, highly detailed illustration, warm colors, nostalgic, beautiful lighting, desktop wallpaper",
            "makoto shinkai style, gorgeous sky details, lens flare, vivid color grading, ethereal, wind blowing, high quality digital art"
        ]
    },
    {
        "id": "minimalist",
        "name_en": "Minimalist",
        "name_ja": "ミニマリスト",
        "subjects": [
            {"en": "a single green leaf with a single water droplet on a clean, soft beige background", "ja": "クリーンで柔らかなベージュの背景に、一滴の水滴がついた一枚の緑の葉"},
            {"en": "a minimal abstract geometric composition of sun and dunes using warm pastel tones", "ja": "暖かみのあるパステルカラーを使用した、太陽と砂丘のミニマルで抽象的な幾何学的構図"},
            {"en": "a clean concrete wall with elegant shadows of palm leaves cast by the afternoon sun", "ja": "午後の太陽によって投げかけられたヤシの葉のエレガントな影があるクリーンなコンクリート壁"},
            {"en": "a solitary wooden pier leading into a vast, calm, misty white lake", "ja": "広大で穏やかな霧深い白い湖へと続く、一連の木製の桟橋"},
            {"en": "a simple pastel colored mountain range silhouette under a pale sun, clean lines", "ja": "淡い太陽の下に広がる、シンプルなパステルカラーの山脈のシルエット、クリーンなライン"}
        ],
        "styles": [
            "clean minimalist design, flat colors, subtle textures, elegant composition, modern aesthetic, zen, 8k resolution",
            "nordic style minimalism, muted pastel color palette, soft shadows, serene, simplistic beauty"
        ]
    },
    {
        "id": "space",
        "name_en": "Space",
        "name_ja": "宇宙",
        "subjects": [
            {"en": "a stunning cosmic nebula with vibrant violet, blue and gold dust clouds forming stars", "ja": "星を形成する鮮やかなバイオレット、ブルー、ゴールドの宇宙塵の雲を持つ、見事な宇宙星雲"},
            {"en": "a distant ringed exoplanet rising over the horizon of a barren alien moon landscape", "ja": "不毛なエイリアンの月の景色の地平線上に昇る、遠くの輪を持つ系外惑星"},
            {"en": "an astronaut floating peacefully in deep space surrounded by distant galaxies and colorful dust", "ja": "遠くの銀河やカラフルな塵に囲まれ、深宇宙を静かに漂う宇宙飛行士"},
            {"en": "a massive spiral galaxy glowing brightly with millions of stars in deep black space", "ja": "深い漆黒の宇宙で何百万もの星々が明るく輝く、巨大な渦巻銀河"},
            {"en": "a futuristic space station orbiting a beautiful green and blue earth-like planet", "ja": "美しい緑と青の地球のような惑星の軌道を回る、未来的な宇宙ステーション"}
        ],
        "styles": [
            "epic space exploration art, Hubble telescope style, highly detailed cosmic rendering, cinematic lighting, photorealistic, 8k",
            "sci-fi concept art, interstellar space, cosmic dust, deep contrast, unreal engine 5 render, hyper-detailed"
        ]
    },
    {
        "id": "abstract",
        "name_en": "Abstract",
        "name_ja": "抽象画",
        "subjects": [
            {"en": "a fluid dynamic flow of liquid gold and deep blue ink blending together with glitter details", "ja": "ラメのディテールとブレンドし合う、液体ゴールドとディープブルーのインクの流体的な流れ"},
            {"en": "a mesmerizing 3D render of looping glass ribbons reflecting a colorful gradient background", "ja": "カラフルなグラデーションの背景を反射する、ループするガラスのリボンの魅惑的な3Dレンダリング"},
            {"en": "a chaotic but beautiful explosion of colorful smoke waves and geometric crystal shards", "ja": "カラフルな煙の波と幾何学的な結晶の破片のカオスでありながら美しい爆発"},
            {"en": "a retro-wave digital grid with organic neon silk-like waves floating above it", "ja": "有機的なネオンシルクのような波が浮かぶ、レトロウェーブ調のデジタルグリッド"},
            {"en": "a dynamic collage of torn textures, colorful brush strokes, and metallic gold paint splatters", "ja": "破れたテクスチャ、カラフルなブラシストローク、金属的なゴールドペイントの飛沫のダイナミックなコラージュ"}
        ],
        "styles": [
            "modern abstract art, vibrant color palette, high fidelity textures, 3D digital render, creative wallpaper, octane render, 8k",
            "fine art aesthetics, textured canvas, organic shapes, fluid movement, premium graphic design, visual masterpiece"
        ]
    }
]

def load_wallpapers():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return json.loads(content) if content else []
        except Exception as e:
            print(f"Error loading wallpapers: {e}")
            return []
    return []

def save_wallpapers(wallpapers):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(wallpapers, f, indent=2, ensure_ascii=False)

def main():
    existing_wallpapers = load_wallpapers()
    count = len(existing_wallpapers)
    
    # Select category sequentially based on count to ensure equal distribution
    cat_index = count % len(CATEGORIES)
    category = CATEGORIES[cat_index]
    
    # Pick a random subject and style from this category
    subject = random.choice(category["subjects"])
    style = random.choice(category["styles"])
    
    # Generate Prompt
    prompt_en = f"{subject['en']}, {style}"
    
    # Set up metadata names & description
    timestamp = int(time.time())
    wallpaper_id = f"wp_{timestamp}"
    filename = f"wallpaper_{timestamp}.jpg"
    filepath = os.path.join(WALLPAPERS_DIR, filename)
    
    # Simple templates for generating Titles and Descriptions
    # English title/desc
    title_en = f"Mystical {category['name_en']} Landscape"
    desc_en = f"A high-quality, breathtaking {category['name_en'].lower()} wallpaper depicting {subject['en']}. Generated with state-of-the-art AI."
    
    # Japanese title/desc
    title_ja = f"神秘的な{category['name_ja']}の風景"
    desc_ja = f"{subject['ja']}を描いた、高品質で息をのむような{category['name_ja']}の壁紙画像。最先端のAIによって生成されました。"
    
    # Use randomized variations for title to make it look unique
    adjectives_en = ["Stunning", "Ethereal", "Epic", "Cinematic", "Serene", "Majestic", "Dreamy", "Vibrant"]
    adjectives_ja = ["見事な", "幻想的な", "壮大な", "映画のような", "静寂な", "雄大な", "夢のような", "鮮やかな"]
    
    adj_idx = random.randint(0, len(adjectives_en) - 1)
    adj_en = adjectives_en[adj_idx]
    adj_ja = adjectives_ja[adj_idx]
    
    title_en = f"{adj_en} {category['name_en']}"
    title_ja = f"{adj_ja}{category['name_ja']}"
    
    print(f"Selected Category: {category['name_en']}")
    print(f"Prompt (EN): {prompt_en}")
    
    # Call Pollinations AI
    encoded_prompt = urllib.parse.quote(prompt_en)
    seed = random.randint(0, 999999)
    # 1920x1080 resolution
    # Retry logic for rate limits/concurrency queue issues (e.g., 402/502/503 errors)
    max_retries = 6
    backoff = 3
    success = False
    
    # Try different URL variations (full URL first, then fallback to parameterless URL)
    urls_to_try = [
        # Full featured URL
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true&seed={seed}",
        # Fallback 1: Simple URL without dimensions/nologo to hit the fast/default queue
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}",
        # Fallback 2: No query parameters at all (random seed inside prompt text)
        f"https://image.pollinations.ai/prompt/{encoded_prompt}%20seed%20{seed}"
    ]
    
    print("Beginning generation attempts with fallback strategies...")
    for url_attempt in urls_to_try:
        backoff = 3  # Reset backoff delay for each URL strategy
        print(f"Targeting URL: {url_attempt}")
        for attempt in range(1, 4):
            try:
                response = requests.get(url_attempt, timeout=60)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Successfully saved wallpaper to {filename}!")
                    success = True
                    break
                elif response.status_code == 402:
                    print(f"Attempt {attempt}: Received 402 (Queue full). Retrying in {backoff} seconds...")
                    time.sleep(backoff)
                    backoff *= 1.5
                else:
                    print(f"Attempt {attempt}: Received status code {response.status_code}. Retrying in {backoff} seconds...")
                    time.sleep(backoff)
                    backoff *= 1.5
            except Exception as e:
                print(f"Attempt {attempt}: Request failed with error: {type(e).__name__}. Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 1.5
        
        if success:
            break
        else:
            print("Current URL strategy failed. Switching to fallback strategy...")

    # ULTRA FALLBACK: If all AI generations failed (common on GitHub Actions runner shared IPs)
    # Download a gorgeous high-resolution landscape/digital art image from a free stock service.
    if not success:
        print("AI generation failed or rate-limited. Activating Ultra Fallback to high-quality stock wallpaper...")
        # Curated keywords for gorgeous search matching the category
        fallback_keywords = {
            "cyberpunk": "cyberpunk,neon,city,night,futuristic",
            "nature": "landscape,mountain,forest,waterfall,nature",
            "anime": "illustration,japanese,art,scenery",
            "minimalist": "minimalist,geometric,pastel,simple",
            "space": "galaxy,nebula,space,stars,astronaut",
            "abstract": "abstract,fluid,acrylic,smoke,art"
        }
        kw = fallback_keywords.get(category["id"], "wallpaper,landscape")
        # Use Picsum or Unsplash source redirect to fetch a stunning 1920x1080 image
        fallback_url = f"https://picsum.photos/1920/1080?sig={timestamp}&q={kw}"
        print(f"Downloading fallback wallpaper from: {fallback_url}")
        
        for attempt in range(1, 4):
            try:
                response = requests.get(fallback_url, timeout=45)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Successfully saved fallback wallpaper to {filename}!")
                    success = True
                    # Update prompt metadata to indicate stock fallback
                    prompt_en = f"[Fallback High-Quality Stock Wallpaper] Keywords: {kw.replace(',', ', ')}"
                    break
                else:
                    print(f"Fallback attempt {attempt} failed with status {response.status_code}. Retrying...")
                    time.sleep(2)
            except Exception as e:
                print(f"Fallback attempt {attempt} threw exception: {type(e).__name__}. Retrying...")
                time.sleep(2)

    if success:
        # Create a database record
        new_wallpaper = {
            "id": wallpaper_id,
            "category": category["id"],
            "category_name_en": category["name_en"],
            "category_name_ja": category["name_ja"],
            "title_en": title_en,
            "title_ja": title_ja,
            "description_en": desc_en,
            "description_ja": desc_ja,
            "prompt": prompt_en,
            "filename": filename,
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "timestamp": timestamp,
            "downloads": 0,
            "likes": 0
        }
        
        existing_wallpapers.insert(0, new_wallpaper) # Add to the top
        save_wallpapers(existing_wallpapers)
        print("Successfully updated database!")
    else:
        print("Failed to generate image after trying all fallback and stock strategies.")

if __name__ == "__main__":
    main()
