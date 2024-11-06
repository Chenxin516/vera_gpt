
.PHONY: black 8 flake clean

#8:
#	@autopep8 --aggressive --aggressive \
#		--recursive --in-place .

black:
	@black --line-length 79 .

flake:	
	@flake8 --exit-zero --statistics .

clean:
	@echo Removing:
	@find . | grep \
		-e "/__pycache__$$" \
		-e "/.DS_Store$$" \
		-e "/*.egg-info$$" \
	| bash -c 'tee >(xargs rm -rf)'
