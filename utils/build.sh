# Clean before, just in case:
rm -rf dist/ build/ logworks.egg-info/ src/logworks.egg-info/

# Build:
python setup.py sdist bdist_wheel

# Upload to test/real PyPI, if requested:
if [[ "x$1" == "xtest" ]]; then
    twine upload --repository test dist/*
fi

if [[ "x$1" == "xpypi" ]]; then
    twine upload --repository pypi dist/*
fi

# Clean after:
rm -rf dist/ build/ logworks.egg-info/ src/logworks.egg-info/
