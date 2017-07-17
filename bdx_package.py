
# ----------------------------------
# bdx_package.py - by SolarLune, 2017
# ----------------------------------
#
# This script is used to handle packaging and distribution of runtime-environment ("jre") based games
# (like LibGDX, Java-based games).
#
# You can specify for each target OS what runtime environment to include, and which files to include.
# You can also specify files that should be removed from the runtime environment to save space.
#
# This essentially does what packr does, but manually, and without an executable. You instead
# package a bash or batch file that invokes the packaged runtime environment with your game file.

import subprocess, shutil, os

a = ""
v = ""

with open("build.gradle") as gradle:

    for line in gradle.readlines():

        if "version" in line:

            v = line.split()[-1].replace("'", "")

        if "appName" in line:

            a = line.split()[-1].replace("'", "").replace(";", "")

appName = a + "-" + v + ".jar"                  # Determining what the outputted .jar will be named

settings = {

    "jre_removable":{       # A list of directories and files that can be removed from the packaged JRE to reduce space
        "src.zip",
        "sample",
        "demo",
        "include",
        "man",
        "plugin",
        "lib/ext",
        "lib/deploy",
        "lib/desktop",
        "lib/oblique-fonts",
        "lib/deploy.jar",
        "lib/plugin.jar",
        "lib/fonts",
    },

    "configs": {            # Where the configurations for each OS goes

        "windows": {
            "jre": "/home/solarlune/Tools/JREs/jre-8u131-windows-i586/",# We want to include the JRE,
            "files": ["desktop/build/libs/" + appName,                  # the game itself,
                      "packaged/resources/Gearend.bat",                 # a batch file that runs it using our JRE,
                      "packaged/resources/Readme.txt"]                  # as well as any other misc. files
        },

        "linux64": {
            "jre": "/home/solarlune/Tools/JREs/jre-8u131-linux-x64",    # Same for all other OSes
            "files": ["desktop/build/libs/" + appName,
                      "packaged/resources/Gearend.sh",
                      "packaged/resources/Readme.txt"]
        },

        "linux32": {
            "jre": "/home/solarlune/Tools/JREs/jre-8u131-linux-i586",
            "files": ["desktop/build/libs/" + appName,
                      "packaged/resources/Gearend.sh",
                      "packaged/resources/Readme.txt"]
        },

        "osx": {
            "jre": "/home/solarlune/Tools/JREs/jre-8u131-macosx-x64",
            "files": ["desktop/build/libs/" + appName,
                      "packaged/resources/Gearend.sh",
                      "packaged/resources/Readme.txt"]
        },

        # "crossplatform": {
        #     "jre": None,                                              # You can also not package a JRE
        #     "files": ["desktop/build/libs/" + appName,
        #               "packaged/resources/Gearend_crossplatform.bat",
        #               "packaged/resources/Gearend_crossplatform.sh",
        #               "packaged/resources/Readme.txt"]
        # }

    }

}

print("Distribution process started. Building JAR file.")

subprocess.call(["./gradlew", "desktop:dist"])  # The build process for a LibGDX game using gradle

if not os.path.exists("packaged"):
    os.mkdir("packaged")

def output(release_mode="release"):

    print("Packaging " + appName + " for " + release_mode + ".")

    if not os.path.exists(os.path.join("packaged", release_mode)):
        os.mkdir(os.path.join("packaged", release_mode))

    for os_conf in settings['configs']:

        config = settings['configs'][os_conf]

        print("Packaging " + os_conf + "...\r", end="")

        targetDir = os.path.join("packaged", release_mode, os_conf)

        if os.path.exists(targetDir):
            shutil.rmtree(targetDir)         # Start fresh; remove anything that was already in the folder
        else:
            os.mkdir(targetDir)

        if config["jre"] is not None:

            jre_dir = os.path.join("packaged", release_mode, os_conf, "jre")

            shutil.copytree(config["jre"], jre_dir)

            for fp in settings["jre_removable"]:

                path = os.path.join(jre_dir, fp)

                if os.path.exists(path):

                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        shutil.rmtree(path)

        for file in config['files']:
            shutil.copy(file, targetDir)

        # Here you'd put your distribution stuff for itch.io, Steam, etc.

        print("Packaging " + os_conf + " done!")

    print ("Packaging " + appName + " for " + release_mode + " complete!")

output("release")