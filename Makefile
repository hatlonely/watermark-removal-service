APP_NAME=watermark-removal-service

image:
	docker build -t $(APP_NAME) -f docker/Dockerfile .

base-image:
	docker build -t $(APP_NAME)-base -f docker/Dockerfile.base .

.PHONY: dev-env
dev-env:
	docker run -d -v ${PWD}:/root/watermark-removal-service --rm docker.io/library/watermark-removal-service-base tail -f /dev/null

.PHONY: run
run:
	docker run --rm -p 8000:8000 docker.io/library/watermark-removal-service
