import streamlit as st
from llama_cpp import Llama

# Настройка внешнего вида страницы
st.set_page_config(page_title="Генератор обложек", page_icon="🎨", layout="centered")

@st.cache_resource
def load_model():
    return Llama(
        model_path="meta-llama-3.1-8b-instruct.Q4_K_M.gguf", 
        n_ctx=2048,
        n_gpu_layers=-1,
        verbose=False
    )

st.title("🎨 Генератор промтов для обложек")
st.write("Вставьте абстракт научной статьи, и нейросеть подготовит детализированный промт для генерации изображения.")

# Загружаем модель (сработает один раз при запуске)
try:
    model = load_model()
except Exception as e:
    st.error(f"Ошибка загрузки! Проверьте, лежит ли файл .gguf в той же папке.\nДетали: {e}")
    st.stop()

# Поле для ввода текста
abstract_text = st.text_area("Текст абстракта:", height=250, placeholder="Вставьте текст статьи сюда...")

if st.button("Сгенерировать промт", type="primary"):
    if abstract_text.strip():
        with st.spinner('Нейросеть читает абстракт и думает над визуалом...'):
            
            # Оборачиваем текст в формат Llama 3 Instruct
            prompt_template = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>

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
Prompt: "Artificial neural network architecture overlaid on primate visual cortex diagram, activation patterns shown as colored heatmaps, connections between nodes mimicking biological pathways, academic illustration style, split-view showing both AI and biology, cool blue to warm red gradient

Abstract:
{abstract_text}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
            
            # Запускаем генерацию
            response = model(
                prompt_template,
                max_tokens=250,      # Лимит длины для генерируемого промта
                temperature=0.3,     # Легкая креативность, но без галлюцинаций
                stop=["<|eot_id|>", "</s>"]
            )
            
            # Достаем чистый текст ответа
            result = response['choices'][0]['text'].strip()
            
            st.success("Готово!")
            st.code(result, language="text") # Выводим в удобном блоке с кнопкой "Копировать"
    else:
        st.warning("Пожалуйста, введите текст абстракта перед генерацией.")