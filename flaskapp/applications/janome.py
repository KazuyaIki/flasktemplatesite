from janome.tokenizer import Tokenizer

def jano_me(pos, text):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text)
    font_path = "C/windows/fonts/BIZ-UDゴシック/BIZ-UDGothicR.ttc"
    word_list = [token.base_form for token in tokens if token.part_of_speech.startswith(pos)]
    word_dict = {}
    for word in word_list:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    word_dict = sorted(word_dict.items(), key=lambda x:x[1], reverse=True)
    return word_dict