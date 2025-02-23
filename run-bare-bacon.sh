podman run \
  --network=host \
  -v /opt/reforger/installation:/reforger \
  -v /opt/reforger/profile:/home/profile \
  --rm \
  --name=reforger-nobackend \
  ghcr.io/gehock/arma-reforger:latest \
  /reforger/ArmaReforgerServer \
    -adminPassword salasana \
    -addons 6324F7124A9768FB,5AB890B71D748750 \
    -addonsDir /reforger/workshop/addons \
    -profile /home/profile \
    -server worlds/NoBackendScenarioLoader.ent \
    -scenarioId {ECC61978EDCC2B5A}Missions/23_Campaign.conf \
    -bindIP 0.0.0.0 \
    -bindPort 2001 \
    -maxFPS 60 \
    -logLevel normal \
    -logStats 60000
