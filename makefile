build: build-init build-features build-train build-visualization

build-init:
	brane import TISNN/brane-setup
build-features:
	brane import TISNN/brane-getfeatures
build-train:
	brane import TISNN/brane-trainandpredict
build-visualization:
	brane import TISNN/brane-visualization