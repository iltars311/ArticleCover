import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import math
import textwrap
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Новые импорты для интеграции вашей логики
from llama_cpp import Llama
from huggingface_hub import InferenceClient

# --- Настройка окружения ---
# __file__ указывает на src/site.py
# .parent указывает на src/
# .parent.parent указывает на корень проекта ArticleCover/ (где лежит .env)
BASE_DIR = Path(__file__).resolve().parent.parent 
load_dotenv(BASE_DIR / '.env')
TOKEN = os.getenv('HUGGINGFACE_TOKEN')

# Конфигурация страницы - должна быть первой командой Streamlit
st.set_page_config(
    page_title="ArticleCover",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Проверка токена с выводом прямо в интерфейс приложения
if not TOKEN:
    st.error("🚨 Токен HuggingFace не найден! Убедитесь, что файл .env находится в корне проекта и содержит HUGGINGFACE_TOKEN.")
    st.stop() # Останавливаем отрисовку страницы, если токена нет

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
            height: 80vh; /* Чуть увеличили стартовую высоту */
            display: flex;
            flex-direction: column;
            overflow-y: auto; /* <-- Добавили прокрутку внутри колонки */
        }
        
        /* Красивый скроллбар для колонок */
        .stColumn::-webkit-scrollbar {
            width: 6px;
        }
        .stColumn::-webkit-scrollbar-track {
            background: transparent;
        }
        .stColumn::-webkit-scrollbar-thumb {
            background-color: #FF6B35;
            border-radius: 10px;
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


# --- ЗАГРУЗКА МОДЕЛЕЙ (кеширование для Streamlit) ---
@st.cache_resource(show_spinner=False)
def load_llm():
    # Измените путь на корректный, если GGUF лежит в другой папке проекта
    return Llama(
        model_path="meta-llama-3.1-8b-instruct.Q4_K_M.gguf", 
        n_ctx=2048,
        n_gpu_layers=-1,
        verbose=False
    )

@st.cache_resource(show_spinner=False)
def load_hf_client():
    return InferenceClient(model='black-forest-labs/FLUX.1-schnell', token=TOKEN)


# --- ФУНКЦИЯ ПОДГОТОВКИ ПОД A4 ---
def process_image_to_a4(img, title_text):
    """
    Адаптировано для работы напрямую с объектом PIL.Image (вместо чтения с диска),
    чтобы не создавать мусорных файлов в Streamlit.
    """
    img.load()
        
    W, H = img.size
    a4_ratio = math.sqrt(2)
    target_H = int(W * a4_ratio)
    strip_H = target_H - H

    if strip_H <= 50: 
        strip_H = int(W * 0.15) 
        target_H = H + strip_H 

    background_color = (30, 30, 30)
    new_img = Image.new("RGB", (W, target_H), background_color)
    new_img.paste(img, (0, strip_H))

    draw = ImageDraw.Draw(new_img)
    text_color = (255, 255, 255)
    
    text_x = W / 2
    text_y = strip_H / 2

    font_size = int(strip_H * 0.60)
    spacing = 15
    
    # Пытаемся загрузить шрифт Arial. Если скрипт будет запущен на Linux, 
    # нужно учесть падение и загрузить дефолтный шрифт.
    font_path = "C:/Windows/Fonts/arial.ttf"
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Для FreeType шрифтов считаем длину символа
    if hasattr(font, 'getlength'):
        while font_size >= 12:
            try:
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                font = ImageFont.load_default()

            char_width = font.getlength("A") if hasattr(font, 'getlength') else 10
            max_chars_per_line = max(10, int((W * 0.9) / char_width))
            wrapped_text = textwrap.fill(title_text, width=max_chars_per_line)
            lines = wrapped_text.split('\n')

            total_height = (len(lines) * font_size) + ((len(lines) - 1) * spacing)

            if total_height <= (strip_H * 0.80):
                break
            font_size -= 2
    else:
        # Резервный вариант, если truetype-шрифт недоступен (например, на сервере без Arial)
        max_chars_per_line = max(10, int((W * 0.9) / 10))
        wrapped_text = textwrap.fill(title_text, width=max_chars_per_line)

    draw.multiline_text(
        (text_x, text_y),
        wrapped_text,
        fill=text_color,
        font=font,
        anchor="mm",
        align="center",
        spacing=spacing
    )
    
    return new_img


# --- ОСНОВНАЯ ФУНКЦИЯ ГЕНЕРАЦИИ (интеграция вашей логики) ---
def generate_cover(title, abstract, prompt_model_name, image_model_name):
    # 1. Загружаем LLaMA (из кеша Streamlit)
    llm_model = load_llm()
    
    # Формируем prompt для LLaMA на основе аннотации
    full_input = f"""<|start_header_id|>user<|end_header_id|>

You are a scientific visualization expert and prompt engineer.

Create a prompt for an AI image generator that will produce an accurate and visually compelling cover image for a scientific paper.

CRITICAL RULES:
- Promts size should be 50-150 tokens
- Scientific accuracy: Visual elements must correctly represent the scientific concept
- No fictional or decorative elements that contradict the research
- Use correct scientific terminology in the prompt
- Output ONLY the prompt, no extra text
- Image must be in A4 format (portrait orientation, 1:sqrt(2) aspect ratio). Add this information to prompt.

PROMPT COMPONENTS:
1. Core scientific concept (what is being shown)
2. Specific visual details (colors, materials, lighting)
3. Style appropriate for the journal/conference
4. Composition and perspective

EXAMPLES:

Article: "Graphene-Based Battery with 10x Capacity"
Prompt: "Cross-section of graphene layered anode material, lithium ions intercalating between graphene sheets, electron flow visualized as golden energy streams, blue and gray color palette, scientific illustration style, cutaway view, detailed material texture"

Article: "Neural Network Explains Visual Cortex Activity"
Prompt: "Artificial neural network architecture overlaid on primate visual cortex diagram, activation patterns shown as colored heatmaps, connections between nodes mimicking biological pathways, academic illustration style, split-view showing both AI and biology, cool blue to warm red gradient"

Abstract:
{abstract}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

    st.toast("Генерация промпта в LLaMA...", icon="🧠")
    response = llm_model(
        full_input,
        max_tokens=250,
        temperature=0.2,
        stop=["<|eot_id|>", "</s>"]
    )
    generated_prompt = response['choices'][0]['text'].strip()
    
    # Выводим сгенерированный промпт в консоль Streamlit для отладки
    print(f"Generated Image Prompt: {generated_prompt}")
    
    # 2. Обращаемся к Hugging Face за картинкой (FLUX)
    st.toast("Отправка промпта в FLUX...", icon="🎨")
    client = load_hf_client()
    try:
        raw_image = client.text_to_image(generated_prompt)
    except Exception as e:
        st.error(f"Ошибка при генерации изображения: {e}")
        raise e

    # 3. Добавляем полосу A4 с названием сверху
    st.toast("Применяем формат обложки (A4)...", icon="📐")
    final_image = process_image_to_a4(raw_image, title)
    
    return final_image


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
        ["black-forest-labs/FLUX.1-schnell"], 
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
    # 1. Инициализация (если еще нет)
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    
    # 2. Заголовок (всегда сверху)
    st.markdown('<div class="column-title">🎨 Generated Cover</div>', unsafe_allow_html=True)

    # 3. Единая логика отображения (ЛИБО картинка, ЛИБО плейсхолдер)
    if st.session_state.generated_image is not None:
        # Блок управления скачиванием
        d_col1, d_col2 = st.columns([0.6, 0.4])
        with d_col2:
            fmt = st.selectbox("Format", ["PNG", "JPEG", "WebP"], 
                               label_visibility="collapsed", key="fmt_selector")
        with d_col1:
            img_buffer, mime_type, file_ext = prepare_image_for_download(
                st.session_state.generated_image, fmt
            )
            st.download_button(
                label=f"💾 DOWNLOAD {fmt}",
                data=img_buffer,
                file_name=f"cover_{datetime.now().strftime('%H%M%S')}.{file_ext}",
                mime=mime_type,
                use_container_width=True
            )
        
        # САМА КАРТИНКА (рисуется сразу под кнопкой)
        st.image(st.session_state.generated_image, use_container_width=True)
        
    else:
        # Плейсхолдер (высота минимальна, чтобы не толкать будущую картинку)
        st.markdown("""
            <div class="image-container" style="min-height: 100px; margin-top: 0;">
                <div style="text-align: center; padding: 20px;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">🎨</div>
                    <div style="font-size: 1.1rem; font-weight: bold; color: #FF6B35;">Ready to Generate</div>
                    <div style="font-size: 0.8rem; opacity: 0.7;">Fill the info and click Generate</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Обработка генерации
if generate_button:
    if title and abstract:
        with st.spinner("Generating cover... 🎨"):
            # Теперь вызываем нашу "боевую" функцию
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