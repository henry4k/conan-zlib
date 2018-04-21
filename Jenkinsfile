def createCacheDir() {
    def cacheDir = "${env.HOME}/.crosscompile-cache"
    sh "mkdir -p '${cacheDir}'"
    return cacheDir
}

def withDockerImage(imageName, closure) {
    node('4bf288b3ce') {
        def cacheDir = createCacheDir()
        def args = "--mount 'type=bind,source=${cacheDir},destination=/cache'"
        docker.image(imageName).inside(args, closure)
    }
}

def buildStage(config) {
    withDockerImage('henry4k/crossbuild:1.0') {
        stage("Build with ${config.name}") {
            unstash 'source'
            sh "conan remote add henry4k 'https://api.bintray.com/conan/henry4k/conan'"
            sh 'GIT_COMMITTER_NAME=noone '+ // Otherwise `git clone` won't work.
               'GIT_COMMITTER_EMAIL=noone@example.org '+
               "conan create --profile ${config.triple} "+
                            '--build=outdated '+
                            '. '+
                            'noone/nothing'
        }
    }
}

def buildConfigs = [[name: 'windows-x64', triple: 'x86_64-w64-mingw32']/*,
                    [name: 'apple-x64',   triple: 'x86_64-apple-darwin14']*/]

node {
    stage('Checkout') {
        checkout scm
        stash name: 'source', includes: '**'
    }

    stage('Build') {
        def stages = [:]
        for (int i = 0; i < buildConfigs.size(); i++) {
            def config = buildConfigs[i]
            stages[config.name] = {
                buildStage(config)
            }
        }

        stages.failFast = true
        parallel stages
    }
}

// vim: set filetype=groovy:
