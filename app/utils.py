import openai
from sqlalchemy.orm import Session
import torch
from transformers import MarianMTModel, AutoTokenizer, M2M100ForConditionalGeneration, M2M100Tokenizer
from crud import update_translation_task
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
# def perform_translation(task_id: int, text: str, languages: list, db: Session):
#     translations = {}
#     for lang in languages:
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 message=[
#                     {"role": "system", "content":f"You are a helpful assistant that translates text into {lang} "},
#                     {"role": "user", "content": text}
#                 ],
#                 max_tokens=1000
#             )
#             translated_text = response['choices'][0]['messange']['content'].strip()
#             translations[lang] = translated_text
#         except Exception as e:
#             print(f"Error translating to {lang}: {e}")
#             translations[lang] = f"Error: {e}"
#         except Exception as e:
#             print(f"Unexpected error: {e}")
#             translations[lang] = f"Unexpected error: {e}"

#     update_translation_task(db, task_id, translations)

    
# def perform_translation(task_id: int, text: str, languages: list, db: Session):
#     translations = {}
#     model_name = "facebook/m2m100_418M"
#     model = M2M100ForConditionalGeneration.from_pretrained(model_name)
#     tokenizer = M2M100Tokenizer.from_pretrained(model_name)

#     for lang in languages:
#         try:
#             # Prepare the input text
#             input_text = text
#             target_lang = lang.split("_")[0]  # e.g., "vi" for "vi_VN"

#             # Tokenize the input text
#             model_inputs = tokenizer(input_text, return_tensors="pt")

#             # Set the target language
#             model_inputs["forced_bos_token_id"] = tokenizer.get_lang_id(target_lang)

#             # Generate the translation
#             generated = model.generate(**model_inputs)
#             translated_text = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

#             translations[lang] = translated_text
#         except Exception as e:
#             print(f"Error translating to {lang}: {e}")
#             translations[lang] = f"Error: {e}"

#     update_translation_task(db, task_id, translations)

from transformers import MarianMTModel, MarianTokenizer

# Language name to code mapping
language_mapping = {
    "vietnamese": "vi",
    "french": "fr",
    "german": "de",
    # Add more languages as needed
}

def perform_translation(task_id: int, text: str, languages: list, db: Session):
    translations = {}

    for lang in languages:
        try:
            # Convert language name to code
            lang_code = language_mapping.get(lang.lower())
            if not lang_code:
                raise ValueError(f"Unsupported language: {lang}")

            # Use Helsinki-NLP/Opus-MT models
            model_name = f"Helsinki-NLP/opus-mt-en-{lang_code}"
            model = MarianMTModel.from_pretrained(model_name)
            tokenizer = MarianTokenizer.from_pretrained(model_name)

            # Tokenize the input text
            model_inputs = tokenizer(text, return_tensors="pt")

            # Generate the translation
            generated = model.generate(**model_inputs)
            translated_text = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

            translations[lang] = translated_text
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
            translations[lang] = f"Error: {e}"

    update_translation_task(db, task_id, translations)

