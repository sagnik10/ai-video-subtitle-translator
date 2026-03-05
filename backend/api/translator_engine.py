from transformers import MarianMTModel, MarianTokenizer

MODELS = {
    "he": "Helsinki-NLP/opus-mt-en-he",
    "fr": "Helsinki-NLP/opus-mt-en-fr",
    "es": "Helsinki-NLP/opus-mt-en-es"
}

tokenizers = {}
models = {}

def load_model(lang):

    if lang not in models:

        model_name = MODELS[lang]

        tokenizers[lang] = MarianTokenizer.from_pretrained(model_name)
        models[lang] = MarianMTModel.from_pretrained(model_name)

    return tokenizers[lang], models[lang]


def translate(text, lang):

    tokenizer, model = load_model(lang)

    tokens = tokenizer(text, return_tensors="pt", padding=True)

    translated = model.generate(**tokens)

    return tokenizer.decode(translated[0], skip_special_tokens=True)