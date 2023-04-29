import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import json


def analyseMainFrames(imageList):
    analyzedData = {}
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    LABELS = ["stance", "leg-movement"]
    STANCE_LABELS = ["close", "top"]
    LM_LABELS = ["fine", "back-leg-bent"]
   
    # Load the modelupright
    #modelLegMovement = tensorflow.keras.models.load_model("/Users/ravindufernando/Desktop/A-1/timetrial/keras_model.h5")
    modelStance = tensorflow.keras.models.load_model("/Users/ravindufernando/Desktop/A-1/upright/keras_model.h5")
    modelLegMovement = tensorflow.keras.models.load_model("/Users/ravindufernando/Desktop/A-1/timetrial/keras_model.h5")
   # modelLegMovement = tensorflow.keras.models.load_model("/Users/ravindufernando/Desktop/A-1/timetrial/keras_model.h5")
 

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    for label in LABELS:
        # Replace this with the path to your image
        image = Image.open(imageList[label])

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        # image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        if label == 'stance':
            print("STANCE ANALYSIS")
            prediction = modelStance.predict(data)
            print(prediction)
            idxs = prediction.argmax(axis=-1)
            for (i, j) in enumerate(idxs):
                print(STANCE_LABELS[j])
                analyzedData["stance"] = STANCE_LABELS[j]
        if label == 'leg-movement':
            print("LM ANALYSIS")
            prediction = modelLegMovement.predict(data)
            print(prediction)
            idxs = prediction.argmax(axis=-1)
            for (i, j) in enumerate(idxs):
                print(LM_LABELS[j])
                analyzedData["leg-movement"] = LM_LABELS[j]
        
    json_data = json.dumps(analyzedData)
    return json_data
