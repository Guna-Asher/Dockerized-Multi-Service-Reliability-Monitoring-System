import json
import os
from datetime import datetime
from typing import Dict, Any

class Logger:
    def __init__(self, log_path: str):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    def log(self, event: str, service: str, details: Dict[str, Any] = None):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": event,
            "service": service,
            "details": details or {}
        }
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def alert(self, message: str):
        print(f"[{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')} ALERT] {message}")
    
    def generate_report(self, uptime_data: Dict[str, Any]):
        report_path = '/app/reports/reliability_summary.txt'
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        summary = "Reliability Summary\n"
        summary += "=" * 50 + "\n\n"
        
        total_uptime = 0
        for service, data in uptime_data.items():
            uptime_pct = data['uptime_pct']
            summary += f"{service.upper()}:\n"
            summary += f"  Uptime: {uptime_pct:.2f}%\n"
            summary += f"  Restarts: {data['restarts']}\n\n"
            total_uptime += uptime_pct
        
        avg_uptime = total_uptime / len(uptime_data)
        summary += f"Average Availability: {avg_uptime:.2f}%\n"
        
        with open(report_path, 'w') as f:
            f.write(summary)
        
        self.alert(f"Report generated. Avg Uptime: {avg_uptime:.2f}%")

