
from keras.preprocessing.text import Tokenizer
import codecs
import pdb


class preprocess(object):
    # Preprocessing for hindi to english
    def __init__(self, path_hindi, path_eng, max_feat, max_len):
        self.path_hindi = path_hindi
        self.path_eng = path_eng
        self.max_feat = max_feat
        self.max_len = max_len


    def preprocess_X(self):
        # Preprocessing hindi corpus
        text_hindi =[line.rstrip() for line in open(self.path_hindi).readlines()]
        #text_eng = [line.rstrip() for line in codecs.open(self.path_eng, encoding='utf-8').readlines()]
        text_eng = [line.rstrip() for line in open(self.path_eng).readlines()]

        print text_hindi
        tokenizer = Tokenizer(1000)
        tokenizer.fit_on_texts(text_eng)
        text_seq = tokenizer.texts_to_sequences(text_eng)
        tokenizer1 = Tokenizer(1000)
        tokenizer1.fit_on_texts(text_hindi)
        text_seq = tokenizer1.texts_to_sequences(text_hindi)
        
        pdb.set_trace()
        

if __name__ == "__main__":
    pre = preprocess('../indian-parallel-corpora/hi-en/training.hi-en.en', '../indian-parallel-corpora/hi-en/training.hi-en.en', 800, 10)
    pre.preprocess_X()
