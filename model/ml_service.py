import json
import os
import time
import numpy as np
import redis
import settings
from joblib import load

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)

# TODO

# image_model = ResNet50(include_top=True, weights="imagenet")
# name_model = load('tfidf_gbc_names.joblib')
# desc_model = load("tfidf_gbc_desc.joblib")

#name_model = load("logreg.joblib")



def predict(image_name, name, description):
    """
    Load image, name from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Load name and description as tex, and run the ML model to get predictions.

    Fusion outputs of three model to return an unique list of predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    name: str
        Text for product title.

    description: str
        Text for product description.


    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted classes as strings and the corresponding confidence
        score as a number.
    """
    # TODO

    # img = image.load_img(os.path.join(settings.UPLOAD_FOLDER, image_name), target_size=(224, 224))
    # x = image.img_to_array(img)
    # x_batch = np.expand_dims(x, axis=0)
    # x_batch = preprocess_input(x_batch)
    # preds_1 = image_model.predict(x_batch)
    # label = decode_predictions(preds, top=1)
    # class_name = label[0][0][1]
    # pred_probability = float(label[0][0][2])

    #preds_name = name_model.predict(name)
    #label_name = preds_name[0]

    #preds_desc = name_model.predict(description)
    #label_desc = preds_desc[0]

    #classes = label_name, label_desc

    labels = ['Root > Parent > Children > Children', 
              'Root > Parent > Children > Children',
              'Root > Parent > Children > Children']

    return labels


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        #   2. Run your ML model on the given data
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        # TODO
        msg = db.brpop(settings.REDIS_QUEUE)
        if msg is not None:
            job_data = json.loads(msg[1])
            prediction = predict(
                job_data["image_name"], job_data["name"], job_data["description"]
            )
            output = {"prediction": prediction}
            db.set(job_data["id"], json.dumps(output))
        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()