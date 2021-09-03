from typing import Optional

windows_icon = ":fontawesome-brands-windows:"
macos_icon = ":fontawesome-brands-apple:"
linux_icon = ":fontawesome-brands-linux:"
warning_icon = ":fontawesome-solid-exclamation-triangle:"
stop_icon = ":fontawesome-solid-times-circle:"

artifacts_url_base = 'https://artifacts.metaborg.org'
artifacts_releases_url = f'{artifacts_url_base}/content/repositories/releases/org/metaborg/'


def artifacts_download(repo, artifact, classifier=None, packaging="jar", version="LATEST", group="org.metaborg"):
    return f'{artifacts_url_base}/service/local/artifact/maven/redirect?r={repo}&g={group}' \
           f'&a={artifact}{f"&c={classifier}" if classifier is not None else ""}&p={packaging}&v={version}'


def eclipse_lwb_artifacts_download(repo: str, variant: str, packaging: str, version: str):
    return artifacts_download(repo, "org.metaborg.spoofax.eclipse.dist", variant, packaging, version)


buildfarm_url_base = 'https://buildfarm.metaborg.org'


def buildfarm_download(path: str):
    return f'{buildfarm_url_base}/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/{path}'


def eclipse_lwb_buildfarm_download(variant: str, packaging: str):
    return buildfarm_download(f'dist/spoofax/eclipse/spoofax-{variant}.{packaging}')


macos_64_jre_variant = 'macosx-x64-jre'
linux_64_jre_variant = 'linux-x64-jre'
win_64_jre_variant = 'windows-x64-jre'
win_32_jre_variant = "windows-x86-jre"
macos_64_variant = 'macosx-x64'
linux_64_variant = "linux-x64"
win_64_variant = 'windows-x64'
win_32_variant = 'windows-x86'

macos_archive_ext = 'tar.gz'
linux_archive_ext = 'tar.gz'
win_archive_ext = 'zip'


def download_link(icon: str, name: str, link: str):
    return f"{icon} [{name}]({link})"


def fill_vars_with_release(vars, env_version: str, version: str, download_version: str, date: Optional[str]):
    repo = 'snapshots' if 'SNAPSHOT' in version else 'releases'

    if 'SNAPSHOT' in version:
        macos_64_jre = eclipse_lwb_buildfarm_download(macos_64_jre_variant, macos_archive_ext)
        linux_64_jre = eclipse_lwb_buildfarm_download(linux_64_jre_variant, linux_archive_ext)
        windows_64_jre = eclipse_lwb_buildfarm_download(win_64_jre_variant, win_archive_ext)
        windows_32_jre = eclipse_lwb_buildfarm_download(win_32_jre_variant, win_archive_ext)
        macos_64 = eclipse_lwb_buildfarm_download(macos_64_variant, macos_archive_ext)
        linux_64 = eclipse_lwb_buildfarm_download(linux_64_variant, linux_archive_ext)
        windows_64 = eclipse_lwb_buildfarm_download(win_64_variant, win_archive_ext)
        windows_32 = eclipse_lwb_buildfarm_download(win_32_variant, win_archive_ext)
        eclipse_repo = buildfarm_download('dist/spoofax/eclipse/site/')
        eclipse_repo_archive = None
        intellij_update_site = buildfarm_download('dist/spoofax/intellij/plugin.zip')
        sunshine_jar = None
        spt_testrunner_jar = None
        spoofax_core_uber_jar = None
        strategoxt_distrib = buildfarm_download('dist/strategoxt/distrib.tar')
        strategoxt_jar = buildfarm_download('dist/strategoxt/strategoxt.jar')
    else:
        macos_64_jre = eclipse_lwb_artifacts_download(repo, macos_64_jre_variant, macos_archive_ext, download_version)
        linux_64_jre = eclipse_lwb_artifacts_download(repo, linux_64_jre_variant, linux_archive_ext, download_version)
        windows_64_jre = eclipse_lwb_artifacts_download(repo, win_64_jre_variant, win_archive_ext, download_version)
        windows_32_jre = eclipse_lwb_artifacts_download(repo, win_32_jre_variant, win_archive_ext, download_version)
        macos_64 = eclipse_lwb_artifacts_download(repo, macos_64_variant, macos_archive_ext, download_version)
        linux_64 = eclipse_lwb_artifacts_download(repo, linux_64_variant, linux_archive_ext, download_version)
        windows_64 = eclipse_lwb_artifacts_download(repo, win_64_variant, win_archive_ext, download_version)
        windows_32 = eclipse_lwb_artifacts_download(repo, win_32_variant, win_archive_ext, download_version)
        eclipse_repo = f'https://artifacts.metaborg.org/content/unzip/releases-unzipped/org/metaborg/org.metaborg.spoofax.eclipse.updatesite/{version}/org.metaborg.spoofax.eclipse.updatesite-{version}-assembly.zip-unzip/'
        eclipse_repo_archive = artifacts_download(repo, 'org.metaborg.spoofax.eclipse.updatesite',
                                                  classifier='assembly', packaging='zip', version=download_version)
        intellij_update_site = artifacts_download(repo, 'org.metaborg.intellij.dist', packaging='zip',
                                                  version=download_version)
        sunshine_jar = artifacts_download(repo, 'org.metaborg.sunshine2', version=download_version)
        spt_testrunner_jar = artifacts_download(repo, 'org.metaborg.spt.cmd', version=download_version)
        spoofax_core_uber_jar = artifacts_download(repo, 'org.metaborg.spoofax.core.uber', version=download_version)
        strategoxt_distrib = artifacts_download(repo, 'strategoxt-distrib', classifier='bin', packaging='tar',
                                                version=download_version)
        strategoxt_jar = artifacts_download(repo, 'strategoxt-jar', version=download_version)

    vars.release[env_version] = dict(
        date=date,
        version=version,
        eclipse=dict(
            install=dict(
                jvm=dict(
                    link=dict(
                        macos_64=download_link(macos_icon, "macOS 64-bit with embedded JVM", macos_64_jre),
                        linux_64=download_link(linux_icon, "Linux 64-bit with embedded JVM", linux_64_jre),
                        windows_64=download_link(windows_icon, "Windows 64-bit with embedded JVM", windows_64_jre),
                        windows_32=download_link(windows_icon, "Windows 32-bit with embedded JVM", windows_32_jre),
                    ),
                    macos_64=macos_64_jre,
                    linux_64=linux_64_jre,
                    windows_64=windows_64_jre,
                    windows_32=windows_32_jre,
                ), link=dict(
                    macos_64=download_link(macos_icon, "macOS 64-bit", macos_64_jre),
                    linux_64=download_link(linux_icon, "Linux 64-bit", linux_64_jre),
                    windows_64=download_link(windows_icon, "Windows 64-bit", windows_64_jre),
                    windows_32=download_link(windows_icon, "Windows 32-bit", windows_32_jre),
                ),
                macos_64=macos_64,
                linux_64=linux_64,
                windows_64=windows_64,
                windows_32=windows_32,
            ),
            repository=eclipse_repo,
            repository_archive=eclipse_repo_archive,
            repository_archive_link=f'[Eclipse update site archive]({eclipse_repo_archive})'
        ),
        intellij=dict(
            update_site=intellij_update_site,
            update_site_link=f'[IntelliJ update site archive]({intellij_update_site})'
        ),
        sunshine_jar=sunshine_jar,
        sunshine_jar_link=f'[Sunshine JAR]({sunshine_jar})',
        spt_testrunner_jar=spt_testrunner_jar,
        spt_testrunner_jar_link=f'[SPT testrunner JAR]({spt_testrunner_jar})',
        spoofax_core_uber_jar=spoofax_core_uber_jar,
        spoofax_core_uber_jar_link=f'[Spoofax Core Uber JAR]({spoofax_core_uber_jar})',
        spoofax_core_uber_jar_artifact=f'org.metaborg:org.metaborg.spoofax.core.uber:{download_version}',
        strategoxt_distrib=strategoxt_distrib,
        strategoxt_distrib_link=f'[Stratego/XT distribution]({strategoxt_distrib})',
        strategoxt_jar=strategoxt_jar,
        strategoxt_jar_link=f'[Stratego/XT JAR]({strategoxt_jar})',
    )


release_versions = {
    '2.5.16': '04-06-2021',
    '2.5.15': '11-05-2021',
    '2.5.14': '16-12-2020',
    '2.5.13': '20-11-2020',
    '2.5.12': '08-10-2020',
    '2.5.11': '17-07-2020',
    '2.5.10': '07-07-2020',
    '2.5.9': '08-05-2020',
    '2.5.8': '28-04-2020',
    '2.5.7': '26-06-2019',
    '2.5.6': '24-05-2019',
    '2.5.5': '23-05-2019',
    '2.5.4': '08-05-2019',
    '2.5.3': '02-05-2019',
    '2.5.2': '12-03-2019',
    '2.5.1': '02-10-2018',
    '2.5.0': '11-09-2018',
    '2.4.1': '29-01-2018',
    '2.4.0': '09-01-2018',
    '2.3.0': '29-09-2017',
    '2.2.1': '04-05-2017',
    '2.2.0': '18-04-2017',
    '2.1.0': '10-01-2017',
    '2.0.0': '08-07-2016',
    '2.0.0-beta1': '07-04-2016',
    '1.5.0': '18-12-2015',
    '1.4.0': '06-03-2015',
    '1.3.1': '09-12-2014',
    '1.3.0': '12-11-2014',
    '1.2.0': '13-08-2014',
    '1.1.0': '25-03-2013',
    '1.0.2': '15-02-2012',
    '1.0.0': '28-12-2011',
}
development_version = '2.6.0-SNAPSHOT'


def on_pre_page_macros(env):
    define_macros(env.conf['extra'])


def define_env(env):
    define_macros(env.variables)


def define_macros(vars):
    vars['warning'] = f"{warning_icon}{{.warning}}"
    vars['stop'] = f"{stop_icon}{{.stop}}"

    vars.os = dict(
        windows=f'{windows_icon} Windows',
        linux=f'{linux_icon} Linux',
        macos=f'{macos_icon} macOS'
    )
    vars.artifacts_releases = artifacts_releases_url
    vars.artifacts_releases_link = f'[artifact server]({artifacts_releases_url})'

    vars.release = {}
    for version, date in release_versions.items():
        fill_vars_with_release(vars, version, version, version, date)
    latest_rel_version, latest_rel_date = next(iter(release_versions.items()))
    fill_vars_with_release(vars, 'rel', latest_rel_version, latest_rel_version, latest_rel_date)
    fill_vars_with_release(vars, 'dev', development_version, "LATEST", None)

