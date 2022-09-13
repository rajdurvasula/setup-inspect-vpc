#!/bin/bash -x
aws s3 cp src/inspectionvpc_nfw_provider.yaml s3://sh-network-dev-bucket1/
aws s3 cp src/calc_cidr.zip s3://sh-network-dev-bucket1/
aws s3 cp src/retrieve_vpceids.zip s3://sh-network-dev-bucket1/
