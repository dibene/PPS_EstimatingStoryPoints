import gzip
import sys
import cPickle
import load_raw_text
import preprocess

# f_dict = gzip.open('apache.dict.pkl.gz', 'rb')
# dictionary = cPickle.load(f_dict)
# for x in range(0, 100):
#     print dictionary.keys()[dictionary.values().index(x+1)]

f = gzip.open('apache_pretrain.pkl.gz', 'rb')
train, valid, test = cPickle.load(f)

print train[1]
print valid[1]
print test[1]

