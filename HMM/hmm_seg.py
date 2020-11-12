from HMM.hmm_model import HMM
import codecs

text = '研究生命的起源'
hmm = HMM()
train_data = '../data/pku_training.utf8'
test_path = "../data/pku_test.utf8"
result_path = "pku_result.utf8"
model_file = 'hmm_model.pkl'

hmm = HMM()
hmm.train(open(train_data, 'r', encoding='utf-8'), model_file)
hmm.load_model(model_file)


def divideWords(model, sentence):
    """
    根据词典对句子进行分词,
    使用正向匹配的算法，从左到右扫描，遇到最长的词，
    就将它切下来，直到句子被分割完闭
    """
    result = []
    start = 0
    sentence = sentence.split(u'\r\n')
    senlen = len(sentence)
    while start < senlen:
        curSentence = sentence[start]
        curSplit = model.cut(curSentence)
        result.extend(curSplit)
        result.append("\r")
        result.append("\n")
    return result

fr = codecs.open(test_path,'r','utf-8')
test = fr.read()
result = divideWords(hmm,test)
fr.close()
fw = codecs.open(result_path,'w','utf-8')
for item in result:
    fw.write(item + ' ')
fw.close()
