from pathlib import Path
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, Activation
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.callbacks import EarlyStopping
from PIL import Image
import numpy as np
from cognicarebe.settings import BASE_DIR
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
import tensorflow as tf
from tensorflow.python.client import device_lib
from tensorflow.keras.optimizers import Adam
import cv2

def train_model():
    # data_dir = BASE_DIR / 'datasetImg/train'
    # epochs = 25
    # base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(48, 48, 3))
    # x = base_model.output
    # x = GlobalAveragePooling2D()(x)
    # x = Dense(1024, activation='relu')(x)
    # predictions = Dense(7, activation='softmax')(x)
    # model = Model(inputs=base_model.input, outputs=predictions)
    # base_model.trainable = False
    # model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    # datagen = ImageDataGenerator(
    #     rescale=1./255,
    #     validation_split=0.2,
    #     horizontal_flip=True,
    #     zoom_range=0.2
    # )
    # train_generator = datagen.flow_from_directory(
    #     str(data_dir),
    #     target_size=(48, 48),
    #     batch_size=64,
    #     class_mode='categorical',
    #     subset='training'
    # )
    # val_generator = datagen.flow_from_directory(
    #     str(data_dir),
    #     target_size=(48, 48),
    #     batch_size=64,
    #     class_mode='categorical',
    #     subset='validation'
    # )
    # early_stopping = EarlyStopping(monitor='val_loss', patience=10)
    # model.fit(train_generator, epochs=epochs, validation_data=val_generator, callbacks=[early_stopping])
    # model.save('emotion_model.h5')

    data_dir = BASE_DIR / 'datasetImg/train'
    epochs = 25
    batch_size = 64

    # Load the MobileNetV2 model with pre-trained weights, excluding the top layer
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(48, 48, 3))

    # Add a global spatial average pooling layer
    x = base_model.output
    x = GlobalAveragePooling2D()(x)

    # Add a fully-connected layer
    x = Dense(1024, activation='relu')(x)

    # Add a logistic layer with 7 neurons (for 7 emotions)
    predictions = Dense(7, activation='softmax')(x)

    # Create the model
    model = Model(inputs=base_model.input, outputs=predictions)

    # Freeze the base model
    base_model.trainable = False

    # Compile the model
    optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    # Data preparation
    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        vertical_flip=False
    )

    train_generator = datagen.flow_from_directory(
        str(data_dir),
        target_size=(48, 48),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    val_generator = datagen.flow_from_directory(
        str(data_dir),
        target_size=(48, 48),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    # Train the model
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    history = model.fit(train_generator, epochs=epochs, validation_data=val_generator, callbacks=[early_stopping])

    # Save the model
    model.save('emotion_model2.h5')

def detect_faces(image):
    face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray, 1.3, 5)
    return faces

def predict_emotion(image_path):

    # train_model()
    model = load_model('fer2013_mini_XCEPTION.102-0.66.hdf5')
    # data_dir = BASE_DIR / 'datasetImg/test'

    # img = Image.open(image_path).convert('RGB').resize((48, 48))
    # img = img_to_array(img)
    # img = img / 255.0
    # img = np.expand_dims(img, axis=0)

    # prediction = model.predict(img)
    # emotion = np.argmax(prediction)

    # emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    # print(emotion_labels[emotion])
    # return emotion_labels[emotion]

    img = cv2.imread(str(image_path))
    
    
    # Detect faces
    faces = detect_faces(img)
    
    # Process each detected face
    for (x, y, w, h) in faces:
        face_img = img[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (64, 64))
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        face_img = np.expand_dims(face_img, axis=0)
        face_img = np.expand_dims(face_img, axis=-1)
        face_img = face_img / 255.0
        
        # Predict emotion
        prediction = model.predict(face_img)
        emotion = np.argmax(prediction)
        
        emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        print(emotion_labels[emotion])
        return emotion_labels[emotion]

