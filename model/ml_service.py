import json
import os
import time
import redis
from joblib import load
import combined_model_class
import settings
from scripts import efficientnet
import yaml
from text_normalizer import Normalizer

os.chdir("/src/")
# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)

####### NLP MODELS #######

# loading pretrained models
model_title = load("name.joblib")
model_title_desc = load("description.joblib")

####### IMAGE MODEL #######

WEIGHTS = "model.06-2.0593.h5"
image_model = efficientnet.create_model(weights=WEIGHTS)

####### PUTTING THE MODELS TOGETHER ########


def predict(name, description, image_name):
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
    class_name, dict
    """
    # TODO
    final_model = combined_model_class.Combined_Model()

    name_desc = name + description

    if image_name != "no_image":
        IMAGE = settings.UPLOAD_FOLDER
        labels = final_model.predict_best_five(
            X_list=[name, name_desc, IMAGE],
            estimators=[model_title, model_title_desc, image_model],
            max_k_feat=5,
        )
    else:
        labels = final_model.predict_best_five(
            X_list=[name, name_desc],
            estimators=[model_title, model_title_desc],
            max_k_feat=5,
        )

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
        #         "prediction": dict,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        # TODO
        _, msg = db.brpop(settings.REDIS_QUEUE)
        job_data = json.loads(msg)
        name = job_data["name"]
        description = job_data["description"]
        image_name = job_data["image_name"]
        job_id = job_data["id"]
        pred_cat = predict(name, description, image_name)

        db.set(job_id, json.dumps(pred_cat))

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
