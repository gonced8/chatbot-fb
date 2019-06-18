#!/bin/bash

mkdir -p ./vocab
cd vocab

directory="$(pwd)"
source_file="$(echo ../messages_processed/*_goncaloraposo_E.txt)"
target_file="$(echo ../messages_processed/*_goncaloraposo_D.txt)"
model_name="m"
vocab_size="10000"
model_type="unigram"
vocab="vocab.txt"
source_file_vocab="source.txt"
target_file_vocab="target.txt"


#cat "$source_file" "$target_file" > "$joined"

# Sentence piece
spm_train --input="$source_file","$target_file" --model_prefix="$model_name" --vocab_size="$vocab_size" --character_coverage=1.0 --model_type="$model_type"

# Get vocab
onmt-build-vocab --save_vocab "$vocab" --from_vocab "${model_name}.vocab" --from_format sentencepiece

# Apply vocab to source and target file
spm_encode --model="${model_name}.model" --output_format=piece < "$source_file" > "$source_file_vocab"
spm_encode --model="${model_name}.model" --output_format=id < "$target_file" > "$target_file_vocab"

cd ..
