clean:
	find . -name '*.pyc' -exec rm -fv {} \;
	find . -name '*~' -exec rm -fv {} \;
	find . -name '*#' -exec rm -fv {} \;

wipe:
	rm -f data/ml-data-100k/pickle.jar

stats:
	python predict.py stats | less

bias:
	python predict.py bias | less

item-based:
	python predict.py item-based | less