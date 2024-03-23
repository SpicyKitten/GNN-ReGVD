#!/home/avilash/anaconda3/envs/set-clang/bin/python
import fire
import json
import os
import sys

from pathlib import Path


def main(predictions_location, test_location, output_dir):
    """
    @param predictions_location: Path to a text file that has index-prediction mapping
    @param test_location: Path to a file that has index and other info about each test file
    @param output_dir: Path to a folder where output files will be written
    """
    positives = {}
    counts = {
        "true_positives": 0,
        "true_negatives": 0,
        "false_positives": 0,
        "false_negatives": 0
    }
    true_positives = []
    with open(test_location) as test_file:
        for line in test_file:
            contents = json.loads(line)
            index = contents["idx"]
            if contents["target"] == 1:
                positives[index] = contents
    with open(predictions_location) as predictions_file:
        for line in predictions_file:
            index, prediction = map(int, line.split('\t'))
            if prediction == 1 and index in positives:
                counts["true_positives"] += 1
                true_positives.append(positives[index])
            elif prediction == 1:
                counts["false_positives"] += 1
            elif index in positives:
                counts["false_negatives"] += 1
            else:
                counts["true_negatives"] += 1
    for count_type, count in counts.items():
        print(f"{count} {count_type.replace('_', ' ')}")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    # attributes are: project, commit_id, target, func, idx
    for true_positive in true_positives:
        output_filepath = os.path.join(output_dir, f"{true_positive['idx']}.c")
        with open(output_filepath, 'w') as output_file:
            output_file.write(true_positive["func"])
        print(true_positive["idx"])

    print(len(true_positives))


if __name__ == "__main__":
    try:
        fire.Fire(main)
    except fire.core.FireExit:
        print("Common error: not using flags to specify arguments (positional arguments disallowed)")
        print("Common error: not using quotations around input arguments")
        raise
