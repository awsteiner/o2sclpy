help:
	@echo "This the O2sclpy root directory makefile."
	@echo "-------------------------------------------------------------"
	@echo "doc:       Make the documentation (requires sphinx & breathe)"
	@echo "sync-doc:  Copies documentation to webserver"
	@echo "reinstall: Reinstall o2sclpy using pip3"
	@echo
	@echo "-------------------------------------------------------------"
	@echo "Other notes: to upload to pypi run 'rm dist/*',"
	@echo "'python3 setup.py sdist bdist_wheel'"
	@echo "  and then 'twine upload dist/*'."

doc: .empty
	cd doc; $(MAKE) html

sync-doc:
	cd doc; $(MAKE) sync-doc

reinstall:
	-pip3 uninstall -y o2sclpy
	pip3 install .

.empty:
