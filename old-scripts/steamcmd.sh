#!/bin/bash
podman run \
  --network=host \
  -v "$(pwd):/mnt" \
  --rm \
  -it \
  --name=steamcmd \
  ghcr.io/gehock/arma-reforger:latest \
  bash
