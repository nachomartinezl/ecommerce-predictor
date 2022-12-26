"""
This script will be used to separate and copy images coming from
`car_ims.tgz` (extract the .tgz content first) between `train` and `test`
folders according to the column `subset` from `car_dataset_labels.csv`.
It will also create all the needed subfolders inside `train`/`test` in order
to copy each image to the folder corresponding to its class.

The resulting directory structure should look like this:
    data/
    ├── car_dataset_labels.csv
    ├── car_ims
    │   ├── 000001.jpg
    │   ├── 000002.jpg
    │   ├── ...
    ├── car_ims_v1
    │   ├── test
    │   │   ├── AM General Hummer SUV 2000
    │   │   │   ├── 000046.jpg
    │   │   │   ├── 000047.jpg
    │   │   │   ├── ...
    │   │   ├── Acura Integra Type R 2001
    │   │   │   ├── 000450.jpg
    │   │   │   ├── 000451.jpg
    │   │   │   ├── ...
    │   ├── train
    │   │   ├── AM General Hummer SUV 2000
    │   │   │   ├── 000001.jpg
    │   │   │   ├── 000002.jpg
    │   │   │   ├── ...
    │   │   ├── Acura Integra Type R 2001
    │   │   │   ├── 000405.jpg
    │   │   │   ├── 000406.jpg
    │   │   │   ├── ...
"""
import argparse
import pandas as pd
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument(
        "data_folder",
        type=str,
        help=(
            "Full path to the directory having all the cars images. E.g. "
            "`/home/app/src/data/car_ims/`."
        ),
    )
    parser.add_argument(
        "labels",
        type=str,
        help=(
            "Full path to the CSV file with data labels. E.g. "
            "`/home/gianniif/ecommerce-predictor/products_v1.csv`."
            
        ),
    )
    parser.add_argument(
        "output_data_folder",
        type=str,
        help=(
            "Full path to the directory in which we will store the resulting "
            "train/test splits. E.g. `/home/gianniif/ecommerce-predictor/data`."
        ),
    )

    args = parser.parse_args()

    return args


def main(data_folder, labels, output_data_folder):
    """
    Parameters
    ----------
    data_folder : str
        Full path to raw images folder.

    labels : str
        Full path to CSV file with data annotations.

    output_data_folder : str
        Full path to the directory in which we will store the resulting
        train/test splits.
    """
    # For this function, you must:
    #   1. Load labels CSV file
    labels_csv = pd.read_csv(labels)
    

    #   2. Iterate over each row in the CSV, create the corresponding
    #      train/test and class folders
    


    for row in labels_csv.itertuples():
        if row[3] == 'train':
            path_img = os.path.join(output_data_folder, row[2])
            os.makedirs(path_img, exist_ok = True)
        else:
            path_img = os.path.join(output_data_folder, row[2])
            os.makedirs(path_img, exist_ok = True)

   #     if os.path.join(data_folder, f'row{row[1]+1}.jpg') == f'data/row{row[1]+1}.gif':
#        convert row{row[1]+1}.gif[0] row{row[1]+1}.jpg

        
        raw_image = os.path.join(data_folder, f'{row[1]}')
        path_img = os.path.join(path_img, f'{row[1]}') 
        os.link(raw_image, path_img)   
    #   3. Copy the image to the new folder structure. We recommend you to
    #      use `os.link()` to avoid wasting disk space with duplicated files
    # TODO



if __name__ == "__main__":
    args = parse_args()
    main(args.data_folder, args.labels, args.output_data_folder)
