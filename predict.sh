source="translate/test.txt"
source_pieces="translate/src-test.txt"
target_pieces="translate/trg-test.txt"
target="translate/result.txt"

model_file="vocab/m.model"
model_data="model/data.yml"


spm_encode --model="$model_file" --output_format=piece < "$source" > "$source_pieces"

onmt-main infer --auto_config --config "$model_data" --features_file "$source_pieces" --predictions_file "$target_pieces"

spm_decode --model="$model_file" --input_format=piece < "$target_pieces" > "$target"
