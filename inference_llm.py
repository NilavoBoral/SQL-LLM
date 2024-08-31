import random
from text_to_sql.sqllm import load_llm, sql_llm
from text_to_sql.helper import load_json, print_progress_bar, save_list_as_json, save_list_as_sql



pipeline = load_llm(
    model_id="/home/ubuntu/AI-experiments/LLMs/Meta-Llama-3.1-8B-Instruct", # Path to the downloaded LLM
    optimize='4-bit', 
    device='auto'
)

# Load JSON content
json_content = load_json("data/dev.json")

# Sample data
num_sample = 30
sample_json_content = random.sample(json_content, num_sample)

# Initialize lists to store SQL queries
sample_data_list, gt_sql_list, pred_sql_dict = [], [], {}
# Generate and store SQL queries
print()
for i in range(num_sample):
    data = sample_json_content[i]
    sample_data_list.append(data)

    db_id = data["db_id"]

    gt_sql = data["SQL"]
    gt_sql_list.append(f"{gt_sql}\t{db_id}")

    pred_sql, _ = sql_llm(
        pipe=pipeline,
        db=f"data/dev_databases/{db_id}/{db_id}.sqlite", 
        question=data["question"], 
        max_try=3,
        domain_knowledge=data["evidence"]
    )
    pred_sql_dict[i] = f"{pred_sql}\t----- bird -----\t{db_id}"

    # Update progress bar
    print_progress_bar(i + 1, num_sample)

print("\n")

# Save lists to files
save_list_as_json("./data/dev_sample.json", sample_data_list)
save_list_as_json("./predicted/predict_dev.json", pred_sql_dict)
save_list_as_sql("./data/dev_gold.sql", gt_sql_list)
