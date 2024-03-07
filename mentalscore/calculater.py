import os
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

def preprocess(file):
    path = os.getcwd()+file+'.txt'
    data = pd.read_csv(path, sep = ';')
    hos = []
    for i in range(len(data.emotion)):
        if data['emotion'][i] in ['joy', 'love', 'surprise']:
            hos.append(1) # happy is 1
        else:
            hos.append(0) # sad is 0
    data['hos'] = hos
    return data

def postprocessor(preds,predstr):
  range = predstr.max()-predstr.min()
  norm_preds = []
  probab = []
  for i in preds:
    norm_preds.append((i - predstr.min()) / range)
    probab.append((i - predstr.min()) * 100 / range)
  return np.mean(probab)


def calculater(answers):

    print(answers)
    
    train_data = preprocess('\\mentalscore\\train')
    train = train_data.copy()

    model = "https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1"
    hub_layer = hub.KerasLayer(model, output_shape=[20], input_shape=[], 
                            dtype=tf.string, trainable=True)

    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(1))


    model.compile(optimizer='adam',
                loss=tf.losses.BinaryCrossentropy(from_logits=True),
                metrics=[tf.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])

    val = preprocess('\\mentalscore\\val')

    history = model.fit(train.text,
                        train.hos,
                        epochs=40,
                        batch_size=512,
                        validation_data=(val.text, val.hos),
                        verbose = 0)


    predstr = model.predict(train.text)

    results = model.predict(answers)
    score = postprocessor(results,predstr)
    print('Your mental health score is:', score)

    if score < 25:
        print("You are going through a bad phase in life. But don't worry, bad times are not permanent. Try to seek help from a trained professional to improve your mental health.")
    else:
        print("Your mental health looks great! Continue enjoying life and try to help others who are struggling with their mental health.")

    return score
