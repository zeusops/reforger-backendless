podman run \
  --network=host \
  -v /opt/reforger/installation:/reforger \
  -v /opt/reforger/profile:/home/profile \
  -v $(pwd):/mnt \
  --rm \
  --name=reforger-nobackend \
  ghcr.io/gehock/arma-reforger:latest \
  /reforger/ArmaReforgerServer \
    $@
