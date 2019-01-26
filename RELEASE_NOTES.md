# Release Notes

- Remove any old dists 
``` bash
rm -rf ./dist
```

- Add and commit any unsaved changes with a generic commit message
```bash
git add .
git commit -m 'About to bump version'
```

- Bump the version (with $releasetype = 'patch', 'minor' or 'major') 
```bash
pipenv run bumpversion $releasetype
```

- Make the dist
```bash
pipenv run python setup.py sdist
```

- Upload to PyPI
```bash
pipenv run twine upload ./dist/*
```

- Clean up the dists
```bash
rm -rf ./dist
```
- Push to GitHub
```bash
git push
git push --tags
```




