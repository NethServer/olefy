DEVTOOLS := $(shell dnf install -y rpmdevtools git python3-pip gcc gcc-c++ cpio tar xz which make gzip util-linux python3-devel libffi-devel openssl-devel)
SOURCE0 := $(shell spectool -s 0 $(spec) | cut -d ' ' -f 2)
SOURCE12 := $(shell spectool -s 12 $(spec) | cut -d ' ' -f 2)
PREFIX := $(shell basename $(SOURCE0) .tar.gz)

srpm:
	spectool -g $(spec)
	git archive --format=tar --prefix=$(PREFIX)/ HEAD | gzip > $(PREFIX).tar.gz
	pip3 download --no-binary=:all: -r requirements.txt -d .
	sha1sum -c SHA1SUM
	rpmbuild -D "_sourcedir $$PWD" -D "_srcrpmdir $$PWD" -bs $(spec)
	cp $$PWD/*.src.rpm $(outdir)