---
title: "Requirements"
---
# Spoofax Development Requirements
This how-to will instruct you which requirements you need to install to do Spoofax 2 development. Spoofax can be run on macOS, Linux, and Windows. Building is directly supported on macOS and Linux. Building on Windows is supported through the [Windows Subsystem for Linux (Bash on Windows)](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide).

The following tools are required to build and develop Spoofax:


??? summary "Git 1.8.2 or newer"
    Required to check out the source code from our GitHub repositories. Instructions on how to install Git for your platform can be found here: <https://git-scm.com/downloads>.

    If you run macOs and have [Homebrew](https://brew.sh/) installed, you can install Git by executing `brew install git`. Confirm your Git installation by executing `git version`.


??? summary "Java JDK 8u141 or newer"
    Required to build and run Java components. The latest JDK can be downloaded and installed from: <https://www.oracle.com/technetwork/java/javase/downloads/index.html>. If using Java 8, 8u141 or newer is required because of [issues with Let's Encrypt certificates](https://letsencrypt.org/docs/certificate-compatibility/).

    On macOS, it can be a bit tricky to use the installed JDK, because Apple by default installs JRE 6. To check which version of Java you are running, execute the `java -version` command. If this tells you that the Java version is 1.8 or newer, or Java 9 or newer, everything is fine. If not, you can either install a newer Java version through [Homebrew](https://brew.sh/) (`brew install --cask adoptopenjdk8`), or use a JDK manager such as [SDKMAN!](https://sdkman.io/).


??? summary "Python 3.4 or newer"
    Python scripts are used to orchestrate the build. Instructions on how to install Python for your platform can be found here: <https://www.python.org/downloads/>.

    If you run macOs and have [Homebrew](https://brew.sh/) installed, you can install Python by executing `brew install python3`. Confirm your Python installation by executing `python3 --version` or `python --version`, depending on how your package manager sets up Python.

    During a build of Spoofax, Pip will install some Python dependencies into a virtual environment. No extra Python dependencies are required for this (with one small exception, see the note below). The latest version of Pip will automatically be installed inside the virtual environment.

    !!! warning ""
        Debian and derivatives (like Ubuntu) do not include the full standard library when installing Python ([bug 1290847](https://bugs.launchpad.net/ubuntu/+source/python3.4/+bug/1290847/+index?comments=all)), so you will need to install `python3-venv` to ensure the virtual environment can be created.


??? summary "Maven 3.5.4 or newer (except Maven 3.6.1 and 3.6.2)"
    Maven is required to build most components of Spoofax. Our Maven artifact server must also be registered with Maven since the build depends on artifacts from previous builds for bootstrapping purposes. We explain how to install and set up Maven in [this how-to](maven.md).

    !!! warning ""
        Spoofax cannot be built using Maven 3.6.1 or 3.6.2 due to bugs [MNG-6642](https://issues.apache.org/jira/browse/MNG-6642) and [MNG-6765](https://issues.apache.org/jira/browse/MNG-6765).


??? summary "Docker"
    Required on macOS Catalina, Big Sur, Monterey, and newer to be able to run the `sdf2table` and `implodePT` legacy binaries. On macOS, install it though the [Docker for Mac](https://docs.docker.com/docker-for-mac/install/) website.


??? summary "Coreutils"
    Required on macOS to be able to run the `sdf2table` and `implodePT` legacy binaries. On macOS with [Homebrew](https://brew.sh/) installed, you can install them by running `brew install coreutils`.