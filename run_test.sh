#!/bin/bash
CI_CASES_REGEX="$1"
CI_TEST_REPORT_PATH="$2"
echo "CI_CASES_REGEX=${CI_CASES_REGEX}"
echo "CI_TEST_REPORT_PATH=${CI_TEST_REPORT_PATH}"

pwd
ls -l
echo pytest ${CI_CASES_REGEX} --capture=no --clean-alluredir --alluredir=${CI_TEST_REPORT_PATH}
pytest ${CI_CASES_REGEX} --capture=no --clean-alluredir --alluredir=${CI_TEST_REPORT_PATH}

ls -l ${CI_TEST_REPORT_PATH}
