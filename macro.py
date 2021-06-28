from typing import Optional

windows_icon = ":fontawesome-brands-windows:"
macos_icon = ":fontawesome-brands-apple:"
linux_icon = ":fontawesome-brands-linux:"

def artifacts_download_link(repo: str, artifact: str, classifier: str, packaging: str, version="LATEST", group="org.metaborg"):
    return f"https://artifacts.metaborg.org/service/local/artifact/maven/redirect?r={repo}&g={group}&a={artifact}&c={classifier}&p={packaging}&v={version}"


def eclipse_lwb_artifacts_download(repo: str, variant: str, packaging: str, version: str):
    return artifacts_download_link(repo, "org.metaborg.spoofax.eclipse.dist", variant, packaging, version)


def eclipse_lwb_buildfarm_download(variant: str, packaging: str):
    return f"http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-{variant}.{packaging}"


def download_markdown_link(icon: str, name: str, link: str):
    return f"{icon} [{name}]({link})"


def fill_env_with_release(env, env_version: str, version: str, download_version: str, date: Optional[str]):
    repo = "snapshots" if "SNAPSHOT" in version else "releases"

    if "SNAPSHOT" in version:
        macos_64_jre = eclipse_lwb_buildfarm_download("macosx-x64-jre", "tar.gz")
        linux_64_jre = eclipse_lwb_buildfarm_download("linux-x64-jre", "tar.gz")
        windows_64_jre = eclipse_lwb_buildfarm_download("windows-x64-jre", "zip")
        windows_32_jre = eclipse_lwb_buildfarm_download("windows-x86-jre", "zip")
        macos_64 = eclipse_lwb_buildfarm_download("macosx-x64", "tar.gz")
        linux_64 = eclipse_lwb_buildfarm_download("linux-x64", "tar.gz")
        windows_64 = eclipse_lwb_buildfarm_download("windows-x64", "zip")
        windows_32 = eclipse_lwb_buildfarm_download("windows-x86", "zip")
        repository = "http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/site/"
    else:
        macos_64_jre = eclipse_lwb_artifacts_download(repo, "macosx-x64-jre", "tar.gz", download_version)
        linux_64_jre = eclipse_lwb_artifacts_download(repo, "linux-x64-jre", "tar.gz", download_version)
        windows_64_jre = eclipse_lwb_artifacts_download(repo, "windows-x64-jre", "zip", download_version)
        windows_32_jre = eclipse_lwb_artifacts_download(repo, "windows-x86-jre", "zip", download_version)
        macos_64 = eclipse_lwb_artifacts_download(repo, "macosx-x64", "tar.gz", download_version)
        linux_64 = eclipse_lwb_artifacts_download(repo, "linux-x64", "tar.gz", download_version)
        windows_64 = eclipse_lwb_artifacts_download(repo, "windows-x64", "zip", download_version)
        windows_32 = eclipse_lwb_artifacts_download(repo, "windows-x86", "zip", download_version)
        repository = f"https://artifacts.metaborg.org/content/unzip/releases-unzipped/org/metaborg/org.metaborg.spoofax.eclipse.updatesite/{version}/org.metaborg.spoofax.eclipse.updatesite-{version}-assembly.zip-unzip/"

    env.variables.release[env_version] = {
        "date": date,
        "version": version,
        "eclipse": {
            "install": {
                "jvm": {
                    "link": {
                        "macos_64": download_markdown_link(macos_icon, "macOS 64-bit with embedded JVM", macos_64_jre),
                        "linux_64": download_markdown_link(linux_icon, "Linux 64-bit with embedded JVM", linux_64_jre),
                        "windows_64": download_markdown_link(windows_icon, "Windows 64-bit with embedded JVM", windows_64_jre),
                        "windows_32": download_markdown_link(windows_icon, "Windows 32-bit with embedded JVM", windows_32_jre),
                    },
                    "macos_64": macos_64_jre,
                    "linux_64": linux_64_jre,
                    "windows_64": windows_64_jre,
                    "windows_32": windows_32_jre,
                },
                "link": {
                    "macos_64": download_markdown_link(macos_icon, "macOS 64-bit with embedded JVM", macos_64_jre),
                    "linux_64": download_markdown_link(linux_icon, "Linux 64-bit with embedded JVM", linux_64_jre),
                    "windows_64": download_markdown_link(windows_icon, "Windows 64-bit with embedded JVM", windows_64_jre),
                    "windows_32": download_markdown_link(windows_icon, "Windows 32-bit with embedded JVM", windows_32_jre),
                },
                "macos_64": macos_64,
                "linux_64": linux_64,
                "windows_64": windows_64,
                "windows_32": windows_32,
            },
            "repository": repository
        }
    }


release_versions = {
    "2.5.16": "28-05-2021"
}
development_version = "2.6.0-SNAPSHOT"


def define_env(env):
    env.variables.os = {
        "windows": f"{windows_icon} Windows",
        "linux": f"{linux_icon} Linux",
        "macos": f"{macos_icon} macOS",
    }
    env.variables.release = {}
    for version, date in release_versions.items():
        fill_env_with_release(env, version, version, version, date)
    latest_rel_version, latest_rel_date = next(iter(release_versions.items()))
    fill_env_with_release(env, "rel", latest_rel_version, latest_rel_version, latest_rel_date)
    fill_env_with_release(env, "dev", development_version, "LATEST", None)
