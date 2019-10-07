#!/usr/bin/env bash

word2vec_binary_location="/home/fvillena/word2vec/word2vec"
corpus_location="/home/fvillena/code/multilingual-medical-nlp/data/processed/merged/$1.merged"
embedding_file="/home/fvillena/code/multilingual-medical-nlp/models/$1.vec"
threads=4

$word2vec_binary_location -train $corpus_location -output $embedding_file -debug 2 -cbow 0 -size 300 -threads $threads -binary 0