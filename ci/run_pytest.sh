#!/bin/bash
PWD=$(cd "$(dirname "$0")" || exit 1; pwd)
ROOT_PATH="${PWD%ci*}"
echo "ROOT_PATH=$ROOT_PATH"

#-----------------------------------------------------------------------------------------------------------------------
CI_CASES_REGEX="$1"
echo "CI_CASES_REGEX=${CI_CASES_REGEX}"

cd $ROOT_PATH
ls -ls

if [[ ".py" =~ "${CI_CASES_REGEX}" ]];then
    echo "pytest ${CI_CASES_REGEX}"
    pytest ${CI_CASES_REGEX}
else
    echo "pytest ${CI_CASES_REGEX}/*.py"
    pytest ${CI_CASES_REGEX}/*.py
fi
