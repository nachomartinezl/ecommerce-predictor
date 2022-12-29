# Automated product categorization for e-commerce

## Description 
API service that is backed by an NLP model that will classify the textual elements of a product record (description, summary etc). 

As an extra feature, our API is also backed by an image model

Meanwhile textual data input - the name of the product and its description - is mandatory the user optionally can upload an image of the product.   

## 1. API Structure 
## 2. Dataset and EDA 
## 3. Preprocessing and Feature Extraction 
### 3.1. Text Data
### 3.1. Image Data
We analyze the content of the URL  that corresponds to the images in the notebook **Images_analysis** that is inside the EDA folder. 
## 4. Modelling
### 4.1. NLP Models
### 4.2. Computer Vision Model
For the **baseline_model** that can be found in the followings folders: model_training/CV_models we use the data in data/data_baseline that we can obtain runing the following commands
```bash
$ python3 scripts/prepare_train_test_baseline.py data_img data/prod_dataset_labels.csv data_splitted
```

### 4.3. Ensembled Model
Base models to ensemble NLP name and NLP name + descriptions and image model
**Notebook ensembled model I**  - Here we explore different combinations of models based on different weights. Here we saved the different models 
**Notebook ensembled model II** ensembled model selected in the previous notebook and that will be backed our API. 

## 5. Model Evaluation

## 6. Improvement Proposals
