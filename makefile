build: build-init build-features build-train build-visualization

build-init:
	brane import TISNN/brane-setup && brane push init
build-features:
	brane import TISNN/brane-getfeatures && brane push getfeatures
build-train:
	brane import TISNN/brane-trainandpredict && brane push train_predict
build-visualization:
	brane import TISNN/brane-visualization && brane push visual