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

# SEO configurations
# Set NOINDEX = True to prevent search engines from indexing the wallpaper detail pages.
# Set NOINDEX = False (default) to allow indexing and increase organic search traffic.
NOINDEX = False

def generate_individual_pages(wallpapers):
    w_dir = os.path.join(BASE_DIR, 'w')
    os.makedirs(w_dir, exist_ok=True)
    
    robots_meta = '<meta name="robots" content="noindex, follow">' if NOINDEX else '<meta name="robots" content="index, follow">'
    
    for wp in wallpapers:
        wp_id = wp.get("id")
        filename = wp.get("filename")
        title_en = wp.get("title_en", "Premium Wallpaper").replace('"', '&quot;')
        title_ja = wp.get("title_ja", "プレミアム壁紙").replace('"', '&quot;')
        desc_en = wp.get("description_en", "").replace('"', '&quot;')
        desc_ja = wp.get("description_ja", "").replace('"', '&quot;')
        category_en = wp.get("category_name_en", "General").replace('"', '&quot;')
        category_ja = wp.get("category_name_ja", "一般").replace('"', '&quot;')
        prompt = wp.get("prompt", "").replace('"', '&quot;').replace('\n', ' ')
        date_str = wp.get("date", "")
        
        # We escape single quotes for Javascript insertion
        js_title_en = title_en.replace("'", "\\'")
        js_title_ja = title_ja.replace("'", "\\'")
        js_desc_en = desc_en.replace("'", "\\'")
        js_desc_ja = desc_ja.replace("'", "\\'")
        js_category_en = category_en.replace("'", "\\'")
        js_category_ja = category_ja.replace("'", "\\'")
        
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_ja} - Aetheria AI Wallpapers</title>
  <meta name="description" content="{desc_ja}">
  {robots_meta}
  
  <!-- Open Graph -->
  <meta property="og:title" content="{title_ja} - Aetheria AI Wallpapers">
  <meta property="og:description" content="{desc_ja}">
  <meta property="og:image" content="https://wall-eosin.vercel.app/wallpapers/{filename}">
  <meta property="og:url" content="https://wall-eosin.vercel.app/w/{wp_id}.html">
  <meta property="og:type" content="article">
  
  <!-- CSS Link -->
  <link rel="stylesheet" href="../index.css">
  
  <!-- Feather Icons -->
  <script src="https://unpkg.com/feather-icons"></script>
</head>
<body>

  <!-- Ambient Glow Effects -->
  <div class="ambient-glow-1"></div>
  <div class="ambient-glow-2"></div>

  <!-- Header Navigation -->
  <header>
    <div class="nav-container">
      <a href="../" class="logo" id="logo-link">
        <span class="logo-icon"></span>
        Aetheria
      </a>
      <div class="nav-actions">
        <!-- Language Switcher -->
        <div class="lang-toggle" id="langToggle">
          <button class="lang-btn active" data-lang="ja">日本語</button>
          <button class="lang-btn" data-lang="en">EN</button>
        </div>
      </div>
    </div>
  </header>

  <!-- Detail Content Section -->
  <main class="gallery-section" style="margin-top: 2rem;">
    <div class="modal-content" style="display: grid; max-height: none; transform: none; margin: 0 auto; background: rgba(20, 20, 30, 0.5);">
      <div class="modal-img-section" style="background: rgba(0,0,0,0.3); padding: 1rem;">
        <img class="modal-preview-img" src="../wallpapers/{filename}" alt="{title_ja}" style="border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
      </div>
      <div class="modal-details">
        <span class="badge" id="detailCategory">{category_ja}</span>
        <h1 class="hero-title" id="detailTitle" style="font-size: 2.2rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #fff, var(--text-secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title_ja}</h1>
        <p class="hero-desc" id="detailDesc" style="font-size: 1rem; margin-bottom: 1.5rem;">{desc_ja}</p>
        
        <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem; display: flex; flex-direction: column; gap: 0.25rem;">
          <div id="detailDate">公開日: {date_str}</div>
          <div id="detailResolution">解像度: 1920 x 1080 (16:9)</div>
        </div>

        <h4 id="promptTitle" style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-primary);">生成プロンプト</h4>
        <div class="modal-prompt-box" style="background: rgba(0, 0, 0, 0.4);">
          <button class="copy-prompt-btn" id="copyPromptBtn">コピー</button>
          <span class="modal-prompt-text" id="detailPromptText">{prompt}</span>
        </div>

        <div style="display: flex; gap: 1rem; margin-top: auto; padding-top: 1rem;">
          <a href="../wallpapers/{filename}" class="btn btn-primary" download style="flex: 1;">
            <i data-feather="download"></i>
            <span id="downloadText">ダウンロード</span>
          </a>
          <button class="btn btn-secondary btn-icon like-btn" id="detailLikeBtn">
            <i data-feather="heart"></i>
          </button>
        </div>
        
        <div style="margin-top: 1.5rem; display: flex; justify-content: center;">
          <a href="../" class="btn btn-secondary" style="width: 100%;">
            <i data-feather="arrow-left"></i>
            <span id="backText">ホームに戻る</span>
          </a>
        </div>
      </div>
    </div>
  </main>

  <!-- Banner ad placement at the bottom -->
  <div class="ad-banner-wrapper">
    <script async="async" data-cfasync="false" src="https://pl29642773.effectivecpmnetwork.com/e02b2bad74f57baf7d09e50da61b9158/invoke.js"></script>
    <div id="container-e02b2bad74f57baf7d09e50da61b9158"></div>
  </div>

  <!-- Toast Notification -->
  <div class="toast" id="toast">プロンプトをクリップボードにコピーしました！</div>

  <!-- Footer -->
  <footer>
    <p>&copy; 2026 Aetheria. All rights reserved.</p>
  </footer>

  <script>
    const wpId = "{wp_id}";
    const translations = {{
      ja: {{
        title: "{js_title_ja} - Aetheria AI Wallpapers",
        description: "{js_desc_ja}",
        detailTitle: "{js_title_ja}",
        detailDesc: "{js_desc_ja}",
        detailCategory: "{js_category_ja}",
        dateLabel: "公開日: {date_str}",
        resolution: "解像度: 1920 x 1080 (16:9)",
        promptTitle: "生成プロンプト",
        copyLabel: "コピー",
        copiedToast: "プロンプトをクリップボードにコピーしました！",
        download: "ダウンロード",
        backHome: "ホームに戻る"
      }},
      en: {{
        title: "{js_title_en} - Aetheria AI Wallpapers",
        description: "{js_desc_en}",
        detailTitle: "{js_title_en}",
        detailDesc: "{js_desc_en}",
        detailCategory: "{js_category_en}",
        dateLabel: "Published: {date_str}",
        resolution: "Resolution: 1920 x 1080 (16:9)",
        promptTitle: "Generation Prompt",
        copyLabel: "COPY",
        copiedToast: "Prompt copied to clipboard!",
        download: "Download",
        backHome: "Back to Home"
      }}
    }};

    let currentLang = localStorage.getItem('lang') || 'ja';

    function updateLanguageUI() {{
      const t = translations[currentLang];
      document.title = t.title;
      document.querySelector('meta[name="description"]').setAttribute("content", t.description);
      document.getElementById('detailTitle').textContent = t.detailTitle;
      document.getElementById('detailDesc').textContent = t.detailDesc;
      document.getElementById('detailCategory').textContent = t.detailCategory;
      document.getElementById('detailDate').textContent = t.dateLabel;
      document.getElementById('detailResolution').textContent = t.resolution;
      document.getElementById('promptTitle').textContent = t.promptTitle;
      document.getElementById('copyPromptBtn').textContent = t.copyLabel;
      document.getElementById('toast').textContent = t.copiedToast;
      document.getElementById('downloadText').textContent = t.download;
      document.getElementById('backText').textContent = t.backHome;
      
      document.documentElement.lang = currentLang;

      document.querySelectorAll('.lang-btn').forEach(btn => {{
        if (btn.dataset.lang === currentLang) {{
          btn.classList.add('active');
        }} else {{
          btn.classList.remove('active');
        }}
      }});
    }}

    // Setup language buttons
    document.getElementById('langToggle').addEventListener('click', (e) => {{
      const btn = e.target.closest('.lang-btn');
      if (!btn) return;
      currentLang = btn.dataset.lang;
      localStorage.setItem('lang', currentLang);
      updateLanguageUI();
    }});

    // Setup copy button
    document.getElementById('copyPromptBtn').addEventListener('click', () => {{
      const text = document.getElementById('detailPromptText').textContent;
      navigator.clipboard.writeText(text).then(() => {{
        const toast = document.getElementById('toast');
        toast.classList.add('show');
        setTimeout(() => {{
          toast.classList.remove('show');
        }}, 2500);
      }});
    }});

    // Setup Like functionality
    const likeBtn = document.getElementById('detailLikeBtn');
    let likedList = JSON.parse(localStorage.getItem('liked_wallpapers') || '[]');
    
    if (likedList.includes(wpId)) {{
      likeBtn.classList.add('liked');
    }}

    likeBtn.addEventListener('click', () => {{
      const idx = likedList.indexOf(wpId);
      if (idx > -1) {{
        likedList.splice(idx, 1);
        likeBtn.classList.remove('liked');
      }} else {{
        likedList.push(wpId);
        likeBtn.classList.add('liked');
      }}
      localStorage.setItem('liked_wallpapers', JSON.stringify(likedList));
    }});

    // Init UI
    updateLanguageUI();
    feather.replace();
  </script>
</body>
</html>
"""
        
        filepath = os.path.join(w_dir, f"{wp_id}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
    print(f"Successfully generated {len(wallpapers)} individual wallpaper HTML pages.")

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
            {"en": "a single green leaf with a single water droplet on a clean, soft beige background", "ja": "クリーンで柔らかなベージュ of 背景に、一滴の水滴がついた一枚の緑の葉"},
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

def generate_rss_feed(wallpapers):
    rss_path = os.path.join(BASE_DIR, 'feed.xml')
    items_xml = []
    
    # Take latest 30 wallpapers for the feed
    for wp in wallpapers[:30]:
        title = wp.get("title_en", "Premium Wallpaper")
        desc = wp.get("description_en", "")
        filename = wp.get("filename")
        wp_id = wp.get("id")
        date_str = wp.get("date")
        
        # Parse date to RFC 822 format for RSS feeds
        try:
            struct_time = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            pub_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", struct_time)
        except Exception:
            pub_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
            
        item_xml = f"""    <item>
      <title><![CDATA[{title}]]></title>
      <link>https://wall-eosin.vercel.app</link>
      <description><![CDATA[{desc}]]></description>
      <enclosure url="https://wall-eosin.vercel.app/wallpapers/{filename}" type="image/jpeg" />
      <guid isPermaLink="false">{wp_id}</guid>
      <pubDate>{pub_date}</pubDate>
    </item>"""
        items_xml.append(item_xml)
        
    joined_items = "\n".join(items_xml)
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>Aetheria AI Wallpapers</title>
    <link>https://wall-eosin.vercel.app</link>
    <description>Daily updated premium AI-generated wallpapers.</description>
    <language>en-us</language>
    <lastBuildDate>{time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())}</lastBuildDate>
{joined_items}
  </channel>
</rss>"""
    
    with open(rss_path, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    print("Successfully generated RSS feed (feed.xml) for Pinterest integration!")

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
    success = False
    
    # 1. Try Hugging Face Inference API if HF_TOKEN is configured (Highly recommended, fast, & guaranteed)
    hf_token = os.environ.get('HF_TOKEN')
    if hf_token:
        print("HF_TOKEN found! Initiating Hugging Face Inference API...")
        # Use high-quality Stable Diffusion XL or FLUX model
        hf_model = "stabilityai/stable-diffusion-xl-base-1.0"
        hf_url = f"https://api-inference.huggingface.co/models/{hf_model}"
        hf_headers = {"Authorization": f"Bearer {hf_token}"}
        
        for attempt in range(1, 4):
            try:
                print(f"Requesting image from Hugging Face ({hf_model}) - Attempt {attempt}...")
                response = requests.post(hf_url, json={"inputs": prompt_en}, headers=hf_headers, timeout=60)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Successfully generated and saved Hugging Face wallpaper to {filename}!")
                    success = True
                    prompt_en = f"[Hugging Face SDXL] {prompt_en}"
                    break
                elif response.status_code == 503:
                    # Model loading, sleep and retry
                    estimated_time = response.json().get("estimated_time", 20)
                    print(f"Hugging Face model is loading. Waiting {estimated_time}s...")
                    time.sleep(estimated_time)
                else:
                    print(f"Hugging Face returned status code {response.status_code}: {response.text}")
                    time.sleep(3)
            except Exception as e:
                print(f"Hugging Face request failed: {type(e).__name__}")
                time.sleep(3)

    # 2. Try Pollinations AI as second option (Free, keyless, but subject to IP rate limits)
    if not success:
        print("Proceeding to Pollinations AI attempts...")
        # Try different URL variations (full URL first, then fallback to parameterless URL)
        urls_to_try = [
            f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true&seed={seed}",
            f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}",
            f"https://image.pollinations.ai/prompt/{encoded_prompt}%20seed%20{seed}"
        ]
        
        for url_attempt in urls_to_try:
            backoff = 3
            print(f"Targeting URL: {url_attempt}")
            for attempt in range(1, 4):
                try:
                    response = requests.get(url_attempt, timeout=60)
                    if response.status_code == 200:
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        print(f"Successfully saved Pollinations wallpaper to {filename}!")
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
                print("Current Pollinations URL strategy failed. Trying next strategy...")

    # 3. Try AI Horde (Stable Horde) anonymous API (Free, keyless, queue-based fallback)
    if not success:
        print("Pollinations AI rate-limited. Initiating AI Horde generation fallback...")
        horde_url = "https://aihorde.net/api/v2/generate/async"
        horde_headers = {
            "apikey": "0000000000",  # Anonymous API key
            "Client-Agent": "AetheriaWallpaperSystem:1.0:user@example.com"
        }
        
        # Explicitly request the most active models to ensure fast queue processing
        horde_payload = {
            "prompt": prompt_en,
            "models": ["stable_diffusion", "Dreamshaper", "Deliberate"],
            "params": {
                "width": 1024,
                "height": 576,
                "steps": 20,
                "cfg_scale": 7.0
            }
        }
        
        try:
            print("Submitting request to AI Horde...")
            submit_resp = requests.post(horde_url, json=horde_payload, headers=horde_headers, timeout=45)
            if submit_resp.status_code == 202:
                job_id = submit_resp.json().get("id")
                print(f"AI Horde accepted request! Job ID: {job_id}. Polling for results...")
                status_url = f"https://aihorde.net/api/v2/generate/status/{job_id}"
                
                # Poll status up to 36 times (3 minutes max)
                for poll in range(1, 37):
                    status_resp = requests.get(status_url, timeout=30)
                    if status_resp.status_code == 200:
                        status_data = status_resp.json()
                        if status_data.get("done") is True:
                            generations = status_data.get("generations", [])
                            if generations:
                                img_url = generations[0].get("img")
                                print(f"AI Horde finished! Downloading generated image from: {img_url}")
                                img_data = requests.get(img_url, timeout=45)
                                if img_data.status_code == 200:
                                    with open(filepath, 'wb') as f:
                                        f.write(img_data.content)
                                    print(f"Successfully saved AI Horde wallpaper to {filename}!")
                                    success = True
                                    prompt_en = f"[AI Horde Generated] {prompt_en}"
                                    break
                        elif status_data.get("faulted") is True:
                            print("AI Horde job failed (faulted).")
                            break
                    time.sleep(5)
            else:
                print(f"AI Horde submission failed: {submit_resp.status_code}")
        except Exception as e:
            print(f"AI Horde encountered error: {type(e).__name__}")
            
    # 4. CRITICAL LAST RESORT: Fall back to stock photos if all AI backends fail
    if not success:
        print("Both AI generation backends failed. Falling back to stock photo...")
        fallback_keywords = {
            "cyberpunk": "cyberpunk,neon,city,night,futuristic",
            "nature": "landscape,mountain,forest,waterfall,nature",
            "anime": "illustration,japanese,art,scenery",
            "minimalist": "minimalist,geometric,pastel,simple",
            "space": "galaxy,nebula,space,stars,astronaut",
            "abstract": "abstract,fluid,acrylic,smoke,art"
        }
        kw = fallback_keywords.get(category["id"], "wallpaper,landscape")
        fallback_url = f"https://picsum.photos/1920/1080?sig={timestamp}&q={kw}"
        
        for attempt in range(1, 4):
            try:
                response = requests.get(fallback_url, timeout=45)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Successfully saved last-resort stock wallpaper to {filename}!")
                    success = True
                    prompt_en = f"[Stock Photo fallback] Keywords: {kw.replace(',', ', ')}"
                    break
                else:
                    print(f"Fallback attempt {attempt} failed. Retrying...")
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
        # Generate RSS feed for Pinterest sync
        generate_rss_feed(existing_wallpapers)
        # Generate individual detail pages for all wallpapers
        generate_individual_pages(existing_wallpapers)
    else:
        print("Failed to generate image after trying all fallback and stock strategies.")

if __name__ == "__main__":
    main()
