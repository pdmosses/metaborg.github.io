---
title: "Building"
---
# How to build Spoofax
This how-to guides you on how to build Spoofax from scratch, via the command-line.


## Cloning the Source Code
Clone the source code from the [`spoofax-releng`](https://github.com/metaborg/spoofax-releng) repository with the following commands:

=== "{{ os.macos }}"
    ```bash
    git clone --recursive https://github.com/metaborg/spoofax-releng.git
    cd spoofax-releng
    ```

    !!! warning "{{ os.macos }} Catalina, Big Sur, or newer"
        On macOS Catalina, Big Sur, or newer, you have to install Docker to be able to build Spoofax. This is temporary, until the 32-bit binaries for `sdf2table` and `implodePT` have been phased out.

        See the [requirements for Spoofax Development](requirements.md) for more information.

=== "{{ os.linux }}"
    ```bash
    git clone --recursive https://github.com/metaborg/spoofax-releng.git
    cd spoofax-releng
    ```

=== "{{ os.windows }}"
    ```powershell
    git clone --recursive https://github.com/metaborg/spoofax-releng.git
    cd spoofax-releng

    cd releng\releng
    py -m pip install -r .\requirements.txt
    ```

Cloning and updating submodules can take a while, since we have many submodules and some have a large history.


## Start a Build
To build Spoofax, simply execute:

=== "{{ os.macos }}"
    ```bash
    ./b build all
    ```

=== "{{ os.linux }}"
    ```bash
    ./b build all
    ```

=== "{{ os.windows }}"
    ```powershell
    .\bd.bat build all
    ```

This downloads the latest Stratego/XT, and builds Spoofax. If you also want to build Stratego/XT from scratch, execute:

=== "{{ os.macos }}"
    ```bash
    ./b build -st all
    ```

=== "{{ os.linux }}"
    ```bash
    ./b build -st all
    ```

=== "{{ os.windows }}"
    ```powershell
    .\bd.bat build -st all
    ```

The `-s` flag build Stratego/XT instead of downloading it, and `-t` skips the Stratego/XT tests since they are very lengthy. The `all` part of the command indicates that we want to build all components. For example, if you would only like to build the Java components of Spoofax, and skip the Eclipse plugins, execute:

=== "{{ os.macos }}"
    ```bash
    ./b build java
    ```
    Use `./b build` to get a list of components available for building, and `./b build --help` for help on all the command-line flags and switches.

=== "{{ os.linux }}"
    ```bash
    ./b build java
    ```
    Use `./b build` to get a list of components available for building, and `./b build --help` for help on all the command-line flags and switches.

=== "{{ os.windows }}"
    ```powershell
    .\bd.bat build java
    ```
    Use `.\bd.bat build` to get a list of components available for building, and `.\bd.bat build --help` for help on all the command-line flags and switches.

!!! warning ""
    If you have opened a project in the repository in Eclipse, you **must turn off** _Project_ ‣ _Build Automatically_ in Eclipse, otherwise the Maven and Eclipse compilers will interfere and possibly fail the build. After the Maven build is finished, enable _Build Automatically_ again.


## Updating the Source Code
If you want to update the repository and submodules, execute:

=== "{{ os.macos }}"
    ```bash
    git pull --rebase
    ./b checkout
    ./b update
    ```

=== "{{ os.linux }}"
    ```bash
    git pull --rebase
    ./b checkout
    ./b update
    ```

=== "{{ os.windows }}"
    ```powershell
    git pull --rebase
    .\bd.bat checkout
    .\bd.bat update
    ```

The `git pull` command will update any changes in the main repository. The `./b checkout` command will check out the correct branches in all submodules, because Git does not do this automatically. The `./b update` command will update all submodules.


## Switching to a Different Branch
Switching to a different branch, for example the `spoofax-release` branch, is done with the following commands:

=== "{{ os.macos }}"
    ```bash
    git checkout spoofax-release
    git pull --rebase
    git submodule update --init --remote --recursive
    ./b checkout
    ./b update
    ```

=== "{{ os.linux }}"
    ```bash
    git checkout spoofax-release
    git pull --rebase
    git submodule update --init --remote --recursive
    ./b checkout
    ./b update
    ```

=== "{{ os.windows }}"
    ```powershell
    git checkout spoofax-release
    git pull --rebase
    git submodule update --init --remote --recursive
    .\bd.bat checkout
    .\bd.bat update
    ```


## Troubleshooting
### Resetting and Cleaning
If updating or checking out a branch of submodule fails (because of unstaged or conflicting changes), you can try to resolve it yourself, or you can reset and clean everything. Reset and clean all submodules using:

=== "{{ os.macos }}"
    ```bash
    ./b reset
    ./b clean
    ```

=== "{{ os.linux }}"
    ```bash
    ./b checkout
    ./b update
    ```

=== "{{ os.windows }}"
    ```powershell
    .\bd.bat reset
    .\bd.bat clean
    ```

!!! warning "Risk of loss of data"
    Resetting and cleaning **deletes uncommitted and unpushed changes**, which can cause **permanent data loss**. Make sure all your changes are committed _and_ pushed!

### Weird Compilation Errors
If you get any weird compilation errors during the command-line build, make sure that _Project_ ‣ _Build Automatically_ is turned off in Eclipse.
