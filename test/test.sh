# Run tests and then show coverage report (only if no errors):
python -m coverage run --source="." -m unittest discover -s test -v || exit

python -m coverage report -m --skip-covered --omit="test/*.py,setup.py"
