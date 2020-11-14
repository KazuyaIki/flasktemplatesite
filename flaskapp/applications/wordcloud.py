from wordcloud import WordCloud
from datetime import datetime
import os
import re
from janome.tokenizer import Tokenizer

def word_cloud(text):
    basedir = os.path.abspath(os.path.dirname(__name__))
    d = datetime.now()
    time = f'{d:%Y%m%d%H%M%S}'
    file_abs_path = os.path.join(basedir, f"flaskapp/static/images/wordcloud/{str(time)}.png")

    if re.match(r'[a-zA-Z]', text):
        image = WordCloud(background_color="white", width=600,height=600).generate(text)
    else:
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(text)
        font_path = "C/windows/fonts/BIZ-UDゴシック/BIZ-UDGothicR.ttc"
        converted_text = ' '.join([token.base_form for token in tokens if token.part_of_speech.startswith(('名詞', '動詞', '副詞', '形容詞'))])
        image = WordCloud(background_color="white", width=600,height=600, font_path=font_path).generate(converted_text)

    image.to_file(file_abs_path)
    file_rel_path = file_abs_path.split('static/')[1]
  
    return file_rel_path