podman run \
  --network=host \
  -v /opt/reforger/installation:/reforger \
  -v /opt/reforger/profile:/home/profile \
  --rm \
  --name=reforger-nobackend \
  ghcr.io/gehock/arma-reforger:latest \
  /reforger/ArmaReforgerServer \
    -bindIP 0.0.0.0 \
    -bindPort 2001 \
    -maxFPS 60 \
    -logLevel normal \
    -logStats 60000 \
    -adminPassword salasana \
    -profile /home/profile \
    -server worlds/GameMaster/GM_Arland.ent \
