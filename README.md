# AeroEdge: Autonomous Multimodal Edge-Swarm for Remote Environmental Monitoring

## Overview
AeroEdge is an intelligent edge AI monitoring system designed for remote environmental monitoring in low-connectivity environments. This system processes environmental sensor data on edge devices and sends critical alerts back to a central dashboard, solving the "Edge AI Bottleneck" problem.

## System Architecture

### Core Components
1. **Sensor Data Aggregator** - Collects and processes video and environmental sensor data
2. **Edge AI Processor** - Executes lightweight AI models for on-device inference
3. **Alert System** - Generates and transmits critical alerts to central dashboard
4. **Main Controller** - Coordinates all components and manages system lifecycle

### Technical Approach
- **Model Optimization**: Uses 8-bit quantized models for low-power execution
- **Multimodal Fusion**: Combines video frame analysis with environmental sensor data
- **Edge Computing**: Processes data locally to minimize bandwidth usage
- **MCP Integration**: Leverages existing ModelScope and other MCP servers

## Directory Structure
```
edge-ai/
├── sensor_processor.py          # Sensor data aggregation and fusion
├── edge_inference.py           # Lightweight AI model execution
├── alert_system.py             # Alert generation and transmission
├── main.py                     # System entry point
├── launcher.sh                 # System startup script
├── models/                     # Local model storage
├── config/                     # Configuration files
├── utils/                      # Helper utilities
└── logs/                       # System logs
```

## Prerequisites
- Python 3.13+
- Git
- SSH access to GitHub (for MCP integration)
- Edge device with sufficient compute resources

## Quick Start

### Installation
```bash
# Make launcher executable
chmod +x launcher.sh

# Run system in test mode to verify setup
./launcher.sh test
```

### Running the System
```bash
# Start the monitoring system
./launcher.sh start

# Run in test mode (single cycle)
./launcher.sh test

# Check system status
./launcher.sh status

# Stop the system
./launcher.sh stop

# Validate system setup
./launcher.sh validate
```

## Key Features

### Model Integration
- Leverages existing ModelScope MCP server configuration
- Supports 8-bit quantized model execution
- Implements model versioning and update mechanisms

### Data Processing
- Multimodal data fusion (video + sensor data)
- Adaptive sampling rates based on conditions
- Data validation and sanitization

### Reliability
- Graceful error handling and recovery
- Circuit breaker patterns for external services
- Secure data transmission

## Configuration

### Environment Variables
Set these in your environment or create a `.env` file:
- `MODELSCOPE_API_KEY` - For ModelScope access
- `DASHBOARD_URL` - Central dashboard endpoint
- `LOG_LEVEL` - Logging verbosity (DEBUG/INFO/WARNING/ERROR)

### Config Files
- `config/sensor_config.json` - Sensor data collection settings
- `config/model_config.json` - Model execution parameters
- `config/alert_config.json` - Alert generation criteria

## Testing

### Unit Tests
```bash
# Run basic validation
./launcher.sh validate
```

### Integration Tests
```bash
# Test with simulated data
./launcher.sh test
```

## Safety Considerations

- Follows existing repository safety guidelines
- No data deletion or modification of critical system files
- Implements graceful degradation during failures
- Uses only read-only diagnostics where possible

## Maintenance

### Model Updates
- Automatic model update mechanism
- Version control through git integration
- Backup model switching capability

### Monitoring
- System status logging
- Performance metrics collection
- Alert history tracking

## Troubleshooting

### Common Issues
1. **Model Loading Failures**: Check ModelScope configuration in MCP settings
2. **Sensor Communication**: Verify sensor connections and permissions
3. **Network Issues**: Ensure central dashboard endpoint is reachable
4. **Resource Constraints**: Monitor memory and CPU usage on edge device

### Diagnostic Commands
```bash
# Check system status
./launcher.sh status

# View logs
tail -f logs/system.log

# Validate configuration
./launcher.sh validate
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
MIT License - see LICENSE file for details

## Acknowledgments
- Built upon existing repository infrastructure and patterns
- Leverages ModelScope and MCP integration capabilities
- Follows device management safety practices from the parent project