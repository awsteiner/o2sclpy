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
	@echo "  html: Build the Sphinx docs"
	@echo "  statfiles: Generate the static doc files."
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
	rsync -Cavzu build/html/* $(STATIC_DOC_DIR)/o2sclpy

test-sync:
	rsync -Cavzun build/html/* $(STATIC_DOC_DIR)/o2sclpy

statfiles:
	cd static; o2graph -h | grep -v "Set o2scl" | \
		grep -v "Compiled at" > o2graph.help.txt
	cd static; ./backend.scr
	cd static; ./table3d_den_plot.scr
	cd static; ./table_errorbar.scr
	cd static; ./table_hist2dplot.scr
	cd static; ./table_histplot.scr
	cd static; ./table_plot.scr
	cd static; ./table_plotv.scr
	cd static; ./table_rplot.scr
	cd static; ./table_scatter.scr
