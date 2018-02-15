# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = 
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = o2sclpy
SOURCEDIR     = .
BUILDDIR      = build

help:
	@echo
	@echo "Standard targets:"
	@echo "----------------------------------------------------"
	@echo "  help: Show this list"
	@echo "  sphinx-help: Show the list of Sphinx commands"
	@echo "  help.txt: Generate the help.txt file for the docs"
	@echo "  html: Build the Sphinx docs"
	@echo "  sync-doc: Copy to server"
	@echo "  all: help.txt, html, and sync-doc in that order"
	@echo "----------------------------------------------------"
	@echo

# Put it first so that "make" without argument is like "make help".
sphinx-help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

all:
	$(MAKE) help.txt
	$(MAKE) html
	$(MAKE) sync-doc

sync-doc:
	cp -r build/html/* $(STATIC_DOC_DIR)/o2sclpy

help.txt:
	cd static; o2graph -h | grep -v "Set o2scl" > o2graph.help.txt
