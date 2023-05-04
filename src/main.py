from dotenv import load_dotenv
import streamlit as st
from model import Model

load_dotenv(override=True)

model = Model()

languages = ('English', 'German', 'Dutch', 'Russian', 'Spanish', 'Italian', 'Portuguese')

st.title('GPT Translator')

# Sidebar with pronunciation language selector.
with st.sidebar:
    st.title("Settings")
    pronunciation_lang = st.radio('Pronounce:', ('Input', 'Output'))

# Input and translation language selection.
col1, col2 = st.columns(2)
with col1:
    input_lang = st.selectbox('Input Language:', ['Auto'] + list(languages))
with col2:
    output_lang = st.selectbox('Translate to:', languages)

# Prompt and complete input display.
tab1, tab2 = st.tabs(['Prompt', 'Text'])
with tab1:
    prompt = st.text_input("Text to be translated.")
with tab2:
    st.write(prompt)

# Translation and pronunciation outputs 
if prompt:
    
    model.text = prompt
    
    # Input language
    if input_lang == 'Auto':
        input_language = model.detect()
        input_language = input_language.strip("\n")
        st.info(f"Language Detected: {input_language}")
    elif input_lang != 'Auto':
        input_language = input_lang
    
    translation = model.translate(lang_in=input_language, lang_out=output_lang)
    
    pronunciation = model.pronounce(text=prompt if pronunciation_lang=='Input' else translation, 
                                                  lang=input_language if pronunciation_lang=='Input' else output_lang)
    
    # Show output if input and output languages differ.
    if input_language != output_lang:

        st.header("Translation")
        st.write(translation)

        with st.expander(f"{pronunciation_lang}'s pronunciation."):
            st.write(pronunciation)
            
    else:
        st.warning('Input and Output languages are the same!', icon="⚠️")
