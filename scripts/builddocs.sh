#!/bin/bash
set -x

sudo apt-get update
sudo apt-get install -y git rsync ruby-full build-essential zlib1g-dev

pwd ls -lah
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)

##################
# Install Jekyll #
##################

echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

gem install jekyll bundler


#####################
# Build the website #
#####################

jekyll build

######################
# Deploy the website #
######################

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

docroot="mktemp -d"
rsync -av "_site" "${docroot}/"

pushd "${docroot}"

git init
git remote add deploy "https://token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
git checkout -b gh-pages

cat > README.md <<EOF

# README
This branch is a cache for the website served from https://RickGelhausen.github.io/webtests/ .

EOF


git add .

msg="Updating Website for commit ${GITHUB_SHA} made on `date --date="@${SOURCE_DATE_EPOCH}" --iso-8601=seconds` from {GITHUB_REF} by {GITHUB_ACTOR}"
git commit -am "${msg}"

# deploy to gh-pages
git push deploy gh-pages --force

popd

exit 0


