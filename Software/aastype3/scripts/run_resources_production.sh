#!/bin/bash

# Run all agents for the production system
# Usage: ./run_resources_production.sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base paths
PROJECT_ROOT="/home/ahmed/Thesis/Type3AAS"
VENV_PATH="$PROJECT_ROOT/.venv"
BASE_PATH="$PROJECT_ROOT/Software/aastype3/Core"

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"

# Function to run agent in background
run_agent() {
    local name=$1
    local path=$2
    echo -e "${GREEN}Starting $name...${NC}"
    python "$path" &
    sleep 2  # Give each agent time to start
}

# Trap to kill all background processes on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down all agents...${NC}"
    pkill -P $$
    deactivate 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Starting Production System Agents${NC}"
echo -e "${GREEN}========================================${NC}"
# 1. run the invokers : 
run_agent "Drill Invoker" "$BASE_PATH/Submodels_base/Resource_Base/invokers/DrillInvoker.py"
run_agent "Movement Invoker" "$BASE_PATH/Submodels_base/Resource_Base/invokers/MoveXYInvoker.py"


# 1. Start Resource Agents first (they need to subscribe before CFP is sent)
run_agent "Resource Agent 1" "$BASE_PATH/Resource_Agent/Agent_Core/Resource_Agent.py"
run_agent "Resource Agent 2" "$BASE_PATH/Resource_Agent/Agent_Core/Resource_Agent_2.py"

# 2. Start Execution Core
run_agent "Execution Core" "$BASE_PATH/Prodcution_Agent/Agent_Core/Execution_Core/ExecutionCore.py"

# 3. Start Negotiation Core
run_agent "Negotiation Core" "$BASE_PATH/Prodcution_Agent/Agent_Core/Negotiation_Core/NegotiationCore.py"

# 4. Wait a bit for all agents to be ready
echo -e "${YELLOW}Waiting for agents to initialize...${NC}"
sleep 3

# 5. Start User Agent (entry point - triggers the workflow)
run_agent "User Agent" "$BASE_PATH/Prodcution_Agent/Agent_Core/agent_entrypoint.py"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  All agents started!${NC}"
echo -e "${GREEN}  Press Ctrl+C to stop all agents${NC}"
echo -e "${GREEN}========================================${NC}"

# Wait for all background processes
wait