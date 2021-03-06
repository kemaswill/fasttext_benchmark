'''This example demonstrates the use of fasttext for text classification, we test it over several datasets using different parameters to get a deeper insight into it.

Based on Joulin et al's paper:

Bags of Tricks for Efficient Text Classification
https://arxiv.org/abs/1607.01759

'''

from __future__ import print_function
import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Embedding
from keras.layers import AveragePooling1D
from keras.datasets import imdb
from util import util
from keras.utils.np_utils import to_categorical

np.random.seed(1337)  # for reproducibility

# set parameters:
max_features = 20000
maxlen = 400
batch_size = 32
embedding_dims = 20
nb_epoch = 5

path_train = "data/ag_news_csv/train.csv"
path_test = "data/ag_news_csv/test.csv"

print('Loading data...')
data_util = util()
data_util.build_vocab(path_train, max_features)
X_train, y_train, X_train_raw = data_util.vectorize(path_train)
X_test, y_test, X_test_raw = data_util.vectorize(path_test)

print(X_train[:10])
print(X_test[:10])
print(X_train_raw[:10])

print("y_train", y_train[:10])

print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')

print('Pad sequences (samples x time)')
X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)

print('Build model...')
model = Sequential()

# we start off with an efficient embedding layer which maps
# our vocab indices into embedding_dims dimensions
model.add(Embedding(max_features,
                    embedding_dims,
                    input_length=maxlen))

# we add a AveragePooling1D, which will average the embeddings
# of all words in the document
model.add(AveragePooling1D(pool_length=model.output_shape[1]))

# We flatten the output of the AveragePooling1D layer
model.add(Flatten())

# We project onto a single unit output layer, and squash it with a sigmoid:
model.add(Dense(5, activation='sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X_train, y_train,
          batch_size=batch_size,
          nb_epoch=nb_epoch,
          validation_data=(X_test, y_test))
