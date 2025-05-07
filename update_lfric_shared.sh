#!/bin/bash

cd $(dirname $0)

# Define source and destination directories
LFRIC_SPACK_SRC=/work/n02/n02/jwc/software/spack/lfric_shared_build/lfric-spack
SIMIT_SPACK_SRC=/work/n02/n02/jwc/software/spack/lfric_shared_build/simit-spack
LFRIC_SPACK_DEST=/work/y07/shared/lfric/software/spack/lfric-spack
SIMIT_SPACK_DEST=/work/y07/shared/lfric/software/spack/simit-spack

rsync -av --exclude "install/*" --exclude "envs/mirror/*" --exclude "envs/.spack-env/" --exclude "*__pycache__" --exclude "slurm-*.out" $LFRIC_SPACK_SRC/ $LFRIC_SPACK_DEST
rsync -av --exclude "*__pycache__" $SIMIT_SPACK_SRC/ $SIMIT_SPACK_DEST

cd $LFRIC_SPACK_DEST
module use ./modules
module load lfric-spack
module list

spack -V
env | grep SPACK_U
spack repo list
spack find -c

# install packages from build cache
LFRIC_SPACK_MIRROR=$LFRIC_SPACK_SRC/envs/mirror
spack mirror set-url lfric-spack-mirror $LFRIC_SPACK_MIRROR
spack mirror list

# Make sure install_tree has no padding for lfric shared install
spack config add config:install_tree:padded_length:false

module load PrgEnv-gnu
spack install -v --no-check-signature --cache-only %gcc@11
spack find -c

#module load PrgEnv-cray
#spack install -v --no-check-signature --cache-only %cce@15
#spack find -c
