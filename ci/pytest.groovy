@Library('jenkins_pipeline_shared_lib@master')_

// ---------------------------------------------------------------------------------------------------------------------
def CI_NODE_LABEL = params.CI_NODE_LABEL.trim()
def CI_COREX_PKG_URL = params.CI_COREX_PKG_URL.trim()
def CI_TESTAGENT = params.CI_TESTAGENT.trim()

def CI_CASES_REGEX = params.CI_CASES_REGEX.trim()

def CI_BRANCH = params.CI_BRANCH.trim()
def CI_KEEP_TESTAGENT = params.CI_KEEP_TESTAGENT.trim()
// ---------------------------------------------------------------------------------------------------------------------

def testagent_ssh_ip = ""
def testagent_ssh_port = ""

def exec_shell(shell_scripts) {
    def isFlowInterrupted = false
    catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') { try{ sh(script: "#!/bin/bash -e\n${shell_scripts}") } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) { isFlowInterrupted = true } }
    if(isFlowInterrupted){ error("build interrupted !!!") }
}

pipeline {
    agent { node { label CI_NODE_LABEL } }
    options {
        timestamps ()
        ansiColor('xterm')
    }
    stages {
        stage('install_ixdriver') {
            steps {
                script{
                    sh """
                    """
                    execute.db_record(CI_COREX_PKG_URL)
                }
            }
        }

        stage('run_test') {
            steps {
                script{
                    testagent_ssh_ip = sh(script: """hostname -I | awk -F ' ' '{print \$1}'""", returnStdout: true).trim()
                    testagent_ssh_port = sh(script: """shuf -i 10000-60000 -n1""", returnStdout: true).trim()
                    def dockerImage = docker.image("${CI_TESTAGENT}")
                    dockerImage.pull()
                    dockerImage.inside("-p ${testagent_ssh_port}:22 -v /dev:/dev -v /lib/modules:/lib/modules --privileged --shm-size 64g -v /stores:/stores") {
                        currentBuild.description = "${testagent_ssh_ip}:${testagent_ssh_port}"
                        exec_shell """
                            echo "install ${CI_COREX_PKG_URL}"
                        """
                        exec_shell """
                            cd ${env.WORKSPACE}/ci
                            bash run_pytest.sh "${CI_CASES_REGEX}" "${env.WORKSPACE}/test_report"
                        """
                        if(CI_KEEP_TESTAGENT.contains("true")) {sh """sleep infinity"""}
                    }
                }
            }
        }

        stage('generate_report') {
            steps {
                script{
                    allure([includeProperties: false, jdk: '', results: [[path: '${env.WORKSPACE}/test_report']]])
                }
            }
        }
    }
    post{
        always{
            script{
                exec_shell """dmesg -T > dmesg.log;"""
                archiveArtifacts(artifacts: 'dmesg.log', fingerprint: true)
                execute.db_record_update()
                driver.remove()
                cleanWs()
            }
        }
    }
}
