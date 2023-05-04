from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain #, SequentialChain

class Model:
    
    def __init__(self, text=None):
        self.llm = OpenAI(temperature=0.7)
        self.text = text 
        
    def detect(self):
        
        detection_template = PromptTemplate(
            input_variables=['text'],
            template="""You are a language detection model. 
            Your answers consist of only the language detected without full stops, leading or trailing spaces (or empty/new lines) (e.g. German).
            Do not leave an empty line or start a new line when givin an answer.
            If you detect more than one possible language you only give the most common one.
            What is the language of the following text: "{text}" """
        )
        detection_chain = LLMChain(llm=self.llm, prompt=detection_template, verbose=True, output_key='input_language')
        
        return detection_chain.run(text=self.text)
    
    def translate(self, lang_in, lang_out):
    
        translation_template = PromptTemplate(
            input_variables=['text', 'input_language', 'output_language'],
            template="""You are a language translation model, not a chatbot. You only provide the translation, nothing else.
            If the input and output languages are the same, leave the text unchanged.
            Do not precede the translation with something like "Answer:" or "Pronunciation:" or "English:".
            Translate the following {input_language} text to {output_language}: "{text}" """
        )
    
        translation_chain = LLMChain(llm=self.llm, prompt=translation_template, verbose=True, output_key='translation')

        return translation_chain.run(text=self.text, input_language=lang_in, output_language=lang_out)
    
    def pronounce(self, text, lang):
    
        pronunciation_template = PromptTemplate(
            input_variables=['text', 'language'],
            template="""You are a language pronunciation model, not a chatbot. 
            You only provide the pronunciation, nothing else. Do not precede the pronunciation with something like "Answer:" or "Pronunciation:".
            How do you pronounce the following {language} text: "{text}" """
        )
    
        pronunciation_chain = LLMChain(llm=self.llm, prompt=pronunciation_template, verbose=True, output_key='pronunciation')
        
        return pronunciation_chain.run(text=text, language=lang) 