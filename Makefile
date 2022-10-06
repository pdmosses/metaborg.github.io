DIR := $(patsubst %/,%,$(dir $(abspath $(lastword ${MAKEFILE_LIST}))))

# The directory where mkdocs.yml lives
ROOT         ?= ${DIR}
# The path to the Dockerfile
DOCKERFILE   ?= ${ROOT}/Dockerfile
# The port on which to serve the documentation on localhost
PORT         ?= 8000
# The path to the tools/ directory, relative to ${ROOT}
TOOLS        ?= tools/
# The path to the mkdocs_requirements.txt file, relative to ${ROOT}
REQUIREMENTS ?= mkdocs_requirements.txt
# The Researchr bibliography to get
RESEARCHR    ?= metaborg-spoofax
# The path to where the Researchr bibliography should be stored
BIB_FILE     ?= $(ROOT)/bibliographies/spoofax.bib
# The path where Makefile.inc lives
include ${ROOT}/Makefile.inc
