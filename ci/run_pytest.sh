#!/bin/bash
PWD=$(cd "$(dirname "$0")" || exit 1; pwd)
ROOT_PATH="${PWD%ci*}"
echo "ROOT_PATH=$ROOT_PATH"

#-----------------------------------------------------------------------------------------------------------------------
CI_CASES_REGEX="$1"
CI_TEST_REPORT_PATH="$2"
echo "CI_CASES_REGEX=${CI_CASES_REGEX}"
echo "CI_TEST_REPORT_PATH=${CI_TEST_REPORT_PATH}"

if [[ ".py" =~ "${CI_CASES_REGEX}" ]];then
    echo pytest ${CI_CASES_REGEX} --alluredir=${CI_TEST_REPORT_PATH}
    pytest ${CI_CASES_REGEX} --alluredir=${CI_TEST_REPORT_PATH}
else
    echo pytest ${CI_CASES_REGEX}/*.py --alluredir=${CI_TEST_REPORT_PATH}
    pytest ${CI_CASES_REGEX}/*.py --alluredir=${CI_TEST_REPORT_PATH}
fi
