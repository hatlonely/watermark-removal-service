APP_NAME=watermark-removal-service

base-image:
	docker build -t $(APP_NAME)-base -f docker/Dockerfile.base .
