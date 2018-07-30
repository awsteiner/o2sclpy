doc:
	cd doc; $(MAKE) html

sync-doc:
	cd doc; $(MAKE) sync-doc

reinstall:
	-pip3 uninstall -y o2sclpy
	pip3 install .
