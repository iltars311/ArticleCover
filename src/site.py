import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np
from datetime import datetime

# Конфигурация страницы - должна быть первой командой
st.set_page_config(
    page_title="ArticleCover",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Кастомный CSS для оранжево-белой темы и фиксации высоты
st.markdown("""
    <style>
        /* Основные цвета */
        :root {
            --orange: #FF6B35;
            --orange-light: #FF8C5A;
            --white: #FFFFFF;
            --gray-light: #F5F5F5;
        }
        
        /* Убираем отступы и фиксируем высоту */
        .main > div {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        
        /* Заголовок с логотипом */
        .header-logo {
            text-align: center;
            padding: 0 0 0 0;
            border-bottom: 2px solid #FF6B35;
            margin-bottom: 1rem;
        }
        
        .header-logo h1 {
            color: #FF6B35;
            font-size: 3rem;
            font-weight: bold;
            margin: 0;
            display: inline-block;
        }
        
        /* Стили для колонок */
        .stColumn {
            background-color: #4E4E4E;
            border-radius: 10px;
            padding: 1rem;
            height: 80vh;
            display: flex;
            flex-direction: column;
        }
        
        /* Заголовки колонок */
        .column-title {
            color: #FF6B35;
            font-size: 1.7rem;
            font-weight: bold;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #FF6B35;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* Стили для комбинированной кнопки загрузки в заголовке */
        .title-download-area {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        
        .title-download-btn {
            background-color: #FF6B35;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 0.9rem;
            padding: 6px 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: inherit;
            white-space: nowrap;
        }
        
        .title-download-btn:hover {
            background-color: #FF8C5A;
            transform: scale(1.02);
        }
        
        .title-format-select {
            background-color: #FF6B35;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 0.9rem;
            padding: 6px 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: inherit;
        }
        
        .title-format-select:hover {
            background-color: #FF8C5A;
        }
        
        .title-format-select option {
            background-color: #FF6B35;
            color: white;
        }
        
        /* Стили для текстовых полей */
        .stTextArea textarea {
            background-color: #26282F;
            border: 1px solid #FF6B35;
            border-radius: 5px;
            font-size: 1.5rem;
        }
            
        .stTextArea textarea::placeholder {
            color: #98989D;
        }
            
        /* Кнопка генерации */
        .stButton button {
            background-color: #FF6B35;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            transition: all 0.3s ease;
            margin-top: 5.6rem;
            margin-bottom: 1rem;
            cursor: pointer;
        }
        
        /* Выпадающие списки */
        .stSelectbox div[data-baseweb="select"] {
            border-color: #FF6B35;
            margin-top: 0rem;
        }
        
        /* Контейнер для изображения */
        .image-container {
            background-color: #2C2C2C;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        /* Убираем прокрутку для всего приложения */
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            max-width: 100%;
        }
        
        /* Стили для placeholder */
        .placeholder-text {
            color: #879BA6;
            text-align: center;
            padding: 5rem;
            font-style: italic;
        }
        
        /* Адаптация высоты */
        html, body, .stApp {
            height: 100vh;
            overflow: hidden;
            background: #0E1116;
        }
        
        .main {
            height: 100vh;
            overflow: hidden;
        }
        
        /* Центрирование содержимого колонок */
        .centered-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            height: 100%;
        }
        
        /* Стили для декоративного изображения */
        .decorative-image {
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C5A 100%);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            margin-top: 1rem;
            color: white;
            font-size: 0.9rem;
        }
        
        hr {
            margin: 0.5rem 0;
        }
        
        /* Уменьшаем отступы между элементами в средней колонке */
        .centered-content .stButton {
            margin-bottom: 0rem;
            margin-top: 10rem;
        }
        
        .centered-content hr {
            margin: 0 12rem;
        }
        
        .centered-content .stMarkdown {
            margin-bottom: 0.2rem;
        }
        
        /* Стили для выпадающих списков */
        .centered-content .stSelectbox {
            margin-bottom: 0.3rem;
        }
    </style>
""", unsafe_allow_html=True)

# Функция для генерации обложки (имитация работы AI)
def generate_cover(title, abstract, prompt_model, image_model):
    """
    Генерирует обложку на основе названия и аннотации статьи
    В реальном приложении здесь должен быть вызов AI моделей
    """
    # Создаем изображение с соотношением сторон 1:sqrt(2) ≈ 1:1.414
    width = 800
    height = int(width * 1.414)  # 800x1131
    
    # Создаем градиентный фон
    img = Image.new('RGB', (width, height), color='#FF6B35')
    draw = ImageDraw.Draw(img)
    
    # Добавляем оранжевый градиент
    for i in range(height):
        color_value = int(255 - (i / height) * 100)
        draw.rectangle([0, i, width, i+1], fill=(255, int(107 - (i/height)*50), 53))
    
    # Пытаемся загрузить шрифт, если нет - используем дефолтный
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
    
    # Добавляем название
    title_text = title[:50] + "..." if len(title) > 50 else title
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, height//4), title_text, fill='white', font=font_title)
    
    # Добавляем абстракт (первые 3 строки)
    abstract_lines = abstract[:200].split('\n')
    y_offset = height//2
    for i, line in enumerate(abstract_lines[:3]):
        bbox = draw.textbbox((0, 0), line, font=font_text)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, y_offset + i*30), line, fill='white', font=font_text)
    
    # Добавляем декоративные элементы
    draw.rectangle([50, height-100, width-50, height-70], fill='#FF8C5A', outline='white', width=2)
    draw.text((width//2 - 100, height-95), "ArticleCover", fill='white', font=font_text)
    
    # Добавляем информацию о моделях
    draw.text((10, height-30), f"Prompt: {prompt_model}", fill='white', font=font_text)
    draw.text((width-200, height-30), f"Image: {image_model}", fill='white', font=font_text)
    
    return img

# Функция для подготовки изображения к скачиванию
def prepare_image_for_download(img, format_choice):
    """Подготавливает изображение к скачиванию в выбранном формате"""
    img_buffer = io.BytesIO()
    
    if format_choice == "PNG":
        img.save(img_buffer, format="PNG")
        mime_type = "image/png"
        file_ext = "png"
    elif format_choice == "JPEG":
        # Конвертируем в RGB для JPEG
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        img.save(img_buffer, format="JPEG", quality=95)
        mime_type = "image/jpeg"
        file_ext = "jpg"
    else:  # WebP
        img.save(img_buffer, format="WEBP", quality=90)
        mime_type = "image/webp"
        file_ext = "webp"
    
    img_buffer.seek(0)
    return img_buffer, mime_type, file_ext

# Заголовок с логотипом
st.markdown("""
    <div class="header-logo">
        <h1>📄 ArticleCover</h1>
    </div>
""", unsafe_allow_html=True)

# Создаем три колонки с заданными пропорциями: 40% | 20% | 40%
col1, col2, col3 = st.columns([0.45, 0.20, 0.35])

# Первая колонка - ArticleInfo
with col1:
    st.markdown('<div class="column-title">📝 Article Info</div>', unsafe_allow_html=True)
    
    title = st.text_area(
        "Title",
        placeholder="Enter your article title here...",
        height=100,
        key="title_input",
        label_visibility="collapsed"
    )
    
    abstract = st.text_area(
        "Abstract",
        placeholder="Enter your article abstract here...",
        height=500,
        key="abstract_input",
        label_visibility="collapsed"
    )

# Вторая колонка - кнопка и модели
with col2:
    st.markdown('<div class="centered-content">', unsafe_allow_html=True)
    
    # Кнопка Generate
    generate_button = st.button("GENERATE", use_container_width=True)
    
    # Выпадающие списки
    st.markdown("**Prompt Model**")
    prompt_model = st.selectbox(
        "Select prompt generation model",
        ["LLaMA-3.1-8B"],
        label_visibility="collapsed",
        key="prompt_model"
    )
    
    st.markdown("**Image Model**")
    image_model = st.selectbox(
        "Select image generation model",
        [""],
        label_visibility="collapsed",
        key="image_model"
    )
    
    # Декоративное изображение
    try:
        deco_img = Image.open("../ico/ai.png")
        st.image(deco_img, use_container_width=True)
    except:
        st.markdown("""
            <div class="decorative-image" style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C5A 100%);">
                🤖 AI Powered
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    # Инициализация session state
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    if 'download_format' not in st.session_state:
        st.session_state.download_format = "PNG"
    
    # Создаем HTML для заголовка с кнопкой
    format_options = ["PNG", "JPEG", "WebP"]
    format_options_html = "".join([
        f'<option value="{f}" {"selected" if st.session_state.download_format == f else ""}>{f}</option>' 
        for f in format_options
    ])
    
    # Отображаем заголовок с комбинированной кнопкой через HTML с JavaScript
    st.markdown(f"""
        <div class="column-title">
            <span>🎨 Generated Cover</span>
            <div class="title-download-area">
                <button id="download-title-btn" class="title-download-btn" onclick="triggerDownload()">
                    DOWNLOAD
                </button>
                <select id="format-title-select" class="title-format-select" onchange="updateFormatAndButton(this.value)">
                    {format_options_html}
                </select>
            </div>
        </div>
        
        <script>
            let currentFormat = '{st.session_state.download_format}';
            
            function updateFormatAndButton(format) {{
                currentFormat = format;
                const btn = document.getElementById('download-title-btn');
                btn.innerHTML = '💾 DOWNLOAD ' + format;
                
                // Сохраняем выбранный формат в sessionStorage
                sessionStorage.setItem('selectedFormat', format);
            }}
            
            function triggerDownload() {{
                const format = document.getElementById('format-title-select').value;
                
                // Создаем ссылку для скачивания через Streamlit
                const downloadUrl = `/download?format=${{format}}&timestamp=${{Date.now()}}`;
                
                // Сохраняем формат и запускаем скачивание через Streamlit
                sessionStorage.setItem('downloadTrigger', 'true');
                sessionStorage.setItem('downloadFormat', format);
                
                // Перезагружаем страницу с параметром для скачивания
                window.location.href = window.location.pathname + '?download=' + format;
            }}
            
            // Восстанавливаем выбранный формат при загрузке страницы
            document.addEventListener('DOMContentLoaded', function() {{
                const savedFormat = sessionStorage.getItem('selectedFormat');
                if (savedFormat) {{
                    const select = document.getElementById('format-title-select');
                    if (select) {{
                        select.value = savedFormat;
                        updateFormatAndButton(savedFormat);
                    }}
                }}
            }});
        </script>
    """, unsafe_allow_html=True)
    
    # Обработка скачивания через query parameters
    import urllib.parse
    query_params = st.query_params
    
    if 'download' in query_params and st.session_state.generated_image is not None:
        format_to_download = query_params['download']
        if format_to_download in ["PNG", "JPEG", "WebP"]:
            img_buffer, mime_type, file_ext = prepare_image_for_download(
                st.session_state.generated_image,
                format_to_download
            )
            st.download_button(
                label="Download",
                data=img_buffer,
                file_name=f"article_cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}",
                mime=mime_type,
                key="download_btn_auto"
            )
            # Очищаем параметр после скачивания
            st.query_params.clear()
    
    # Показываем изображение или плейсхолдер
    if st.session_state.generated_image is not None:
        st.image(st.session_state.generated_image, use_container_width=True)
    else:
        # Плейсхолдер для изображения
        st.markdown("""
            <div class="image-container">
                <div style="
                    border-radius: 10px;
                    padding: 2rem;
                    min-height: 584px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🎨</div>
                    <div style="font-size: 1.2rem; font-weight: bold;">No cover generated yet</div>
                    <div style="font-size: 0.9rem; margin-top: 0.5rem;">Fill in the article info and click Generate</div>
                    <div style="font-size: 0.8rem; margin-top: 1rem;">Aspect ratio: 1 : √2</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
# Обработка генерации
if generate_button:
    if title and abstract:
        with st.spinner("Generating cover... 🎨"):
            img = generate_cover(title, abstract, prompt_model, image_model)
            st.session_state.generated_image = img
            st.rerun()
    else:
        st.warning("Please fill in both Title and Abstract fields!")

# Добавляем информацию внизу
st.markdown("""
    <div style="
        position: fixed;
        bottom: 10px;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 0.7rem;
        color: #FF6B35;
        opacity: 0.7;
        pointer-events: none;
    ">
        ArticleCover | AI-powered scientific article cover generator
    </div>
""", unsafe_allow_html=True)