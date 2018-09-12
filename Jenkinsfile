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
lintContext = "continuous-integration/jenkins/lint"
pipInstallContext = "continuous-integration/jenkins/pipinstall"
userPath = '/home/jenkins/.local/bin'
lockErrorRegex = /.*Your Pipfile.lock \(\S+\) is out of date. Expected: \(\S+\).*/
lockError = "\n* `Pipfile.lock` is out of sync. Run '`pipenv lock`' and commit the changes."
installError = "\n* '`pipenv install`' has failed."

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
        resetContexts()
        runStages()
    } else {
        echo 'Skipped pipeline for this commit, not a PR or not a new commit on master.'
    }
}

def resetContexts() {
    notify(lintContext, "PENDING")
    notify(pipInstallContext, "PENDING")
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

def removePipfileComments() {
    try {
        for (comment in pullRequest.comments) {
            if (comment.body.contains("Pipfile violation")) {
                deleteComment(comment.id)
            }
        }
    } catch (err) {
        msg = err.getMessage()
        echo "Error removing Pipfile comments: ${msg}"
    }
}

def postPipfileComment(commitId, str) {
    def shortId = commitId.substring(0, 7)
    def body = "Commit `${shortId}` Pipfile violation\n${str}"
    try {
        pullRequest.comment(body)
    } catch (err) {
        msg = err.getMessage()
        echo "Error adding Pipfile comment: ${msg}"
    }
}

def runPipInstall(scmVars) {
    sh "pip install --user --no-warn-script-location pipenv"
    sh "${userPath}/pipenv run pip install --upgrade pip"

    // NOTE: Removing old comments won't work unless Pipeline Github Plugin >= v2.0
    removePipfileComments()

    // use --deploy to check if Pipfile and Pipfile.lock are in sync
    def cmdStatus = sh(
        script: "${userPath}/pipenv install --dev --deploy --verbose > pipenv_install_out.txt",
        returnStatus: true
    )

    def installFailed = false
    def errorMsg = ""
    if (cmdStatus != 0) { 
        if (readFile('pipenv_install_out.txt').trim() ==~ lockErrorRegex) {
            currentBuild.result = "UNSTABLE"
            errorMsg += lockError
            // try to install without the deploy flag to allow the other tests to run
            try {
                sh "${userPath}/pipenv install --dev --verbose"
            } catch (err) {
                // second try without --deploy failed too, fail this build.
                echo err.getMessage()
                installFailed = true
                errorMsg += installError
            }
        } else {
            // something else failed (not a lock error), fail this build.
            echo err.getMessage()
            installFailed = true
            errorMsg += installError
        }
    }

    if (errorMsg) {
        postPipfileComment(scmVars.GIT_COMMIT, errorMsg)
    }
    if (installFailed) {
        error("pipenv install has failed")
        notify(pipInstallContext, "FAILURE")
    } else {
        notify(pipInstallContext, "SUCCESS")
    }
}

def runStages() {
    // Fire up a pod on openshift with containers for the DB and the app
    podTemplate(label: podLabel, slaveConnectTimeout: 120, cloud: 'openshift', containers: [
        containerTemplate(
            name: 'jnlp',
            image: 'registry.access.redhat.com/openshift3/jenkins-slave-nodejs-rhel7',
            args: '${computer.jnlpmac} ${computer.name}',
            resourceRequestCpu: '500m',
            resourceLimitCpu: '500m',
            resourceRequestMemory: '500Mi',
            resourceLimitMemory: '650Mi'
        ),
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
                stage('Pip install') {
                    runPipInstall(scmVars)
                }

                stage('Lint') {
                    runLintCheck()
                }
            }
        }
    }
}
