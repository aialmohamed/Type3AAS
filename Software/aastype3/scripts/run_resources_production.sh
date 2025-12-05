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
Simulators_PATH="$PROJECT_ROOT/Software/aastype3/Simulators"

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

# 1. Run the simulators (4 separate processes for drill and move)
run_agent "Drill Machine 1 (port 8090)" "$Simulators_PATH/DrillMachine1.py"
run_agent "MoveXY Machine 1 (port 8092)" "$Simulators_PATH/MoveXYMachine1.py"
run_agent "Drill Machine 2 (port 8091)" "$Simulators_PATH/DrillMachine2.py"
run_agent "MoveXY Machine 2 (port 8093)" "$Simulators_PATH/MoveXYMachine2.py"

# 2. Start Resource Agents first (they need to subscribe before CFP is sent)
run_agent "Resource Agent 1" "$BASE_PATH/Resource_Agent/Agent_Core/Resource_Agent.py"
run_agent "Resource Agent 2" "$BASE_PATH/Resource_Agent/Agent_Core/Resource_Agent_2.py"

# 3. Start Execution Core
run_agent "Execution Core" "$BASE_PATH/Prodcution_Agent/Agent_Core/Execution_Core/ExecutionCore.py"

# 4. Start Negotiation Core
run_agent "Negotiation Core" "$BASE_PATH/Prodcution_Agent/Agent_Core/Negotiation_Core/NegotiationCore.py"

# 5. Wait a bit for all agents to be ready
echo -e "${YELLOW}Waiting for agents to initialize...${NC}"
sleep 3

# 6. Start User Agent (entry point - triggers the workflow)
run_agent "User Agent" "$BASE_PATH/Prodcution_Agent/Agent_Core/agent_entrypoint.py"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  All agents started!${NC}"
echo -e "${GREEN}  Press Ctrl+C to stop all agents${NC}"
echo -e "${GREEN}========================================${NC}"

# Wait for all background processes
wait