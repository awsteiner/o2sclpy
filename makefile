help:
	@echo "This the O2sclpy root directory makefile. It is not intended"
	@echo "for the end-user. Use 'python setup.py' for standard "
	@echo "package setup and installation."
	@echo "-------------------------------------------------------------"
	@echo "Developer targets:"
	@echo "doc:       Make the documentation (requires sphinx & breathe)"
	@echo "sync-doc:  Copies documentation to webserver"
	@echo "test-sync:"
	@echo "reinstall: Reinstall o2sclpy using pip3"
	@echo "statfiles: Make the images and extra files for the docs"
	@echo
	@echo "-------------------------------------------------------------"
	@echo "Notes: to upload to pypi run 'rm dist/*',"
	@echo "'python3 setup.py sdist bdist_wheel'"
	@echo "  and then 'twine upload dist/*'."

doc: .empty
	cd doc; $(MAKE) html

sync-doc:
	cd doc; $(MAKE) sync-doc

test-sync:
	cd doc; $(MAKE) test-sync

ifeq ($(MACHINE),isospin)
PIP3_CMD = sudo pip3
else
PIP3_CMD = pip3 
endif

reinstall:
	-$(PIP3_CMD) uninstall -y o2sclpy
	$(PIP3_CMD) install .

.empty:

yt-test1:
	o2graph -backend Agg -set verbose 2 -create tensor_grid 3 10 10 10 \
		-entry 1 1 1 -function "i0*sin(i1)*i2" -entry 1 1 1 \
		-yt-add-vol -yt-render test.png

yt-test2:
	o2graph -backend Agg -set verbose 2 -create tensor_grid 3 10 10 10 \
		-entry 1 1 1 -function "i0*sin(i1)*i2" -entry 1 1 1 \
		-yt-add-vol \
		-clear -create tensor_grid 3 10 10 10 \
		-entry 1 1 1 -function "i0*cos(i1)*i2" -entry 1 1 1 \
		-yt-add-vol -yt-render test.png

statfiles:
	cd doc; $(MAKE) statfiles
