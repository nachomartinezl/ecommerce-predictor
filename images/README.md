## Steps to Image modeling

1)	Downloading the data using Download_data.py (approx. 1 Hour). In the data folder

```bash
$ /usr/bin/python3 /home/gianniif/ecommerce-predictor/Download_data.py
```

2)	Create the csv to split train and test. Running the creating_csv.ipynb notebook (approx. +1 Hour) or using the one that is already created that it is with a 100 threslhod

3) Run docker

4)	Split the data in train an test

```bash
$ python3 scripts/prepare_train_test_dataset.py data prod_dataset_labels.csv data_splitted
```

    if an error appears  ->    pip install protobuf==3.20.*

5)	Run the  model

```bash
$ python3 scripts/train.py experiments/exp3/exp3.yml
```

6)	Open tensorboard

7)	Check in Model Evaluation Notebook - Has Bugs

Notes: to create the train/test folder for the baseline model use scripts/prepare_train_test2.py

Folders looks like:
![image](https://user-images.githubusercontent.com/107515696/207886116-14b61f03-61b5-4c94-94ae-72fb347ab374.png)
