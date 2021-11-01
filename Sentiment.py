from nltk import NaiveBayesClassifier as nbc
from pythainlp.tokenize import word_tokenize
import pickle
import codecs
from itertools import chain


# pos.txt
with codecs.open('pos.txt', 'r', "utf-8") as f:
  lines = f.readlines()
listpos=[e.strip() for e in lines]
del lines
f.close() # ปิดไฟล์
# neg.txt
with codecs.open('neg.txt', 'r', "utf-8") as f:
  lines = f.readlines()
listneg=[e.strip() for e in lines]
del lines
f.close() # ปิดไฟล์


pos1=['pos']*len(listpos)
neg1=['neg']*len(listneg)
training_data = list(zip(listpos,pos1)) + list(zip(listneg,neg1)) 

vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))
feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]

classifier = nbc.train(feature_set)


print('start')

#save model
while True:
  save_classifier = open("Demonaivebayes.pickle","wb")
  pickle.dump(classifier, save_classifier)
  save_classifier.close()
  break
  # Message = input('\nข้อความ : ')
  # useSentiment(Message)

print('end')



