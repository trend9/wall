// Application State
let state = {
  lang: localStorage.getItem('lang') || 'ja',
  currentCategory: 'all',
  searchQuery: '',
  wallpapers: [],
  likedList: JSON.parse(localStorage.getItem('liked_wallpapers') || '[]'),
};

// UI Translations Dictionary
const TRANSLATIONS = {
  ja: {
    title: "Aetheria Wallpapers - AI生成4K壁紙",
    searchPlaceholder: "壁紙を検索...",
    allCategory: "すべて",
    emptyTitle: "壁紙が見つかりません",
    emptyDesc: "別のキーワードやカテゴリーで検索をお試しください。",
    download: "ダウンロード",
    copiedToast: "プロンプトをクリップボードにコピーしました！",
    footerTagline: "毎日6回自動更新されるAI壁紙ステーション",
    latestBadge: "最新の壁紙",
    resolution: "解像度: 1920 x 1080 (16:9)",
    dateLabel: "公開日: ",
    copyLabel: "コピー",
    promptTitle: "生成プロンプト"
  },
  en: {
    title: "Aetheria Wallpapers - AI-Generated 4K Wallpapers",
    searchPlaceholder: "Search wallpapers...",
    allCategory: "All",
    emptyTitle: "No wallpapers found",
    emptyDesc: "Try searching for a different keyword or category.",
    download: "Download",
    copiedToast: "Prompt copied to clipboard!",
    footerTagline: "AI Wallpaper Station, auto-updated 6 times daily",
    latestBadge: "LATEST WALLPAPER",
    resolution: "Resolution: 1920 x 1080 (16:9)",
    dateLabel: "Published: ",
    copyLabel: "COPY",
    promptTitle: "Generation Prompt"
  }
};

// Available Categories
const CATEGORY_NAMES = {
  all: { ja: "すべて", en: "All" },
  cyberpunk: { ja: "サイバーパンク", en: "Cyberpunk" },
  nature: { ja: "自然", en: "Nature" },
  anime: { ja: "アニメ", en: "Anime" },
  minimalist: { ja: "ミニマリスト", en: "Minimalist" },
  space: { ja: "宇宙", en: "Space" },
  abstract: { ja: "抽象画", en: "Abstract" }
};

// DOM Elements
const langToggle = document.getElementById('langToggle');
const searchInput = document.getElementById('searchInput');
const categoriesContainer = document.getElementById('categories-container');
const galleryGrid = document.getElementById('gallery-grid');
const heroSection = document.getElementById('hero-section');
const emptyState = document.getElementById('empty-state');
const emptyTitle = document.getElementById('empty-title');
const emptyDesc = document.getElementById('empty-desc');

// Modal Elements
const wallpaperModal = document.getElementById('wallpaperModal');
const modalClose = document.getElementById('modalClose');
const modalImg = document.getElementById('modalImg');
const modalCategoryBadge = document.getElementById('modalCategoryBadge');
const modalTitle = document.getElementById('modalTitle');
const modalDesc = document.getElementById('modalDesc');
const modalDate = document.getElementById('modalDate');
const modalResolution = document.getElementById('modalResolution');
const modalPromptText = document.getElementById('modalPromptText');
const modalDownloadBtn = document.getElementById('modalDownloadBtn');
const modalLikeBtn = document.getElementById('modalLikeBtn');
const copyPromptBtn = document.getElementById('copyPromptBtn');
const downloadText = document.getElementById('downloadText');

// Toast
const toast = document.getElementById('toast');

// Initialize Website
async function init() {
  updateLanguageUI();
  setupEventListeners();
  await loadWallpapersData();
  renderCategories();
  renderHero();
  renderGallery();
}

// Fetch Wallpapers JSON
async function loadWallpapersData() {
  try {
    const response = await fetch('data/wallpapers.json');
    if (response.ok) {
      state.wallpapers = await response.json();
    } else {
      console.warn("Could not find data/wallpapers.json or it's empty.");
    }
  } catch (error) {
    console.error("Failed to load wallpapers database:", error);
  }
}

// Update UI elements based on selected Language
function updateLanguageUI() {
  const t = TRANSLATIONS[state.lang];
  document.title = t.title;
  searchInput.placeholder = t.searchPlaceholder;
  emptyTitle.textContent = t.emptyTitle;
  emptyDesc.textContent = t.emptyDesc;
  document.getElementById('footer-tagline').textContent = t.footerTagline;
  downloadText.textContent = t.download;
  copyPromptBtn.textContent = t.copyLabel;
  toast.textContent = t.copiedToast;
  
  // Update HTML lang attribute
  document.documentElement.lang = state.lang;
  
  // Toggle button active classes
  langToggle.querySelectorAll('.lang-btn').forEach(btn => {
    if (btn.dataset.lang === state.lang) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
}

// Setup listeners
function setupEventListeners() {
  // Language Switch
  langToggle.addEventListener('click', (e) => {
    const btn = e.target.closest('.lang-btn');
    if (!btn) return;
    state.lang = btn.dataset.lang;
    localStorage.setItem('lang', state.lang);
    updateLanguageUI();
    renderCategories();
    renderHero();
    renderGallery();
  });

  // Search Input
  searchInput.addEventListener('input', (e) => {
    state.searchQuery = e.target.value.toLowerCase().trim();
    renderGallery();
  });

  // Close Modal
  modalClose.addEventListener('click', closeModal);
  wallpaperModal.addEventListener('click', (e) => {
    if (e.target === wallpaperModal) closeModal();
  });

  // Copy Prompt
  copyPromptBtn.addEventListener('click', () => {
    const text = modalPromptText.textContent;
    navigator.clipboard.writeText(text).then(() => {
      showToast();
    });
  });
  
  // Keyboard esc to close modal
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && wallpaperModal.classList.contains('active')) {
      closeModal();
    }
  });
}

// Render Categories filters
function renderCategories() {
  categoriesContainer.innerHTML = '';
  Object.keys(CATEGORY_NAMES).forEach(catId => {
    const name = CATEGORY_NAMES[catId][state.lang];
    const button = document.createElement('button');
    button.className = `cat-pill ${state.currentCategory === catId ? 'active' : ''}`;
    button.textContent = name;
    button.addEventListener('click', () => {
      state.currentCategory = catId;
      document.querySelectorAll('.cat-pill').forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      renderGallery();
    });
    categoriesContainer.appendChild(button);
  });
}

// Render Hero Showcase (Latest Wallpaper)
function renderHero() {
  if (state.wallpapers.length === 0) {
    heroSection.innerHTML = '';
    return;
  }

  const latest = state.wallpapers[0];
  const t = TRANSLATIONS[state.lang];
  const title = state.lang === 'ja' ? latest.title_ja : latest.title_en;
  const desc = state.lang === 'ja' ? latest.description_ja : latest.description_en;
  const catName = state.lang === 'ja' ? latest.category_name_ja : latest.category_name_en;
  const isLiked = state.likedList.includes(latest.id);

  heroSection.innerHTML = `
    <div class="hero-card">
      <img class="hero-img" src="wallpapers/${latest.filename}" alt="${title}">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <span class="badge">${t.latestBadge} • ${catName}</span>
        <h1 class="hero-title">${title}</h1>
        <p class="hero-desc">${desc}</p>
        <div class="hero-buttons">
          <button class="btn btn-primary" onclick="openWallpaperModal('${latest.id}')">
            <i data-feather="eye"></i>
            <span>${state.lang === 'ja' ? '詳細を見る' : 'View Details'}</span>
          </button>
          <a class="btn btn-secondary" href="wallpapers/${latest.filename}" download>
            <i data-feather="download"></i>
            <span>${t.download}</span>
          </a>
          <button class="btn btn-secondary btn-icon like-btn ${isLiked ? 'liked' : ''}" onclick="toggleLike(event, '${latest.id}')">
            <i data-feather="heart"></i>
          </button>
        </div>
      </div>
    </div>
  `;
  feather.replace();
}

// Get filtered list of wallpapers
function getFilteredWallpapers() {
  return state.wallpapers.filter(wp => {
    // Category match
    const categoryMatch = state.currentCategory === 'all' || wp.category === state.currentCategory;
    
    // Search match
    const query = state.searchQuery;
    const titleMatch = wp.title_en.toLowerCase().includes(query) || wp.title_ja.toLowerCase().includes(query);
    const descMatch = wp.description_en.toLowerCase().includes(query) || wp.description_ja.toLowerCase().includes(query);
    const catMatch = wp.category_name_en.toLowerCase().includes(query) || wp.category_name_ja.toLowerCase().includes(query);
    
    return categoryMatch && (titleMatch || descMatch || catMatch);
  });
}

// Render Gallery Grid
function renderGallery() {
  galleryGrid.innerHTML = '';
  const filtered = getFilteredWallpapers();
  const t = TRANSLATIONS[state.lang];

  if (filtered.length === 0) {
    emptyState.style.display = 'flex';
    galleryGrid.style.display = 'none';
    return;
  }

  emptyState.style.display = 'none';
  galleryGrid.style.display = 'grid';

  filtered.forEach(wp => {
    const title = state.lang === 'ja' ? wp.title_ja : wp.title_en;
    const desc = state.lang === 'ja' ? wp.description_ja : wp.description_en;
    const catName = state.lang === 'ja' ? wp.category_name_ja : wp.category_name_en;
    const isLiked = state.likedList.includes(wp.id);

    const card = document.createElement('div');
    card.className = 'wallpaper-card';
    card.innerHTML = `
      <div class="card-img-wrapper" onclick="openWallpaperModal('${wp.id}')">
        <img class="card-img" src="wallpapers/${wp.filename}" alt="${title}" loading="lazy">
        <div class="card-tags">
          <span class="card-free">${state.lang === 'ja' ? '無料ダウンロード' : 'Free Download'}</span>
          <span class="card-cat">${catName}</span>
        </div>
      </div>
      <div class="card-info">
        <h3 class="card-title">${title}</h3>
        <p class="card-desc">${desc}</p>
        <div class="card-footer">
          <a href="wallpapers/${wp.filename}" class="btn btn-primary" download style="padding: 0.5rem 1rem; font-size: 0.85rem; border-radius: 8px;">
            <i data-feather="download" style="width: 16px; height: 16px;"></i>
            <span>${t.download}</span>
          </a>
          <button class="btn btn-secondary btn-icon like-btn ${isLiked ? 'liked' : ''}" style="width: 36px; height: 36px; border-radius: 8px;" onclick="toggleLike(event, '${wp.id}')">
            <i data-feather="heart" style="width: 16px; height: 16px;"></i>
          </button>
        </div>
      </div>
    `;
    galleryGrid.appendChild(card);
  });
  feather.replace();
}

// Open Details Modal
window.openWallpaperModal = function(id) {
  const wp = state.wallpapers.find(w => w.id === id);
  if (!wp) return;

  const t = TRANSLATIONS[state.lang];
  const title = state.lang === 'ja' ? wp.title_ja : wp.title_en;
  const desc = state.lang === 'ja' ? wp.description_ja : wp.description_en;
  const catName = state.lang === 'ja' ? wp.category_name_ja : wp.category_name_en;
  const isLiked = state.likedList.includes(wp.id);

  modalImg.src = `wallpapers/${wp.filename}`;
  modalImg.alt = title;
  modalCategoryBadge.textContent = catName;
  modalTitle.textContent = title;
  modalDesc.textContent = desc;
  
  modalDate.textContent = `${t.dateLabel}${wp.date}`;
  modalResolution.textContent = t.resolution;
  modalPromptText.textContent = wp.prompt;
  
  modalDownloadBtn.href = `wallpapers/${wp.filename}`;
  
  // Configure like button inside modal
  modalLikeBtn.className = `btn btn-secondary btn-icon like-btn ${isLiked ? 'liked' : ''}`;
  modalLikeBtn.onclick = (e) => {
    toggleLike(e, wp.id);
    modalLikeBtn.className = `btn btn-secondary btn-icon like-btn ${state.likedList.includes(wp.id) ? 'liked' : ''}`;
  };

  wallpaperModal.classList.add('active');
  document.body.style.overflow = 'hidden'; // Stop scrolling
  feather.replace();
};

// Close Details Modal
function closeModal() {
  wallpaperModal.classList.remove('active');
  document.body.style.overflow = ''; // Restore scrolling
}

// Toggle Like
window.toggleLike = function(event, id) {
  event.stopPropagation();
  const idx = state.likedList.indexOf(id);
  if (idx > -1) {
    state.likedList.splice(idx, 1);
  } else {
    state.likedList.push(id);
  }
  localStorage.setItem('liked_wallpapers', JSON.stringify(state.likedList));
  
  // Refresh views to show updated like statuses
  renderHero();
  renderGallery();
};

// Toast notification trigger
function showToast() {
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 2500);
}

// Start Application
window.addEventListener('DOMContentLoaded', init);
