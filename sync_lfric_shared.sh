#!/bin/bash

cd $(dirname $0)

# Define source and destination directories
LFRIC_SPACK_SRC=/work/n02/n02/jwc/software/spack/lfric_shared_build/lfric-spack
SIMIT_SPACK_SRC=/work/n02/n02/jwc/software/spack/lfric_shared_build/simit-spack
LFRIC_SPACK_DEST=/work/y07/shared/lfric/software/spack/lfric-spack
SIMIT_SPACK_DEST=/work/y07/shared/lfric/software/spack/simit-spack

rsync -av --exclude "install/*" --exclude "envs/mirror/*" --exclude "envs/.spack-env/" --exclude "*__pycache__" --exclude "slurm-*.out" $LFRIC_SPACK_SRC/ $LFRIC_SPACK_DEST
rsync -av --exclude "*__pycache__" $SIMIT_SPACK_SRC/ $SIMIT_SPACK_DEST
