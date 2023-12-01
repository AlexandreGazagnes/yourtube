#! /bin/bash


git push &&\
git checkout main &&\
git merge --no-ff dev &&\
git push &&\
git checkout dev