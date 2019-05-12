#
#
#

chosen_frequency = 30
import cPickle as pkl
import numpy
import sys
from sklearn.cross_validation import StratifiedKFold
import gzip

import load_raw_text

from subprocess import Popen, PIPE

# tokenizer.perl is from Moses: https://github.com/moses-smt/mosesdecoder/tree/master/scripts/tokenizer
tokenizer_cmd = ['/usr/bin/perl', 'tokenizer.perl', '-l', 'en', '-q', '-']

def tokenize(sentences):

    print 'Tokenizing..',
    text = "\n".join(sentences)
    tokenizer = Popen(tokenizer_cmd, stdin=PIPE, stdout=PIPE)
    tok_text, _ = tokenizer.communicate(text)
    toks = tok_text.split('\n')[:-1]
    print 'Done'

    return toks

    # frecuencias de las palabras
    # indices ordenados de mayor a menor
    # palabra[valor_ordenado] = index
    # por lo tanto le da un numero mas bajo a los que tienen mayor frecuencia y mas alto al de menor frecuencia
def build_dict(sentences):
    #devuelve array de sentencias
    sentences = tokenize(sentences)

    print 'Building dictionary..'
    # key palabra value frecuencia
    wordcount = dict()
    for ss in sentences:
        words = ss.strip().lower().split()
        for w in words:
            if w not in wordcount:
                wordcount[w] = 1
            else:
                wordcount[w] += 1
    #frecuencias de las palabras
    counts = wordcount.values()
    #palabras
    keys = wordcount.keys()
    # indices ordenados de mayor a menor
    sorted_idx = numpy.argsort(counts)[::-1]
    counts = numpy.array(counts)

    print 'number of words in dictionary:', len(keys)

    worddict = dict()

    # counter = idx , value = ss
    # palabra[valor_ordenado] = index
    for idx, ss in enumerate(sorted_idx):
        worddict[keys[ss]] = idx+1  # leave 0 (UNK)

    # se fija en que posicion( cantidad de palabras) hay con mayor frecuencia a X
    pos = 0
    for i, c in enumerate(sorted_idx):
        if counts[c] >= chosen_frequency: pos = i

    print numpy.sum(counts), ' total words, ', pos, 'words with frequency >=', chosen_frequency

    return worddict

# cambia la palabra por el valor del diccionario
def grab_data(title, description, dictionary):
    title = tokenize(title)
    description = tokenize(description)

    # array fila 1 x title columntas fila 2 x description columnas
    seqs = [[None] * len(title), [None] * len(description)]

    for i, sentences in enumerate([title, description]):
        for idx, ss in enumerate(sentences):
            words = ss.strip().lower().split()
            # recorre las palabras si se encuentra en el diccionario asigna lo que vale la palabra
            seqs[i][idx] = [dictionary[w] if w in dictionary else 0 for w in words]
            if len(seqs[i][idx]) == 0:
                print 'len 0: ', i, idx

    return seqs[0], seqs[1]

def main():
    # sys.argv[1] = repo  = 'apache.csv'
    # load pretrain text:
    pretrain_path = sys.argv[1] + '_pretrain.csv'
    # del archivo lee las columnas title y description
    pre_title, pre_descr = load_raw_text.load_pretrain(pretrain_path)
    print 'number of datapoints:', len(pre_title)
    print "after building dict..."
    # train 2/3 del total
    n_train = len(pre_title) * 2 // 3
    # arange(n) = [0 , 1 ,2 .. n]
    ids = numpy.arange(len(pre_title))
    # mescla el array
    numpy.random.shuffle(ids)
    # divide los ids en 2 array train y test
    train_ids = ids[:n_train]
    valid_ids = ids[n_train:]
    # junta las columnas de title y description dividido para los ids mesclados titulos arriba ydescripciones abajo
    train = numpy.concatenate([pre_title[train_ids], pre_descr[train_ids]])
    valid = numpy.concatenate([pre_title[valid_ids], pre_descr[valid_ids]])
    
    # crea un diccionario de todo el repo de diferentes proyectos 'apache.csv' con solo train
    dictionary = build_dict(train)

    # cambia las palabras del repo por el valor del diccionario
    pre_train, pre_valid = grab_data(train, valid, dictionary)
    f_pre = gzip.open(sys.argv[1] + '_pretrain.pkl.gz', 'wb')
    pkl.dump((pre_train, pre_valid, pre_valid), f_pre, -1)
    f_pre.close()

    f = gzip.open(sys.argv[1] + '.dict.pkl.gz', 'wb')
    pkl.dump(dictionary, f, -1)
    f.close()


if __name__ == '__main__':
    main()