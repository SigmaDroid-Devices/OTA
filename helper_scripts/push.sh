# after copying the JSON and changelog to vendor/OTA
cd vendor/OTA
git fetch --all
 # checkout the sigma-14.3 branch after fetching the latest changes
git checkout sigma-devices/sigma-14.3
# delete the local copy of the sigma-14.3 branch
git branch -D sigma-14.3
# create a new local branch named sigma-14.3 based on the remote branch and change to it
git checkout -b sigma-14.3
# add the JSON and changelog to the local branch
git add .
# commit the changes (add the commit message in the editor and then save and close the editor)
git commit -as
# push the changes to the remote branch
git push sigma-devices sigma-14.3