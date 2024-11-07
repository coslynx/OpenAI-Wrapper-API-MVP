#!/bin/bash

# Strict error handling
set -euo pipefail

# Environment setup
export PROJECT_ROOT=$(dirname "$0")
export LOG_FILE="$PROJECT_ROOT/logs/startup.log"
export PID_FILE="$PROJECT_ROOT/logs/app.pid"
export DATABASE_PORT=5432
export BACKEND_PORT=5000

# Utility functions
log_info() {
  echo "$(date +'%Y-%m-%d %H:%M:%S') - INFO - $*" >> "$LOG_FILE"
}

log_error() {
  echo "$(date +'%Y-%m-%d %H:%M:%S') - ERROR - $*" >&2
}

cleanup() {
  if [[ -f "$PID_FILE" ]]; then
    kill -9 $(cat "$PID_FILE") 2>/dev/null
    rm "$PID_FILE"
  fi
}

check_dependencies() {
  # Check if required tools are installed
  command -v pip >/dev/null 2>&1 || { log_error "pip is required. Install pip."; exit 1; }
  command -v python3 >/dev/null 2>&1 || { log_error "Python3 is required. Install Python3."; exit 1; }
  command -v gunicorn >/dev/null 2>&1 || { log_error "gunicorn is required. Install gunicorn."; exit 1; }
}

# Health checks
check_port() {
  local port="$1"
  nc -z localhost "$port" >/dev/null 2>&1
}

wait_for_service() {
  local service="$1"
  local port="$2"
  local timeout="$3"
  local start_time=$(date +%s)
  local elapsed_time=0
  while [[ "$elapsed_time" -lt "$timeout" ]]; do
    if check_port "$port"; then
      log_info "Service '$service' started on port '$port'"
      return 0
    fi
    sleep 1
    elapsed_time=$(( $(date +%s) - $start_time ))
  done
  log_error "Timeout waiting for service '$service' on port '$port'"
  exit 1
}

# Service management
start_database() {
  # Implement database startup logic
  log_info "Starting database service..."
  # Example for PostgreSQL:
  # sudo pg_ctl -D /var/lib/postgresql/data start
  wait_for_service "database" "$DATABASE_PORT" 60
}

start_backend() {
  # Implement backend server startup logic
  log_info "Starting backend server..."
  nohup gunicorn app:app --bind 0.0.0.0:"$BACKEND_PORT" --workers 2 &
  store_pid "$!"
  wait_for_service "backend" "$BACKEND_PORT" 60
}

store_pid() {
  local pid="$1"
  echo "$pid" > "$PID_FILE"
}

# Main execution flow
trap cleanup EXIT ERR
check_dependencies
start_database
start_backend
log_info "AI Powered OpenAI Request Wrapper MVP started successfully"