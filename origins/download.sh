#/bin/bash

curl -L -o 31Kmeta_en.zip\
  https://www.kaggle.com/api/v1/datasets/download/Cornell-University/arxiv
unzip 31Kmeta_en.zip -d ./31Kmeta_en
rm 31Kmeta_en.zip

curl -L -o 24Kmeta_en.zip\
  https://www.kaggle.com/api/v1/datasets/download/neelshah18/arxivdataset
unzip 24Kmeta_en.zip -d ./24Kmeta_en
rm 24Kmeta_en.zip
