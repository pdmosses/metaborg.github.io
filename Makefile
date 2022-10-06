DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

ROOT         ?= $(DIR)
DOCKERFILE   ?= $(ROOT)/Dockerfile
PORT         ?= 8000

RESEARCHR    ?= metaborg-spoofax
BIB_FILE     ?= $(ROOT)/bibliographies/spoofax.bib

include $(ROOT)/Makefile.inc