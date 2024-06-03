VERSION=0.1.0

.PHONY: build
build:
	docker build --tag sirianni/screenlogic-exporter .

publish: build
	docker tag sirianni/screenlogic-exporter sirianni/screenlogic-exporter:$(VERSION)
	docker push sirianni/screenlogic-exporter:$(VERSION)
	docker push sirianni/screenlogic-exporter:latest