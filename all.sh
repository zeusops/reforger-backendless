CONFIG="${CONFIG:-/opt/reforger/installation/Configs/config.json}"
addons="$(jq -r '.game.mods[].modId' $CONFIG | tr '\n' ',')"
if [ "$1" = "-addons" ]; then
  echo $addons
  exit
fi
scenario_id="$(jq -r .game.scenarioId $CONFIG)"
podman run \
  --network=host \
  -v /opt/reforger/installation:/reforger \
  -v /opt/reforger/profile:/home/profile \
  --rm \
  --name=reforger-nobackend \
  ghcr.io/zeusops/arma-reforger:latest \
  /reforger/ArmaReforgerServer \
    -bindIP 0.0.0.0 \
    -bindPort 2001 \
    -noSound \
    -maxFPS 60 \
    -logLevel normal \
    -logStats 60000 \
    -adminPassword salasana \
    -profile /home/profile \
    -addons "$addons" \
    -addonsDir /reforger/workshop/addons \
    -server worlds/NoBackendScenarioLoader.ent \
    -scenarioId "$scenario_id" \
    $@
