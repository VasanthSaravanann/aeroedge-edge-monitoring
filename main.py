#!/usr/bin/env python3
"""
Main Entry Point for AeroEdge System
Coordinates all components of the edge AI monitoring system.
"""

import logging
import time
import argparse
import sys
import traceback
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
    logger.info(f"Debug mode: {args.debug}")
    logger.info(f"Test mode: {args.test}")

    # Initialize components
    try:
        logger.info("Initializing system components...")

        sensor_aggregator = SensorDataAggregator()
        ai_processor = EdgeAIProcessor()
        alert_system = AlertSystem()

        logger.info("System components initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize system components: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

    # Load AI model
    try:
        logger.info("Loading AI model...")
        if not ai_processor.load_model():
            logger.error("Failed to load AI model. Exiting.")
            return False
        logger.info("AI model loaded successfully")

    except Exception as e:
        logger.error(f"Failed to load AI model: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

    # Validate model
    try:
        logger.info("Validating AI model...")
        if not ai_processor.validate_model():
            logger.error("Model validation failed. Exiting.")
            return False
        logger.info("AI model validated successfully")

    except Exception as e:
        logger.error(f"Model validation failed: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

    # Main processing loop
    try:
        logger.info("Starting main processing loop...")

        if args.test:
            logger.info("Running in test mode")
            # Run a single test cycle
            success = run_single_cycle(sensor_aggregator, ai_processor, alert_system)
            if not success:
                logger.error("Test cycle failed")
                return False
        else:
            # Continuous monitoring loop
            cycle_count = 0
            while True:
                try:
                    success = run_single_cycle(sensor_aggregator, ai_processor, alert_system)
                    if not success:
                        logger.warning("Processing cycle had issues, continuing...")

                    cycle_count += 1
                    if cycle_count % 10 == 0:
                        logger.info(f"Processed {cycle_count} cycles successfully")

                    time.sleep(10)  # Wait 10 seconds between cycles

                except KeyboardInterrupt:
                    logger.info("Received interrupt signal. Shutting down...")
                    break
                except Exception as e:
                    logger.error(f"Error in main processing loop: {e}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    # Continue processing despite individual cycle errors
                    time.sleep(5)  # Brief pause before retrying

    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False
    finally:
        # Cleanup
        logger.info("Cleaning up...")
        try:
            ai_processor.unload_model()
            logger.info("AI model unloaded successfully")
        except Exception as e:
            logger.error(f"Error during model unload: {e}")

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
        success = alert_system.process_alert(inference_result)

        if success:
            logger.info("Cycle completed successfully")
        else:
            logger.warning("Alert processing failed, but cycle continues")

        return True

    except Exception as e:
        logger.error(f"Error in processing cycle: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)