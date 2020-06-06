from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

class TextToInput(object):
    def __init__(self):
        self.dir = 'Data/2015/'

    def convert_text_to_input(self, name=""):
        text_file = self.dir + name + "_text.txt" # _text_token.txt
        input_text_file = self.dir + name + "_text_input.txt"
        sen_max_length = -100

        rf = open(text_file, 'r')
        wf = open(input_text_file, 'w')
        while True:
            line = rf.readline()

            if line == "":
                break
            line = line.lower()
            line = line.replace("\n", "")
            line = line.replace('n\'t', 'not')
            line = line.replace('\'ve', 'have')
            line = line.replace('\'ll', 'will')
            line = line.replace('\'re', 'are')
            line = line.replace("'RT", "")
            line = line.replace("rt","")
            line = line.replace('\'m', 'am')
            line = line.replace('/', ' / ')
            line = line.replace('@', '')
            line = line.replace('#', '')
            line = line.replace('-', '')
            #line = line.replace('!', ' ')
            #line = line.replace('?', ' ')
            line = line.replace('+', ' ')
            line = line.replace('*', ' ')
            while "  " in line:
                line = line.replace('  ', ' ')
            while ",," in line:
                line = line.replace(',,', ',')
            line = line.strip()
            line = line.strip('.')
            line = line.strip()
            temp = line.count(' ') + 1
            if temp > sen_max_length:
                sen_max_length = temp
            wf.write(line + "\n")
        wf.close()
        rf.close()

        return sen_max_length

    def convert_aspect_to_input(self, name='', tk=None):
        aspect_text_file = self.dir + name + "_aspects_text.txt"
        aspect_text_index_file = self.dir + name + "_aspects_text_index.txt"
        aspect_text_input_file = self.dir + name + "_aspects_text_input.txt"
        aspect_max_length = -1

        aspect_texts = []
        rf = open(aspect_text_file, 'r')
        wf = open(aspect_text_input_file, 'w')
        while True:
            line = rf.readline()
            if line == "":
                break
            line = line.lower()
            line = line.replace("\n", "")
            line = line.replace('n\'t', 'not')
            line = line.replace('\'ve', 'have')
            line = line.replace('\'ll', 'will')
            line = line.replace('\'re', 'are')
            line = line.replace('\'m', 'am')
            line = line.replace('/', ' / ')
            line = line.replace('-', ' ')
            line = line.replace('#', '')
            line = line.replace('!', ' ')
            line = line.replace('?', ' ')
            line = line.replace('+', ' ')
            line = line.replace('*', ' ')
            while "  " in line:
                line = line.replace('  ', ' ')
            while ",," in line:
                line = line.replace(',,', ',')
            line = line.strip()
            line = line.strip('.')
            line = line.strip()

            temp = line.count(' ') + 1
            if temp > aspect_max_length:
                aspect_max_length = temp
            wf.write(line + "\n")

            aspect_texts.append(line)
        rf.close()
        wf.close()
        aspect_texts = tk.texts_to_sequences(aspect_texts)
        self.write_index_to_file(inputs=aspect_texts, file=aspect_text_index_file)

        print("max length of aspect is " + str(aspect_max_length))
        return aspect_texts

    def convert_aspect_to_label(self, name='', sentences=[]):
        # class_ids = {}
        aspect_label_file = self.dir + name + "_aspects_label.txt"
        aspect_label_index_file = self.dir + name + "_aspects_label_index.txt"
        text_index_file = self.dir + name + "_text_index.txt"
        rf = open(aspect_label_file, 'r')
        wf = open(aspect_label_index_file, 'w')

        labels = []
        sen_inputs = []
        while True:
            line = rf.readline()
            if line == "":
                break
            line = line.split("#")
            label = line[0]
            wf.write(str(label) + "\n")
            line_index = int(line[1])
            labels.append(label)
            sen_inputs.append(sentences[line_index])
        rf.close()
        wf.close()
        self.write_index_to_file(inputs=sen_inputs, file=text_index_file)
        return labels

    def read_text_file(self, name):
        input_text_file = self.dir + name + "_text_input.txt"
        rf = open(input_text_file, 'r')
        inputs = []
        while True:
            line = rf.readline()
            line = line.replace("\n", "")
            line.strip()
            if line == "":
                break
            inputs.append(line)
        rf.close()
        return inputs

    @staticmethod
    def convert_input_to_index(train_inputs=[], test_inputs=[], val_inputs=[],max_sen_length=40):
        print("start convert text to index.")
        tk = Tokenizer(num_words=20000, filters="", split=" ")
        tk.fit_on_texts(train_inputs)
        tk.fit_on_texts(test_inputs)
        tk.fit_on_texts(val_inputs)

        train_text_inputs = tk.texts_to_sequences(train_inputs)
        test_text_inputs = tk.texts_to_sequences(test_inputs)
        val_text_inputs = tk.texts_to_sequences(val_inputs)

        train_text_inputs = pad_sequences(train_text_inputs, maxlen=max_sen_length, padding='post') #post填充后面，pre前面
        test_text_inputs = pad_sequences(test_text_inputs, maxlen=max_sen_length, padding='post')
        val_text_inputs = pad_sequences(val_text_inputs, maxlen=max_sen_length, padding='post')
        print("finish!")
        return train_text_inputs, test_text_inputs, val_text_inputs, tk

    @staticmethod
    def write_index_to_file(inputs=[], file=''):
        wf = open(file, 'w')
        for line in inputs:
            for index in line:
                wf.write(str(index) + " ")
            wf.write("\n")
        wf.close()

    def write_word_index(self, word_index={}):
        word_index_file = self.dir + "word_index.txt"
        wf = open(word_index_file, 'w')
        for word, index in word_index.items():
            wf.write(word + " " + str(index) + "\n")
        wf.close()

if __name__ == '__main__':
    x = TextToInput()
    print("=== converting text to normal text ===")
    train_max = x.convert_text_to_input(name='train')
    test_max = x.convert_text_to_input(name='test')
    val_max = x.convert_text_to_input(name='val')

    max_len = max([train_max, test_max, val_max])
    print("The max length of sentence is " + str(max_len) + ".")  # 38text 8aspect

    print("===== converting normal text to index ====")
    train_sen_inputs = x.read_text_file(name='train')
    test_sen_inputs = x.read_text_file(name='test')
    val_sen_inputs = x.read_text_file(name='val')
    train_sen_inputs, test_sen_inputs,  val_sen_inputs, tk = TextToInput.convert_input_to_index(train_inputs=train_sen_inputs,test_inputs=test_sen_inputs,val_inputs=val_sen_inputs,max_sen_length=max_len)
    x.write_word_index(word_index=tk.word_index)

    print("==== converting aspect text to index ====")
    x.convert_aspect_to_input(name='train', tk=tk)
    x.convert_aspect_to_input(name='test', tk=tk)
    x.convert_aspect_to_input(name='val', tk=tk)

    #ids = dict(negative=0, positive=1, neutral=2, conflict=3)  # negative=0, positive=1, neutral=2, conflict=3
    print("== getting sentence index input and aspect label ==")
    x.convert_aspect_to_label(name='train', sentences=train_sen_inputs)
    x.convert_aspect_to_label(name='test', sentences=test_sen_inputs) #class_ids=ids
    x.convert_aspect_to_label(name='val', sentences=val_sen_inputs)
