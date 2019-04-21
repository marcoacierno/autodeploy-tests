prepare-release:
	python scripts2/prepare_release.py

tag-release:
	python scripts2/tag_release.py

publish-changes:
	python scripts2/publish_changes.py

check-has-release:
	python scripts2/has_release.py

install-deploy-deps:
	pip install githubrelease
