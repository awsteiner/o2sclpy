help:
	@echo "This the O2sclpy root directory makefile. It is not intended"
	@echo "for the end-user. Use 'python setup.py' for standard "
	@echo "package setup and installation."
	@echo "-------------------------------------------------------------"
	@echo "Developer targets:"
	@echo "doc:       Make the documentation (requires sphinx & breathe)"
	@echo "test:      Test the library"
	@echo "sync-doc:  Copies documentation to webserver"
	@echo "open-doc:  Open local documentation in browser"
	@echo "web-doc:   Open web documentation in browser (after sync-doc)"
	@echo "test-sync:"
	@echo "reinstall: Reinstall o2sclpy using pip3"
	@echo "statfiles: Make the images and extra files for the docs"
	@echo "           (to be run before 'make doc')"
	@echo
	@echo "-------------------------------------------------------------"
	@echo "Notes: to upload to pypi run 'rm dist/*',"
	@echo "'python3 setup.py sdist bdist_wheel'"
	@echo "  and then 'twine upload dist/*'."

BROWSER = 
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    BROWSER += open
else
    BROWSER += xdg-open
endif

open-doc: .empty
	$(BROWSER) doc/build/html/index.html

web-doc: .empty
	$(BROWSER) "https://neutronstars.utk.edu/code/o2sclpy"

doc: .empty
	cd doc/static; o2graph -h | grep -v "Set o2scl" | \
		grep -v "Compiled at" | grep -v "New alias" > o2graph.help.txt
	cd doc/static/examples; $(MAKE) skyrme.ipynb
	cd static/examples; $(MAKE) skyrme.ipynb

sync-doc:
	cd doc; $(MAKE) sync-doc

test-sync:
	cd doc; $(MAKE) test-sync

test:
	cd doc/static/examples; jupytext --set-kernel python3 \
		--execute skyrme.py
	pytest o2sclpy/test doc/static/examples/skyrme.py -s -v

ifeq ($(MACHINE),isospin)
PIP3_CMD = sudo pip3
else
PIP3_CMD = pip3 
endif

reinstall:
	-$(PIP3_CMD) uninstall -y o2sclpy
	$(PIP3_CMD) install .

.empty:

statfiles:
	cd doc; $(MAKE) statfiles
