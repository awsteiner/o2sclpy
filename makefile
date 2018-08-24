help:
	@echo "doc"
	@echo "sync-doc"
	@echo "reinstall"
	@echo "to upload to pypi run 'rm dist/*',"
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
