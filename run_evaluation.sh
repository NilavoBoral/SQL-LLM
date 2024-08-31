# # Have to match

# Databases path: f"./data/dev_databases/{db_name}/{db_name}.sqlite"
# Sample data path: "./data/dev_sample.json"

# Original SQL path: "./data/dev_gold.sql"
# Predicted SQL path: "./predicted/predict_dev.json"


db_root_path='./data/dev_databases/'
ground_truth_path='./data/'
predicted_sql_path='./predicted/'
data_mode='dev'
diff_json_path='./data/dev_sample.json' # sample data path (using for only extract difficulty)
num_cpus=16
meta_time_out=30.0
mode_gt='gt'
mode_predict='gpt'


echo '''\nstarting to compare for Execution Accuracy (EX)'''
python3 -u ./text_to_sql/evaluation.py --db_root_path ${db_root_path} --predicted_sql_path ${predicted_sql_path} --data_mode ${data_mode} \
--ground_truth_path ${ground_truth_path} --num_cpus ${num_cpus} --mode_gt ${mode_gt} --mode_predict ${mode_predict} \
--diff_json_path ${diff_json_path} --meta_time_out ${meta_time_out}

echo '''\nstarting to compare for Valid Efficiency Score (VES)'''
python3 -u ./text_to_sql/evaluation_ves.py --db_root_path ${db_root_path} --predicted_sql_path ${predicted_sql_path} --data_mode ${data_mode} \
--ground_truth_path ${ground_truth_path} --num_cpus ${num_cpus} --mode_gt ${mode_gt} --mode_predict ${mode_predict} \
--diff_json_path ${diff_json_path} --meta_time_out ${meta_time_out}
