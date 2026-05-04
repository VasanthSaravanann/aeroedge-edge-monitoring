#!/bin/bash

# AeroEdge System Launcher Script
# Launches the edge AI monitoring system

# Exit on any error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if required commands exist
check_dependencies() {
    print_status "Checking dependencies..."

    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi

    # Check if we're in the right directory
    if [[ ! -f "main.py" ]]; then
        print_error "This script must be run from the edge-ai directory"
        exit 1
    fi

    print_status "All dependencies satisfied"
}

# Function to setup virtual environment (if needed)
setup_virtual_env() {
    if [[ ! -d ".venv" ]]; then
        print_status "Creating virtual environment..."
        python3 -m venv .venv
        source .venv/bin/activate

        # Install requirements if they exist
        if [[ -f "requirements.txt" ]]; then
            pip install -r requirements.txt
        fi
    else
        print_status "Virtual environment already exists"
    fi
}

# Function to create log directory
setup_logging() {
    mkdir -p logs
    print_status "Log directory ready"
}

# Function to validate configuration
validate_config() {
    print_status "Validating system configuration..."

    # Check if config directory exists
    if [[ ! -d "config" ]]; then
        print_warning "Config directory not found, creating empty directory"
        mkdir -p config
    fi

    # Check if model directory exists
    if [[ ! -d "models" ]]; then
        print_warning "Models directory not found, creating empty directory"
        mkdir -p models
    fi

    # Validate configuration files exist
    if [[ ! -f "config/sensor_config.json" ]]; then
        print_warning "Sensor config not found, creating default"
        cat > config/sensor_config.json << EOF
{
    "sensor_types": ["camera", "temperature", "humidity", "pressure", "light", "motion"],
    "sampling_rates": {
        "camera": 10,
        "temperature": 60,
        "humidity": 60,
        "pressure": 60,
        "light": 30,
        "motion": 5
    },
    "data_validation": {
        "enabled": true,
        "thresholds": {
            "temperature_min": -40,
            "temperature_max": 85,
            "humidity_min": 0,
            "humidity_max": 100
        }
    }
}
EOF
    fi

    if [[ ! -f "config/model_config.json" ]]; then
        print_warning "Model config not found, creating default"
        cat > config/model_config.json << EOF
{
    "model_paths": {
        "local": "./models/",
        "remote": "https://mcp.api-inference.modelscope.ai/"
    },
    "model_format": "onnx",
    "quantization": {
        "bits": 8,
        "type": "uint8"
    },
    "optimization": {
        "enabled": true,
        "target_device": "edge",
        "memory_limit_mb": 50
    },
    "inference_settings": {
        "batch_size": 1,
        "precision": "fp32",
        "thread_count": 2
    }
}
EOF
    fi

    if [[ ! -f "config/alert_config.json" ]]; then
        print_warning "Alert config not found, creating default"
        cat > config/alert_config.json << EOF
{
    "alert_severity": {
        "LOW": {
            "min_confidence": 0.0,
            "max_confidence": 0.3,
            "min_risk": 0,
            "max_risk": 1
        },
        "MODERATE": {
            "min_confidence": 0.3,
            "max_confidence": 0.6,
            "min_risk": 1,
            "max_risk": 2
        },
        "HIGH": {
            "min_confidence": 0.6,
            "max_confidence": 0.8,
            "min_risk": 2,
            "max_risk": 3
        },
        "CRITICAL": {
            "min_confidence": 0.8,
            "max_confidence": 1.0,
            "min_risk": 3,
            "max_risk": 4
        }
    },
    "transmission": {
        "retry_attempts": 3,
        "retry_delay_seconds": 30,
        "max_queue_size": 100
    },
    "filters": {
        "min_anomaly_score": 0.1,
        "time_window_minutes": 5
    }
}
EOF
    fi

    print_status "Configuration validation complete"
}

# Function to run system in different modes
run_system() {
    local mode="$1"

    case "$mode" in
        "start")
            print_status "Starting AeroEdge system..."
            python3 main.py "$@"
            ;;
        "test")
            print_status "Running system in test mode..."
            python3 main.py --test "$@"
            ;;
        "status")
            print_status "Checking system status..."
            if pgrep -f "main.py" > /dev/null; then
                echo "AeroEdge system is running"
            else
                echo "AeroEdge system is not running"
            fi
            ;;
        "stop")
            print_status "Stopping AeroEdge system..."
            pkill -f "main.py" 2>/dev/null || true
            echo "System stopped"
            ;;
        "validate")
            print_status "Validating system setup..."
            python3 -c "import sensor_processor; import edge_inference; import alert_system; print('All modules imported successfully')"
            echo "System validation complete"
            ;;
        "test-unit")
            print_status "Running unit tests..."
            python3 test_unit.py
            ;;
        *)
            print_error "Unknown mode: $mode"
            echo "Usage: $0 {start|test|status|stop|validate|test-unit}"
            exit 1
            ;;
    esac
}

# Main execution
main() {
    # Parse arguments
    if [[ $# -eq 0 ]]; then
        echo "AeroEdge System Launcher"
        echo "Usage: $0 {start|test|status|stop|validate|test-unit}"
        echo ""
        echo "Commands:"
        echo "  start    - Start the monitoring system"
        echo "  test     - Run in test mode"
        echo "  status   - Check system status"
        echo "  stop     - Stop the monitoring system"
        echo "  validate - Validate system setup"
        echo "  test-unit - Run unit tests"
        exit 1
    fi

    # Check dependencies
    check_dependencies

    # Setup
    setup_logging
    validate_config

    # Run specified command
    run_system "$1"
}

# Execute main function with all arguments
main "$@"