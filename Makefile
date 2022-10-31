VERSION := 0.1.1

.PHONY: clean lint rpm

rpm: SOURCES/v$(VERSION).tar.gz
	@rpmbuild -ba --define "_topdir $$(pwd)" build-info.spec

SOURCES/v$(VERSION).tar.gz: SOURCES LICENSE yum-build-info.py dnf-build-info.py build-info.conf
	@tar czf SOURCES/v$(VERSION).tar.gz --transform='s,^,yum-plugin-build-info-$(VERSION)/,' LICENSE yum-build-info.py dnf-build-info.py build-info.conf

SOURCES:
	@mkdir -p SOURCES

clean:
	@rm -rf BUILD BUILDROOT RPMS SOURCES SPECS SRPMS

lint:
	@rpmlint build-info.py $$(find . -name \*.rpm)