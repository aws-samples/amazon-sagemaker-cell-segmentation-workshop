all: build-MyLayer

build-CellSegmentationLayer:
	rm -rf "$(ARTIFACTS_DIR)/python"
	mkdir -p "$(ARTIFACTS_DIR)/python"
	echo $(ARTIFACTS_DIR)
	cp requirements.txt $(ARTIFACTS_DIR)/python
	python3.7 -m pip install -r requirements.txt -t $(ARTIFACTS_DIR)/python
	rm -rf $(ARTIFACTS_DIR)/python/bin

build-CellSegmentationFunction:
	#mkdir -p "./python"
	cp requirements.txt $(ARTIFACTS_DIR)
	python3.7 -m pip3 install -r requirements.txt -t $(ARTIFACTS_DIR)
	rm -rf $(ARTIFACTS_DIR)/bin

