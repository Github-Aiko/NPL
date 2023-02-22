from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import random


# Load the data
path = keras.utils.get_file(
    "shakespeare.txt", origin="https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt"
)
with open(path) as f:
    text = f.read().lower()

# Preprocess the data
chars = sorted(set(text))
char_to_index = dict(zip(chars, range(len(chars))))
index_to_char = dict(zip(range(len(chars)), chars))
max_sequence_length = 100
step = 5
sentences = []
next_chars = []
for i in range(0, len(text) - max_sequence_length, step):
    sentences.append(text[i : i + max_sequence_length])
    next_chars.append(text[i + max_sequence_length])
x = np.zeros((len(sentences), max_sequence_length, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_to_index[char]] = 1
    y[i, char_to_index[next_chars[i]]] = 1

# Build the model
model = keras.Sequential(
    [
        layers.LSTM(128, input_shape=(max_sequence_length, len(chars))),
        layers.Dense(len(chars), activation="softmax"),
    ]
)
optimizer = keras.optimizers.RMSprop(learning_rate=0.01)
model.compile(loss="categorical_crossentropy", optimizer=optimizer)

# Train the model
model.fit(x, y, batch_size=128, epochs=5)


# Generate new text
start_index = random.randint(0, len(text) - max_sequence_length - 1)
generated_text = text[start_index : start_index + max_sequence_length]
for i in range(400):
    x_pred = np.zeros((1, max_sequence_length, len(chars)))
    for t, char in enumerate(generated_text):
        x_pred[0, t, char_to_index[char]] = 1
    preds = model.predict(x_pred, verbose=0)[0]
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / 0.5
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    next_index = np.random.choice(len(preds), p=preds)
    next_char = index_to_char[next_index]
    generated_text += next_char
    generated_text = generated_text[1:]



with open('generated_text.txt', 'w', encoding='utf-8') as f:
	f.write(generated_text)