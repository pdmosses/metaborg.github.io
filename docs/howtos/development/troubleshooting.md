# Development Troubleshooting
This page provides some troubleshooting information.


## Developing on macOS Catalina and newer
Due to some legacy 32-bit binaries (`sdf2table` and `implodePT`) that are required to build some of the Spoofax meta-languages, building on {{os.macos}} Catalina or newer (Big Sur, Monterey) requires the following additional components to be installed:

- `coreutils`
- Docker for Mac

Refer to the [Requirements](requirements.md) page for more information and installation instructions. The following subsections detail some problems that can occur when developing on macOS Catalina or newer.


### realpath: command not found
You should install `coreutils`. Refer to the [Requirements](requirements.md) page for installation instructions.

Invoke the following command to test it (it should return the full path to the current directory):

```
realpath -s .
```


### Mounts denied: The path is not shared the host and is not known to Docker
```
Error response from daemon: Mounts denied: 
The path /var/folders/a_/foo0000bar/T/vfs_cache-345/tmp_123_macosx/sdf2table-macosx
is not shared from the host and is not known to Docker.
```

Ensure the root of the path (`/var/folders` in this example) is shared in Docker for Mac. Go to Docker for Mac _Preferences_ ‣ _Resources_ ‣ _File Sharing_ and add the path to the list. The default list should contain:

- `/Users`
- `/Volumes`
- `/private`
- `/tmp`
- `/var/folders`


### invalid mount config for type "bind": bind source path does not exist
```
Error response from daemon: invalid mount config for type "bind":
bind source path does not exist:
/var/folders/a_/foo0000bar/T/vfs_cache-345/tmp_123_macosx
```

Ensure that both Docker and the terminal from which you are invoking the build have _full-disk access_. Go to macOS _Preferences_ ‣ _Security and Privacy_ ‣ _Full Disk Access_ and check the checkboxes next to _Docker_ and your terminal (_Terminal_ and/or _iTerm_).
