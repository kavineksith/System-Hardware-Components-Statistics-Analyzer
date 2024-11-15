#!/usr/bin/env python3

import json
import psutil
import sys
from report_signatures import TimeStampGenerator


class ProcessManager:
    def __init__(self):
        self.process_list = None

    def get_process_list(self):
        try:
            self.process_list = [{'pid': pid} for pid in psutil.pids()]
            return self.process_list
        except Exception as e:
            print(f"Error retrieving process list: {e}")
            sys.exit(1)

    def get_process_info(self):
        process_info_list = []
        try:
            for process in self.process_list:
                process_id = process['pid']
                process = psutil.Process(process_id)
                process_info = process.as_dict(attrs=['pid', 'name'])
                process_info_list.append(process_info)

            return process_info_list
        except psutil.NoSuchProcess as e:
            print(f"Error retrieving process info: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def manage_processes(self):
        try:
            # System Processes Statistics
            process_list = self.get_process_list()
            process_info = self.get_process_info()

            # Check if process_list is a string, if not convert it to a string
            if not isinstance(process_list, str):
                process_list = ", ".join(map(str, process_list))

            statistics = {
                'System Processes Statistics': {
                    'Process List': process_list,
                    'Process Info': process_info,
                    'Generated Time & Date': f'{TimeStampGenerator().generate_report()}'
                }
            }

            result = json.dumps(statistics, indent=4)
            json_output = json.loads(result)
            return json_output  # Return the JSON output as a string
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
