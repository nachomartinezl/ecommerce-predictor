import json
import time
from uuid import uuid4
import redis
import settings

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host = settings.REDIS_IP, 
    port = settings.REDIS_PORT, 
    db = settings.REDIS_DB_ID
)

def model_predict(name, description, image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.
    
    name : str
        Title for the product uploaded by the user.
    
    description : str
        Description for the product uploaded by the user.

    Returns
    -------
    prediction : dict
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
  
    # Assign an unique ID for this job and add it to the queue.
    # We need to assing this ID because we must be able to keep track
    # of this particular job across all the services
    # TODO
    job_id = str(uuid4())

    job_data = {
        "id" : job_id,
        "name" : name,
        "description" : description,
        "image_name": image_name
    }
   
    # Send the job to the model service using Redis
    # Hint: Using Redis `lpush()` function should be enough to accomplish this.
    # TODO
    db.lpush(
        settings.REDIS_QUEUE,
        json.dumps(job_data)
    )

    # Loop until we received the response from our ML model
    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis
        # TODO
        output = db.get(job_id)
        if output is not None:
            results = json.loads(output)
            prediction = results
            db.delete(job_id)
            return prediction
        else:
            time.sleep(settings.API_SLEEP)