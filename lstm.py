#!/usr/bin/python
import keras
from keras.models import load_model
import numpy as np
from random import choice, randint
import json

#metamorphosis, shakespear , gutenberg, darwin
source = 'darwin'
model = load_model('models/' + source + '.h5')
text = open('source_text/'  + source + '.txt').read().lower()
maxlen = 40
chars = sorted(list(set(text)))
char_indices = dict((c,i) for i, c in enumerate(chars))
indices_char = dict((i,c) for i,c in enumerate(chars))

# helper function to sample an index from a probability array
def sample(preds, temperature=0.5):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)
    
# Generate LSTM text
def lstmText(classification):
    seeds = []

    for element in classification:
        element = " ".join(element[1].split("_"))
        seeds.append(element)

    sentence = seeds[0]

    while len(sentence) < maxlen:
        sentence += sentence
    if len(sentence) > maxlen:
        sentence = sentence[:maxlen]

    temperature = float(0.3)
    length = int(100)
    generated = ''

    for i in range(length):
        x = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x[0, t, char_indices[char]] = 1.
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, temperature)
        next_char = indices_char[next_index]
        generated += next_char
        sentence = sentence[1:] + next_char
    return "the " + seeds[0] + generated;
