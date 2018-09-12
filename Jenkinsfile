/*
 * Required plugins:
 * Blue Ocean / all the 'typical' plugins for GitHub multi-branch pipelines
 * GitHub Branch Source Plugin
 * SCM Filter Branch PR Plugin
 * Pipeline GitHub Notify Step Plugin
 * Pipeline: GitHub Plugin
 * Kubernetes Plugin
 */

pyContainer = "python3"
podLabel = "tag-service-test-${UUID.randomUUID().toString()}"
gitEmail = "rhinsightsbot@gmail.com"
gitName = "InsightsDroid"

node {
    milestone()

    // trick to cancel previous builds, see https://issues.jenkins-ci.org/browse/JENKINS-40936
    // avoids quick PR updates triggering too many concurrent tests
    for (int i = 0; i < (env.BUILD_NUMBER as int); i++) {
        milestone()
    }

    stage ('Checkout') {
        scmVars = checkout scm
    }

    echo "env.CHANGE_ID:                  ${env.CHANGE_ID}"
    echo "env.BRANCH_NAME:                ${env.BRANCH_NAME}"
    echo "GIT_COMMIT:                     ${scmVars.GIT_COMMIT}"
    echo "GIT_PREVIOUS_SUCCESSFUL_COMMIT: ${scmVars.GIT_PREVIOUS_SUCCESSFUL_COMMIT}"
    echo "GIT_URL:                        ${scmVars.GIT_URL}"

    if (env.CHANGE_ID || (env.BRANCH_NAME == 'master' && scmVars.GIT_COMMIT != scmVars.GIT_PREVIOUS_SUCCESSFUL_COMMIT)) {
        // run lint and unit tests for any PR or upon new commits/merges to master
        runStages()
    } else {
        echo 'Skipped pipeline for this commit, not a PR or not a new commit on master.'
    }
}

def runLintCheck() {
    try {
        sh "${userPath}/pipenv run flake8 tag/ --output-file flake8-output.txt"
        notify(lintContext, "SUCCESS")
    } catch (err) {
        echo err.getMessage()
        currentBuild.result = "UNSTABLE"
        notify(lintContext, "FAILURE")

        // junit will fail if there's an empty file, for flake8 an empty file is a pass though
        // only evaluate the test results with 'junit' when the flake8 command failed
        try {
            sh "${userPath}/pipenv run flake8_junit flake8-output.txt flake8-output.xml"
            junit 'flake8-output.xml'
        } catch (evalErr) {
            // allow the unit tests to run even if evaluating flake8 results failed...
            echo evalErr.getMessage()
        }
    }
}

def notify(String context, String status) {
    def targetUrl

    if (status == "PENDING") {
        // Always link to the fancy blue ocean UI while the job is running ...
        targetUrl = env.RUN_DISPLAY_URL
    } else {
        switch (context) {
            case lintContext:
                targetUrl =  "${env.BUILD_URL}testReport"
                break
            case unitTestContext:
                targetUrl =  "${env.BUILD_URL}testReport"
                break  
            case coverageContext:
                targetUrl = "${env.BUILD_URL}artifact/advisor/htmlcov/index.html"
                break
            default:
                targetUrl = env.RUN_DISPLAY_URL
                break
        }
    }

    try {
        githubNotify context: context, status: status, targetUrl: targetUrl
    } catch (err) {
        msg = err.getMessage()
        echo "Error notifying GitHub: ${msg}"
    }
}

def runStages() {
    // Fire up a pod on openshift with containers for the DB and the app
    podTemplate(label: podLabel, slaveConnectTimeout: 120, cloud: 'openshift', containers: [
        containerTemplate(
            name: pyContainer,
            image: 'python:3.6.5',
            ttyEnabled: true,
            command: 'cat',
            resourceRequestCpu: '1000m',
            resourceLimitCpu: '1000m',
            resourceRequestMemory: '1Gi',
            resourceLimitMemory: '1Gi'
        )
    ]) {
        node(podLabel) {
            sh "git config --global user.email \"${gitEmail}\""
            sh "git config --global user.name \"${gitName}\""

            // check out source again to get it in this node's workspace
            scmVars = checkout scm

            container(pyContainer) {
                stage('Lint') {
                    runLintCheck()
                }
            }
        }
    }
}
