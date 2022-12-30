# AnyoneAI Cohort Full-Time #AY22-03
# Final Project Team 6: Automated product categorization for e-commerce

**Team Leader:** Erika Ortiz<br> 
**Team Members:**<br> 
Giannina Fernandez<br> 
Ignacio Martinez Lombardero<br> 
Julián Arango<br> 


## Description 
In this project we developed and API service that is backed by an NLP model that will classify the textual elements of a product record (description, summary etc). 

As an extra feature, our API is also backed by an image model

Meanwhile textual data input - the name of the product and its description - is mandatory the user optionally can upload an image of the product.   

<img src="https://user-images.githubusercontent.com/103912003/210112307-54f897eb-cf8c-4ead-a9f1-83716e0c5384.png" width="400" />

## Run the API
You can run the API by running the following command from the root directory of the project:

```bash
docker compose up --build
```

The application will be accesible then from 'localhost' in the browser.

## 1. API Structure 

The API is based in three micro services mounted using Docker. The one in the middle: the message broker, handles all the requests made from the web service end and the ML service, managing the jobs queue and the hash table that stores every result to be retrieved after making a prediction:

- 1. Web service: designed with HTML, CSS, JS and Flask.
- 2. Message broker: based on Redis.
- 3. ML service: uses pretrained models.


## 2. Dataset and EDA 

The dataset that was used can be found in the `data` folder with the name `products.json`.

The EDA is located in the `EDA` folder. There are differents EDA in each one we explore different aspects of the dataset.

## 3. Preprocessing and Feature Extraction 
### 3.1. Text Data
### 3.1. Image Data
To Download the Images we can excute

```bash
$ python3 scripts/Download_data.py
```
We analyze the content of the URL  that corresponds to the images in the notebook **Images_analysis** that is inside the EDA folder. 

## 4. Modelling

In the `model/training` folder you will find the `integration_pd_build_and_make_tree.ipynb`. Here we integrate different functions devised mainly to generate the dataset to be used for training (but also in evaluation). In this folder, you can also find three folders containing notebooks relative to models trained during the development of this project. 

The training folder is divided into three folders according to the kind of model


### 4.1. NLP Models

Here you will find all the notebooks dedicated to train different NLP models. You can start with the `NB0_data_set_prep_and_training.ipynb`. In it, you will find instructions and examples about how to generate the dataset, preprocess the data, train and evaluate your models.

### 4.2. Computer Vision Model
For the **baseline_model** that can be found in the followings folders: model_training/CV_models we use the data in data/data_baseline that we can obtain runing the following commands
```bash
$ python3 scripts/prepare_train_test_baseline.py data_img data/prod_dataset_labels.csv data_splitted
```
For the next model we used an EfficientNet model pretrained with ImageNet to have the data in the folders we need we have to execute:
```bash
$ python3 scripts/prepare_train_test_dataset.py data_img data/prod_dataset_labels.csv data_splitted
```
and to have the weights we can execute

```bash
$ python3 scripts/train.py experiments/exp3/exp3.yml
```

and after we have it we can run the **Model Evaluation_img.ipynb** that can be found in the model evaluation folder

### 4.3. Ensembled Model

`model/training/ensembled` is the folder where you can see the model that generates the predictions for our API. 
The design of this model, first evaluations, and predictions are all displayed in the `ensembled_model_I.ipynb`

This model ensembles one NLP model trained on the name of products to be classified, another trained on descriptions of the product, and finally, a computer vision model trained on the image of the products

## 5. Model Evaluation

In `model_evaluation` you can find an evaluation of the ensembled model that backed our API. This is evaluation is based on the prediction on test set given by our model and focuses on the model resulting from the ensemble of the NLP's models. 

<img src="https://user-images.githubusercontent.com/103912003/210112747-b033e270-1309-44ee-b5d0-41460c68df58.png" width="400" />

The evaluation is carried out in the ensemble_model_II.ipynb notebook

## 6. Improvement Proposals
Finally, you can find a list of possible improvements for the API, model, preprocessing, and other aspects relative to the project we developed 

Thank you for read! 


