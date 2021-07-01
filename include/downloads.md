{% macro downloads(version) -%}
## Downloads

### Eclipse plugin

#### Premade Eclipse installations

With embedded JRE:

* {{ release[version].eclipse.install.jvm.link.macos_64 }}
* {{ release[version].eclipse.install.jvm.link.linux_64 }}
* {{ release[version].eclipse.install.jvm.link.windows_64 }}
* {{ release[version].eclipse.install.jvm.link.windows_32 }}

Without embedded JRE:

* {{ release[version].eclipse.install.link.macos_64 }}
* {{ release[version].eclipse.install.link.linux_64 }}
* {{ release[version].eclipse.install.link.windows_64 }}
* {{ release[version].eclipse.install.link.windows_32 }}

#### Update site

* Eclipse update site: `{{ release[version].eclipse.repository }}`
* {{release[version].eclipse.repository_archive_link}}

### IntelliJ plugin

* IntelliJ update site: `{{ release[version].intellij.update_site }}`
* {{release[version].intellij.update_site_link}}

### Command-line utilities

* {{release[version].sunshine_jar_link}}
* {{release[version].spt_testrunner_jar_link}}

### Core API

* {{release[version].spoofax_core_uber_jar_link}}
* Spoofax Core uber Maven artifact: `{{release[version].spoofax_core_uber_jar_artifact}}`

### StrategoXT

* {{release[version].strategoxt_distrib_link}}
* {{release[version].strategoxt_jar_link}}

### Maven artifacts

Maven artifacts can be found on our {{artifacts_releases_link}}.
The Maven version used for this release is `{{release[version].version}}`.
{%- endmacro %}
