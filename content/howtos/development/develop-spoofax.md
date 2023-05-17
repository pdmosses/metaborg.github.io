---
title: "Developing"
---
# How to develop Spoofax
If you are developing a project that is included in Spoofax, it is recommended to set up a development environment. This how-to describes how to set up such a development environment.

!!! note ""
    A working Spoofax build is required before being able to develop. You must be able to successfully build Spoofax by running `./b build all`. Do not continue if this does not work. See the [instructions on how to build Spoofax](./build-spoofax.md).


## Eclipse
Currently, an Eclipse development environment is the most supported environment. An Eclipse development environment can be generated with our scripts.

### Generating an Eclipse Instance
The `./b` script in the `spoofax-releng` repository can generate an Eclipse installation for you. Change directory into the `spoofax-releng` repository and run:

```bash
./b gen-spoofax -l -d ~/eclipse/spoofax-dev
```

This will download and install Eclipse into `~/eclipse/spoofax-dev` with the right plugins and `eclipse.ini` for Spoofax development. The locally built version of the Spoofax plugin will be installed into that Eclipse. Generating an Eclipse installation can take several minutes. After it’s done generating, open the Eclipse installation and confirm that it works by creating a Spoofax project.

??? info "RuntimeError: Eclipse generation failed"
    If you get the error _"RuntimeError: Eclipse generation failed"_, then ensure you're building Eclipse using JDK 8.

??? info "Installation failed. Cannot complete the install because of a conflicting dependency"
    If you get an error _"Installation failed. Cannot complete the install because of a conflicting dependency."_, then make sure there is not an existing Eclipse instance at the destination.

??? info "{{os.macos}}: To open “Eclipse” you need to install the legacy Java SE 6 runtime"
    If upon starting Eclipse you get the error _"To open “Eclipse” you need to install the legacy Java SE 6 runtime"_, then you should install a Java JDK 8 or newer for Eclipse to use (Java 11 or newer is recommended). If you installed one through [SDKMAN!](https://sdkman.io/) then you have to point Eclipse to it. To do this, edit the `Contents/Eclipse/eclipse.ini` file in the Eclipse application package content. Add the following lines at the start of the file, where <USERNAME> is your username:

    ```ini
    -vm
    /Users/<USERNAME>/.sdkman/candidates/java/current/jre/lib/jli/libjli.dylib
    ```


### Fixing Eclipse Settings
Some Eclipse settings unfortunately have sub-optimal defaults. Go to the Eclipse preferences and set these options:

- General
    - **Enable**: Keep next/previous editor, view and perspectives dialog open
- General ‣ Startup and Shutdown
    - **Enable**: Refresh workspace on startup
- General ‣ Workspace
    - **Enable**: Refresh using native hooks or polling
- Maven
    - **Enable**: Do not automatically update dependencies from remote repositories
    - **Enable**: Download Artifact Sources
    - **Enable**: Download Artifact JavaDoc
- Maven ‣ Annotation Processing
    - **Enable**: Automatically configure JDT APT
- Maven ‣ User Interface
    - **Enable**: Open XML page in the POM editor by default
- Run/Debug ‣ Launching
    - **Disable**: Build (if required) before launching


### Developing
Import the projects you’d like to develop. To import Java and language projects, use _Import ‣ Maven ‣ Existing Maven Projects_. Eclipse plugins are still imported with _Import ‣ General ‣ Existing Projects into Workspace_.


### Running
To test your changes in the Spoofax Eclipse plugin, import the `org.metaborg.spoofax.eclipse` project from the `spoofax-eclipse` repository, which provides launch configurations for starting new Eclipse instances (a “guest” Eclipse). Press the little down arrow next to the bug icon (next to the play icon) and choose _Spoofax Eclipse Plugin_ to start a new Eclipse instance that contains your changes. If it is not in the list of recently used configurations, click _Debug configurations..._, it should be under _Eclipse Application configurations_.

Some tricks:

- If you change a (meta-)language and want to test it in a new Eclipse instance, import that language’s corresponding Eclipse plugin project. For example, `org.metaborg.meta.lang.nabl` has Eclipse plugin project `org.metaborg.meta.lang.nabl.eclipse`. Then compile both those projects from the command-line (don’t forget to turn off _Build Automatically_ in Eclipse), and start a new Eclipse instance.
- A different way to test the (meta-)language change is to import that language project into the workspace of the guest Eclipse. Because we use Maven snapshot versions, the built-in version will be overridden when you build the language in the guest eclipse.


### Troubleshooting
If there are many errors in a project, try updating the Maven project. Right click the project and choose _Maven_ ‣ _Update Project..._, uncheck _Clean projects_ in the new dialog and press _OK_. This will update the project from the POM file, update any dependencies, and trigger a build. If this does not solve the problems, try it again but this time with _Clean projects_ checked. Note that if you clean a language project, it has to be rebuilt from the command-line. Restarting Eclipse and repeating these steps may also help.

Multiple projects can be updated by selecting multiple projects in the package/project explorer, or by checking projects in the update dialog.

If you have particular trouble with `org.eclipse.*` plugins in the `MANIFEST.MF` file that do not resolve, try the following. Go to _Preferences_ ‣ _Plug-in Development_ ‣ _Target Platform_, most likely there will not be an active _Running Platform_ there. You can use _Add..._ to add a new one if there isn’t one already. Select the _Default_ option, click _Next_, then click _Finish_. Check the box next to the platform to activate it.


### Advanced: Developing from Scratch
In some cases it can be beneficial to have full control over all projects, instead of relying on Maven artifacts and the installed Spoofax plugin. To develop completely from scratch, uninstall Spoofax from Eclipse, and import all projects by importing `releng/eclipse/import/pom.xml`, which will import all relevant projects automatically.

If you change a language project, build them on the command-line, because languages cannot be built inside Eclipse without the Spoofax plugin.


## IntelliJ
Easiest is to install the [latest release of the Spoofax plugin](../../release/stable.md) in an installation of IntelliJ IDEA.

Otherwise, you may want to build it from source, and to run the built plugin inside a special sandbox-instance of IntelliJ IDEA, execute the following command:

```bash
./gradlew runIdea
```

Alternatively, in IntelliJ IDEA you can invoke the _IntelliJ Plugin_ run/debug configuration. You can use this to run or debug the IntelliJ IDEA plugin code. However, this cannot be used to debug the JPS Spoofax build process.

To debug the JPS Spoofax build process, you need to execute the following command:

```bash
./gradlew debugJps
```

...or invoke the _IntelliJ Plugin (Debug JPS)_ run configuration (_not debug_) from IntelliJ. Then in the sandbox IntelliJ IDEA instance you enable the _Debug Build Process_ action (++ctrl+shift+a++). Then you start a build. IntelliJ will wait for a debugger to be attached to port 5005. Attach a debugger, and the build will continue. From the Spoofax plugin’s IntelliJ IDEA project, you can invoke the _JPS Plugin_ remote debug configuration to attach the debugger.


### Logging
To get debug logging in IntelliJ, locate the `bin/log.xml` file in the IntelliJ folder and add the following snippet in the `#!xml <log4j:configuration>` element, just above the `#!xml <root>` element:

```xml
<category name="#org.metaborg" additivity="true">
    <priority value="DEBUG"/>
    <appender-ref ref="CONSOLE-DEBUG"/>
    <appender-ref ref="FILE"/>
</category>
```
