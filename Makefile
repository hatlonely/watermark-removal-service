APP_NAME=watermark-removal-service

base-image:
	docker build -t $(APP_NAME)-base -f docker/Dockerfile.base .

.PHONY: dev-env
dev-env:
	docker run -d -v ${PWD}:/root/watermark-removal-service --rm docker.io/library/watermark-removal-service-base tail -f /dev/null
