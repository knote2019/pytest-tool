#!/bin/bash
CI_CASES_REGEX="$1"
echo "CI_CASES_REGEX=${CI_CASES_REGEX}"
# show current folder.
pwd
ls -l
# run test.
echo "pytest ${CI_CASES_REGEX} --clean-alluredir --alluredir=./test_report"
pytest ${CI_CASES_REGEX} --clean-alluredir --alluredir=./test_report || echo "test failed"
