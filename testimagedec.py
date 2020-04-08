from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pylab as plt

import tensorflow as tf
import tensorflow_hub as hub

from tensorflow.keras import layers

import multiprocessing
import numpy as np
import PIL.Image as Image
import cv2 


def apiim( im, return_dictim):
    IMAGE_SHAPE = (224, 224)
    image = np.array(im)/255.0

    classifier_url = "https://tfhub.dev/google/tf2-preview/inception_v3/classification/4"
    classifier = tf.keras.Sequential([
        hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE+(3,))
    ])

    result = classifier.predict(image[np.newaxis, ...])
    predicted_class = np.argmax(result[0], axis=-1)

    labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
    imagenet_labels = np.array(open(labels_path).read().splitlines())

    #cv2.imshow("ada",image)

    predicted_class_name = imagenet_labels[predicted_class]
    _ = plt.title("Prediction: " + predicted_class_name.title())
    print(_)

    print(result.shape)
    print(predicted_class)
    key = cv2.waitKey(0)

    return_dictim["im"] = str(predicted_class_name.title())
    im.save("test_img\\"+str(predicted_class_name.title()) + '.png', "PNG")
    return return_dictim


def multiprocim(im):
    managerim = multiprocessing.Manager()
    return_dictim = managerim.dict()

    p = multiprocessing.Process(target=apiim, args=(im, return_dictim))
    p.start()
    p.join()

    return return_dictim.values()[0]


if __name__ == "__main__":
    out = multiprocim(pass)
    print(out)
