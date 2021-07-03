# Spoofax Development Maven Setup
Maven is a project management and build tool for software projects. Most components in Spoofax are built with Maven. This how-to will guide you to setup Maven for Spoofax 2 development.


## Installation
Maven can be downloaded and installed from <https://maven.apache.org/download.cgi>. We require Maven 3.5.4 or newer (except Maven 3.6.1 and 3.6.2). On macOs, Maven can be easily installed with [Homebrew](https://brew.sh/) by executing:

```bash
brew install maven
```

Confirm the installation was successful and the version is supported by running `mvn --version`.


## Memory Allocation
By default, Maven does not assign a lot of memory to the JVM that it runs in, which may lead to out-of-memory exceptions during builds. To increase the allocated memory, execute before building:

```bash
export MAVEN_OPTS="-Xms512m -Xmx1024m -Xss16m"
```

!!! note ""
    Such an export is not permanent. To make it permanent, add that line to `~/.bashrc` or equivalent for your OS/shell (create the file if it does not exist), which will execute it whenever a new shell is opened.


## Proxy Settings
If you are behind a proxy, please put the proxy settings in your `~/.m2/settings.xml` file. When you use the `./b` script to build Spoofax, the `MAVEN_OPTS` environment variable is overridden to ensure the memory options above are supplied, so using command-line options in the environment variable for the proxy settings does not work.


## Spoofax Maven Artifacts
Spoofax’s Maven artifacts are hosted on our artifact server at [artifacts.metaborg.org](https://artifacts.metaborg.org). To use these artifacts, repositories have to be added to your Maven configuration. This configuration is required when building and developing Spoofax. Repositories can be added to your local Maven settings file (which is recommended), or to a project’s POM file.


## Simple: Local Settings File
The recommended approach is to add repositories to your local Maven settings file, located at `~/.m2/settings.xml`. If you have not created this file yet, or want to completely replace it, simply create it with the following content:

???+ quote "`~/.m2/settings.xml`"
    ```xml
    <?xml version="1.0" ?>
    <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
        <profiles>
            <profile>
            <id>add-metaborg-release-repos</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <repositories>
                <repository>
                <id>metaborg-release-repo</id>
                <url>https://artifacts.metaborg.org/content/repositories/releases/</url>
                <releases>
                    <enabled>true</enabled>
                </releases>
                <snapshots>
                    <enabled>false</enabled>
                </snapshots>
                </repository>
            </repositories>
            <pluginRepositories>
                <pluginRepository>
                <id>metaborg-release-repo</id>
                <url>https://artifacts.metaborg.org/content/repositories/releases/</url>
                <releases>
                    <enabled>true</enabled>
                </releases>
                <snapshots>
                    <enabled>false</enabled>
                </snapshots>
                </pluginRepository>
            </pluginRepositories>
            </profile>
            <profile>
            <id>add-metaborg-snapshot-repos</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <repositories>
                <repository>
                <id>metaborg-snapshot-repo</id>
                <url>https://artifacts.metaborg.org/content/repositories/snapshots/</url>
                <releases>
                    <enabled>false</enabled>
                </releases>
                <snapshots>
                    <enabled>true</enabled>
                </snapshots>
                </repository>
            </repositories>
            <pluginRepositories>
                <pluginRepository>
                <id>metaborg-snapshot-repo</id>
                <url>https://artifacts.metaborg.org/content/repositories/snapshots/</url>
                <releases>
                    <enabled>false</enabled>
                </releases>
                <snapshots>
                    <enabled>true</enabled>
                </snapshots>
                </pluginRepository>
            </pluginRepositories>
            </profile>
        </profiles>
        <mirrors>
            <mirror>
            <id>metaborg-central-mirror</id>
            <url>https://artifacts.metaborg.org/content/repositories/central/</url>
            <mirrorOf>central</mirrorOf>
            </mirror>
        </mirrors>
    </settings>
    ```

If you’ve already created a settings file before and want to add the repositories, just add the `profile` element (and the `profiles` element if it does not exist yet) to the settings file.


## Advanced: Project POM File
Repositories can also be added directly to a project’s POM file, which only set the repositories for that particular project. This is not recommended, because it makes repositories harder to change by users, and duplicates the configuration. But it can be convenient, because it does not require an external settings file.

To do this, just add the the following content to the POM file:

???+ quote "`~/.m2/settings.xml`"
    ```xml
    <repositories>
        <repository>
            <id>metaborg-release-repo</id>
            <url>https://artifacts.metaborg.org/content/repositories/releases/</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </repository>
        <repository>
            <id>metaborg-snapshot-repo</id>
            <url>https://artifacts.metaborg.org/content/repositories/snapshots/</url>
            <releases>
                <enabled>false</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </repository>
    </repositories>

    <pluginRepositories>
        <pluginRepository>
            <id>metaborg-release-repo</id>
            <url>https://artifacts.metaborg.org/content/repositories/releases/</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </pluginRepository>
        <pluginRepository>
            <id>metaborg-snapshot-repo</id>
            <url>https://artifacts.metaborg.org/content/repositories/snapshots/</url>
            <releases>
                <enabled>false</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </pluginRepository>
    </pluginRepositories>
    ```


## Maven Central Repository Mirror
Artifacts of most open source projects are hosted in the [Maven Central Repository](https://search.maven.org/). If you are building any project using Maven, many artifacts will be downloaded from that server. While it is a fast server, it can still take a while to download all required artifacts for big projects.

If you are on the TU Delft network, you can use our local mirror of Maven Central to speed things up. Using the mirroring requires a change in your local `~/.m2/settings.xml` file. If this file does not exist, create it with the following content:

???+ quote "`~/.m2/settings.xml`"
    ```xml
    <?xml version="1.0" ?>
    <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
        <mirrors>
            <mirror>
                <id>metaborg-central-mirror</id>
                <url>https://artifacts.metaborg.org/content/repositories/central/</url>
                <mirrorOf>central</mirrorOf>
            </mirror>
        </mirrors>
    </settings>
    ```

If you’ve already created a settings file before and want to add the mirror configuration, just add the `mirror` element (and the `mirrors` element if it does not exist yet) to the settings file.