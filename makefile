n ?= 10

start-localstack:
	mkdir teste-content
	mkdir teste-content/folder-01

	n=$(n); \
	while [ $${n} -gt 0 ] ; do \
		touch teste-content/file-$$n.txt ; \
		touch teste-content/folder-01/file-$$n.txt ; \
		n=`expr $$n - 1`; \
	done; \
	true

	aws --endpoint-url=http://localhost:4566 s3 mb s3://mybucket-1
	aws --endpoint-url=http://localhost:4566 s3 mb s3://mybucket-2
	aws --endpoint-url=http://localhost:4566 s3 cp teste-content s3://mybucket-1/ --recursive

	rm -r teste-content
