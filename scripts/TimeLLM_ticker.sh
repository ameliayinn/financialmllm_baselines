model_name=TimeLLM
train_epochs=10
learning_rate=0.01
llama_layers=32

#master_port=00097
master_port=8080
num_process=1
batch_size=12
d_model=16
d_ff=32

comment='TimeLLM-ticker'

accelerate launch --num_machines 1 --dynamo_backend 'no' --mixed_precision bf16 --num_processes $num_process --main_process_port $master_port run_main.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path dataset/ticker/ \
  --data_path data.csv \
  --model_id ticker_10_2 \
  --model $model_name \
  --data ticker \
  --features S \
  --target DlyNumTrd \
  --seq_len 10 \
  --label_len 5 \
  --pred_len 2 \
  --e_layers 2 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 6 \
  --dec_in 6 \
  --c_out 6 \
  --batch_size $batch_size \
  --learning_rate $learning_rate \
  --llm_layers $llama_layers \
  --train_epochs $train_epochs \
  --model_comment $comment