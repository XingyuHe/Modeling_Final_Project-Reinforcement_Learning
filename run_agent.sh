#AGENT=$"scripts/configs/HighwayEnv/agents/MCTSAgent/baseline.json"
AGENT="scripts/configs/HighwayEnv/agents/DQNAgent/dqn.json"
ENV="scripts/configs/HighwayEnv/env.json"

python3 scripts/experiments.py evaluate $ENV $AGENT --train