#!/bin/bash
CI_CASES_REGEX="$1"
echo "CI_CASES_REGEX=${CI_CASES_REGEX}"

pwd
ls -l

echo "pytest ${CI_CASES_REGEX} --capture=no --clean-alluredir --alluredir=./test_report"
pytest ${CI_CASES_REGEX} --capture=no --clean-alluredir --alluredir=./test_report

ls -l ${CI_TEST_REPORT_PATH}
