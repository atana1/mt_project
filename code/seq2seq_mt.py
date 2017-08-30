

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Activation, RepeatVector, TimeDistributedDense, Dropout, Dense
from keras.layers import recurrent
from keras.layers.embeddings import Embedding
import numpy as np
from preprocess import preprocess
import pdb
RNN = recurrent.LSTM

class seq2seq(object):
    # Train a sequence to sequence model for hindi to english translation
    def __init__(self, maxlen, vocab_size):
        self.maxlen = maxlen
       # self.batch = batch
        self.proproces = preprocess("../indian-parallel-corpora/hi-en/tok/training.hi-en.hi",
                           "../indian-parallel-corpora/hi-en/tok/training.hi-en.en", maxlen, vocab_size)
        self.proproces.gen_vocab()
        #self.X_train = self.proproces.gen_seq_X("/home/shashank/datasets/MT-dataset/indian-parallel-corpora/hi-en/tok/training.hi-en.hi",
        #              "hindi")
        #self.Y_train = self.proproces.gen_seq_X("/home/shashank/datasets/MT-dataset/indian-parallel-corpora/hi-en/tok/training.hi-en.en",
        #              "english")
        #self.X_val = self.proproces.gen_seq_X("/home/shashank/datasets/MT-dataset/indian-parallel-corpora/hi-en/tok/dev.hi-en.hi",
        #              "hindi")
        #self.Y_val = self.proproces.gen_seq_X("/home/shashank/datasets/MT-dataset/indian-parallel-corpora/hi-en/tok/dev.hi-en.en.0",
        #              "english")
        #self.X_test = self.proproces.gen_seq_X("/home/shashank/datasets/MT-dataset/indian-parallel-corpora/hi-en/tok/test.hi-en.hi",
        #              "hindi")
        #self.Y_test = self.proproces.gen_seq_X("/home/shashank/datasets/MT-dataset/indian-parallel-corpora/hi-en/tok/test.hi-en.en.0",
        #              "english")

        #pdb.set_trace()
        #indices = np.arange(len(self.X_train))
        #np.random.shuffle(indices)
        #self.X_train = self.X_train[indices]
        #self.Y_train = self.Y_train[indices]
    
    def decode(self, prob):
        # Decodes the probability tensor into english sentence
        n_sent = prob.shape[0]
        for sent_id in range(n_sent):
            eng_ind = prob[sent_id].argmax(axis=-1)
            print eng_ind
            return ' '.join(self.proproces.vocab_en_rev[ind] for ind in eng_ind)
    
    def train_seq2seq(self):
        print "Input sequence read, starting training"
        #X_train = sequence.pad_sequences(self.X_train, maxlen=self.maxlen)
        #Y_train = sequence.pad_sequences(self.Y_train, maxlen=self.maxlen)
        #X_val = sequence.pad_sequences(self.X_val, maxlen=self.maxlen)
        #y_val = sequence.pad_sequences(self.Y_val, maxlen=self.maxlen)
        #X_test = sequence.pad_sequences(self.X_test, maxlen=self.maxlen)
        #Y_test = sequence.pad_sequences(self.Y_test, maxlen=self.maxlen)

        model = Sequential()
        model.add(Embedding(len(self.proproces.vocab_hind), 30,
                            input_length=self.maxlen))
        model.add(RNN(30))#, input_shape=(100, 128)))
        model.add(RepeatVector(self.maxlen))
        model.add(RNN(30, return_sequences=True))
        model.add(TimeDistributedDense(len(self.proproces.vocab_en)))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam',
                      metrics=['accuracy'])
        for e in range(100):
            print("epoch %d" % e)
            for (X,Y) in self.proproces.gen_seq("../indian-parallel-corpora/hi-en/tok/dev.hi-en.en.0",
                                 "../indian-parallel-corpora/hi-en/tok/dev.hi-en.hi",
                                           128):
                loss, acc = model.train_on_batch(X, Y)#, batch_size=64, nb_epoch=1)
                print("Loss is %f, accuracy is %f " % (loss, acc))
            # After one epoch test one sentence
            if e % 5 == 0 :
                print("Enter sentence in hindi")
                inp = raw_input().decode("utf-8")
                tokens = inp.split()
                seq = []
                for token in tokens:
                    if token in self.proproces.vocab_hind:
                        seq.append(self.proproces.vocab_hind[token])
                    else:
                        token = "UNK"
                        seq.append(self.proproces.vocab_hind[token])
                #seq = map(lambda x:self.proproces.vocab_hind[x], tokens)
                # Normalize seq to maxlen
                X = []
                X.append(seq)
                print X
                temp = sequence.pad_sequences(X, maxlen=self.maxlen)
                #temp[0:len(seq)] = seq
                print len(temp)
                #temp = np.asarray(temp).reshape(128,)
                print temp.shape
                prob = model.predict_on_batch(temp)#, batch_size=1, verbose=0)
                translated = self.decode(prob)
                print("Tranlated is", translated)
                print("Probabilities are", prob)
                print("Shape of prob tensor is",prob.shape)

if __name__ == "__main__":
    seq2seq = seq2seq(32, 5000)
    seq2seq.train_seq2seq()
