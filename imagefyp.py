from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pylab as plt

import tensorflow as tf
import tensorflow_hub as hub

from tensorflow.keras import layers

import numpy as np
import PIL.Image as Image
import cv2 


def pred():
    IMAGE_SHAPE = (224, 224)

    classifier_url = "https://tfhub.dev/google/tf2-preview/inception_v3/classification/4"
    classifier = tf.keras.Sequential([
        hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE+(3,))
    ])


    image = Image.open("wiskey.png").resize(IMAGE_SHAPE)
    image = image.convert("RGB")
    image = np.array(image)/255.0

    result = classifier.predict(image[np.newaxis, ...])
    predicted_class = np.argmax(result[0], axis=-1)


    labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
    imagenet_labels = np.array(open(labels_path).read().splitlines())

    predicted_class_name = imagenet_labels[predicted_class]

    _ = plt.title("Prediction: " + predicted_class_name.title())
    print(_)

    print(result.shape)
    print(predicted_class)
    """
    export_path = "saved_models"
    classifier.save(export_path, save_format='tf')
    reloaded = tf.keras.models.load_model(export_path)
    """

    key = cv2.waitKey(0)

    return predicted_class_name.title()

out = pred()
print(out)


