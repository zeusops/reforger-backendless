ADDONS="$(jq -r '.game.mods[].modId' /opt/reforger/installation/Configs/config.json | tr '\n' ',')"
if [ "$1" = "-addons" ]; then
  echo $ADDONS
  exit
fi
SCENARIO_ID="$(jq -r .game.scenarioId /opt/reforger/installation/Configs/config.json)"
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
    -noSound \
    -maxFPS 60 \
    -logLevel normal \
    -logStats 60000 \
    -adminPassword salasana \
    -profile /home/profile \
    -addons "$ADDONS" \
    -addonsDir /reforger/workshop/addons \
    -server worlds/NoBackendScenarioLoader.ent \
    -scenarioId "$SCENARIO_ID" \
    $@
