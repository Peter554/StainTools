#!/bin/bash

while true; do
    echo "";
    read -p "This script will add modified files and commit them - is that Okay (y/n)? " go;
    if [ $go == "y" ] || [ $go == "yes" ]; then break; fi;
    if [ $go == "n" ] || [ $go == "no" ]; then exit; fi;
    echo "Sorry, I didn't recognize that. Try again."
done

while true; do
    echo "";
    read -p "Do you know your PyPI and GitHub credentials? - If not don't proceed! (y/n)? " go;
    if [ $go == "y" ] || [ $go == "yes" ]; then break; fi;
    if [ $go == "n" ] || [ $go == "no" ]; then exit; fi;
    echo "Sorry, I didn't recognize that. Try again.";
done

while true; do
    echo "";
    read -p "What type of release do you want to make (patch/minor/major)? " releasetype;
    if [ $releasetype == "patch" ] || [ $releasetype == "minor" ] || [ $releasetype == "major" ]; then break; fi;
    echo "Sorry, I didn't recognize that. Try again.";
done

echo "";
rm -rf ./dist;

# Just to be safe
echo "";
git add .;
echo "";
git commit -m 'About to bump version';

echo "";
bumpversion $releasetype;

echo "";
python setup.py sdist;

error="true";
while [ $error == "true" ]; do
    error="false";
    {
        echo "";
        twine upload ./dist/*;
    } || { 
        echo "";
        echo "Error uploading to PyPI. Did you enter the wrong credetials?";
        error="true";
    }
done

echo "";
rm -rf ./dist;

error="true";
while [ $error == "true" ]; do
    error="false";
    {
        echo "";
        git push;
    } || { 
        echo "";
        echo "Error pushing to GitHub. Did you enter the wrong credetials?";
        error="true";
    }
done

error="true";
while [ $error == "true" ]; do
    error="false";
    {
        echo "";
        git push --tags;
    } || { 
        echo "";
        echo "Error pushing tags to GitHub. Did you enter the wrong credetials?";
        error="true";
    }
done




