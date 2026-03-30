import docker
import time
import json
import os
import requests
import signal
from datetime import datetime
from logger import Logger
from typing import Dict, Any

# Load config
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

POLL_INTERVAL = CONFIG['poll_interval']
MAX_RESTARTS = CONFIG['max_restarts']
SERVICES = CONFIG['services']
REPORT_INTERVAL = CONFIG['report_interval']
HEALTH_TIMEOUT = CONFIG['health_timeout']

# Init
client = docker.from_env(version='auto')
logger = Logger('/app/logs/container_events.json')
uptime_data: Dict[str, Dict[str, Any]] = {}

def signal_handler(sig, frame):
    logger.alert("Monitor shutting down gracefully...")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def is_service_healthy(container) -> bool:
    """Check container status and health endpoint if applicable."""
    if container.status != 'running':
        return False
    
    container_name = container.name.split('_')[0]  # container_name: service
    
    if container_name == 'flask-app':
        try:
            response = requests.get(
                'http://flask-app:5000/health',
                timeout=HEALTH_TIMEOUT
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    # For nginx/redis: rely on Docker status + healthcheck
    health = container.attrs.get('State', {}).get('Health', {}).get('Status', 'unknown')
    return health in ['healthy', 'starting']

def calculate_uptime(start_time_str: str, total_time: float) -> float:
    """Approximate uptime % from start time."""
    if not start_time_str:
        return 0.0
    start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
    running_time = (datetime.utcnow() - start_time).total_seconds()
    return min((running_time / total_time) * 100, 100.0)

def update_uptime_data():
    """Update uptime tracking for all services."""
    monitoring_start = time.time()
    cycle_count = 0
    
    while True:
        cycle_start = time.time()
        
        for service in SERVICES:
            try:
                containers = client.containers.list(
                    filters={'name': service},
                    all=True
                )
                if not containers:
                    logger.log('error', service, {'message': 'Container not found'})
                    continue
                
                container = containers[0]
                service_name = service  # e.g., 'nginx'
                
                if service_name not in uptime_data:
                    uptime_data[service_name] = {'start_time': None, 'restarts': 0, 'monitoring_time': 0}
                
                data = uptime_data[service_name]
                
                healthy = is_service_healthy(container)
                started_at = container.attrs['State'].get('StartedAt')
                
                if started_at:
                    data['start_time'] = started_at
                    data['monitoring_time'] = time.time() - cycle_start
                    data['uptime_pct'] = calculate_uptime(started_at, data['monitoring_time'] * 100)  # rough approx per cycle
                
                if not healthy:
                    logger.alert(f"CRITICAL: {service_name} unhealthy/stopped at {datetime.utcnow().isoformat()}")
                    logger.log('failure', service_name, {'status': container.status, 'health': container.attrs.get('State', {}).get('Health', {})})
                    
                    if data['restarts'] < MAX_RESTARTS:
                        try:
                            container.restart()
                            data['restarts'] += 1
                            logger.log('restart', service_name, {'attempt': data['restarts']})
                            logger.alert(f"Restart attempt {data['restarts']} successful for {service_name}")
                        except Exception as e:
                            logger.log('restart_failed', service_name, {'error': str(e)})
                    else:
                        logger.alert(f"Max restarts exceeded for {service_name}")
                else:
                    logger.log('healthy', service_name, {'uptime_pct': data.get('uptime_pct', 0)})
            
            except Exception as e:
                logger.log('error', service, {'error': str(e)})
        
        cycle_count += 1
        if cycle_count % REPORT_INTERVAL == 0:
            logger.generate_report(uptime_data)
        
        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    logger.alert("Starting Reliability Monitor...")
    update_uptime_data()

