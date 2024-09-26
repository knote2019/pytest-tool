#!/bin/bash
PWD=$(cd "$(dirname "$0")" || exit 1; pwd)
ROOT_PATH="${PWD%ci*}"
echo "ROOT_PATH=$ROOT_PATH"

#-----------------------------------------------------------------------------------------------------------------------
CI_CASES_REGEX="$1"
echo "CI_CASES_REGEX=${CI_CASES_REGEX}"

cd $ROOT_PATH
if [[ ".py" =~ "${CI_CASES_REGEX}" ]];then
    pytest "${CI_CASES_REGEX}"
else
    pytest "${CI_CASES_REGEX}/*.py" --junitxml=./iluvatar_test_report.xml
fi
