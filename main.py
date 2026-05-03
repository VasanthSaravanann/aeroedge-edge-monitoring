#!/usr/bin/env python3
"""
Main Entry Point for AeroEdge System
Coordinates all components of the edge AI monitoring system.
"""

import logging
import time
import argparse
from sensor_processor import SensorDataAggregator
from edge_inference import EdgeAIProcessor
from alert_system import AlertSystem

def setup_logging(log_level: int = logging.INFO):
    """Setup logging configuration"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/system.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main execution function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AeroEdge Edge AI Monitoring System')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(log_level)

    logger = logging.getLogger(__name__)

    logger.info("Starting AeroEdge System")

    try:
        # Initialize components
        logger.info("Initializing system components...")

        sensor_aggregator = SensorDataAggregator()
        ai_processor = EdgeAIProcessor()
        alert_system = AlertSystem()

        # Load AI model
        logger.info("Loading AI model...")
        if not ai_processor.load_model():
            logger.error("Failed to load AI model. Exiting.")
            return False

        # Validate model
        logger.info("Validating AI model...")
        if not ai_processor.validate_model():
            logger.error("Model validation failed. Exiting.")
            return False

        # Main processing loop
        logger.info("Starting main processing loop...")

        if args.test:
            logger.info("Running in test mode")
            # Run a single test cycle
            run_single_cycle(sensor_aggregator, ai_processor, alert_system)
        else:
            # Continuous monitoring loop
            while True:
                run_single_cycle(sensor_aggregator, ai_processor, alert_system)
                time.sleep(10)  # Wait 10 seconds between cycles

    except KeyboardInterrupt:
        logger.info("Received interrupt signal. Shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
        return False
    finally:
        # Cleanup
        logger.info("Cleaning up...")
        ai_processor.unload_model()
        logger.info("System shutdown complete")

    return True

def run_single_cycle(sensor_aggregator, ai_processor, alert_system):
    """Run a single processing cycle"""
    try:
        # Collect sensor data
        logger = logging.getLogger(__name__)
        logger.info("Collecting sensor data...")
        sensor_data = sensor_aggregator.process_sensor_data()

        # Run AI inference
        logger.info("Running AI inference...")
        inference_result = ai_processor.run_inference(sensor_data)

        # Process alert
        logger.info("Processing alert...")
        alert_system.process_alert(inference_result)

        logger.info("Cycle completed successfully")

    except Exception as e:
        logger.error(f"Error in processing cycle: {e}")

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)