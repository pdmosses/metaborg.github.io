---
title: "Install on macOS M1, M2"
---
# How to install Spoofax on macOS ARM (M1, M2)
Currently the Eclipse with bundled JRE does not yet support M1.  We recommend downloading [Spoofax Eclipse _without the embedded JRE_]({{ release.rel.eclipse.install.macos_64 }}).  Then either use the JDK 8 that is installed by default on macOS M1/M2, or install your own.

To configure Eclipse to use an installed JDK:

1.  In the Finder, right-click the Spoofax app, choose _Show Package Contents_.
2.  Browse to `Contents/Eclipse`.
3.  Edit the `eclipse.ini` file.
4.  Replace or add two lines at the top of the file with the `-vm` argument:

    ```
    -vm
    <path>
    ```

    Where `<path>` is the path of your JDK, using one of the approaches below.


## Using macOS default JDK
If you want to use the default JDK 8 that is installed with macOS, you can verify its version number:

```shell
java -version
```

This should print something like:

```
java version "1.8.0_202"
Java(TM) SE Runtime Environment (build 1.8.0_202-b08)
Java HotSpot(TM) 64-Bit Server VM (build 25.202-b08, mixed mode)
```

The `-vm` path you should use in this case should be something like:

```
-vm
/Library/Java/JavaVirtualMachines/jdk1.8.0_202.jdk/Contents/Home/bin
```


## Installing a custom JDK
To install and use a custom JDK for Spoofax, we recommend using [SDKman](https://sdkman.io/).  However, only an x86 JDK is supported.  Therefore SDKman has to be configured to use x86 JDKs that are compatible with the Rosetta 2 emulation layer:

1.  Edit the file `~/.sdkman/etc/config`.
2.  Change the value of `sdkman_rosetta2_compatible` to `true` (it is `false` by default).
3.  Save and close the file.
4.  Restart your terminal to apply the changes.

Now you can install a JDK.  We tested this with JDK 11 (recommended) but Java 8 and newer should work.  For example:

```shell
sdk install java 11.0.18-tem
```

!!! note ""
    For Temurin, JDK 8 should be the lowest version of JDK that is listed.  If the lowest version of Temurin is JDK 11, then the above change to `sdkman_rosetta2_compatible=true` was not applied correctly or the terminal was not restarted.

Once installed, the `-vm` path in the Eclipse installation should be something like:

```
-vm
/Users/myusername/.sdkman/candidates/java/11.0.18-tem/bin
```

Or alternatively, but perhaps less predictable, use whatever version is set as the _current_ default version of Java (using `sdk default java`):

```
-vm
/Users/myusername/.sdkman/candidates/java/current/bin
```



