#!/bin/bash
poetry install
poetry run p1204_3 --result_folder test_videos/reports_new \
    --tmp test_videos/parsed \
    test_videos/*.mkv


function report_diff() {
    # ignore the "date" field in the reports
    python <<HEREDOC
import json
with open("$1") as fp:
    r1 = json.load(fp)
with open("$2") as fp:
    r2 = json.load(fp)
dc = 0
for k in set(r1.keys() + r2.keys()) - set(["date"]):
    if k in r1 and k in r2:
        if r1[k] != r2[k]:
            dc +=1
    else:
        dc += 1
print(dc)
HEREDOC
}

for new_report in test_videos/reports_new/*; do
    echo "$new_report"
    ref_report=$(echo "$new_report"|sed "s|reports_new|reports|g")
    rdiff=$(report_diff "$new_report" "$ref_report")
    if [[ "$rdiff" != "0" ]]; then
        echo "differente in "$ref_report" and "$new_report""
        diff "$ref_report" "$new_report"  | grep -v "date"
    fi
done
