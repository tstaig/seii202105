#! /bin/bash
source /scripts/acs.env
cd $WORKDIR
MAKE_PARS="-j 4" make build
