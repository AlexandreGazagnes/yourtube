#! /bin/bash


git push &&\
git checkout main &&\
git merge --no-ff dev --commit --no-edit &&\
git push &&\
git checkout dev