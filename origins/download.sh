#/bin/bash

curl -L -o 3Mmeta_en.zip\
  https://www.kaggle.com/api/v1/datasets/download/Cornell-University/arxiv
unzip 3Mmeta_en.zip -d ./3Mmeta_en
rm 3Mmeta_en.zip

curl -L -o 41Kmeta_en.zip\
  https://www.kaggle.com/api/v1/datasets/download/neelshah18/arxivdataset
unzip 24Kmeta_en.zip -d ./41Kmeta_en
rm 41Kmeta_en.zip
