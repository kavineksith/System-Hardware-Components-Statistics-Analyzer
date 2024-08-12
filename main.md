# System Analyzer Script Documentation

## Overview
The System Analyzer script is a Python utility designed to generate detailed reports on various system metrics, including CPU usage, process management, memory statistics, disk usage, network status, system information, and battery status. By leveraging multiple management modules, the script provides comprehensive insights into system performance and health. Users can generate individual reports or an all-inclusive report, with results stored in JSON format for easy access and analysis.

## Features
- **Comprehensive Reporting**: Generate detailed reports on CPU, process management, memory, disk, network, system information, and battery status.
- **Customizable Reports**: Choose between single metric reports and an all-in-one report.
- **Screen Management**: Clear the terminal screen for improved readability.
- **Error Handling**: Gracefully handles errors and user interruptions.
- **JSON Output**: Results are saved in JSON format for consistent and structured data presentation.

## Dependencies
- **Python**: Requires Python 3.x.
- **Modules**:
  - `battery_management`: For battery status monitoring.
  - `cpu_management`: For CPU usage monitoring.
  - `disk_management`: For disk usage management.
  - `memory_management`: For memory statistics.
  - `network_management`: For network status reporting.
  - `process_management`: For process management.
  - `system_infoAnalyzer`: For system information retrieval.
  - `terminal_clearance`: For clearing the terminal screen.
  - `methods`: For converting results to JSON format.

## Usage
To use the System Analyzer script, execute it with Python 3.x. The script will prompt for the type of report needed and then generate the corresponding report based on user input.

### Running the Script
1. **Start the Script**: Execute the script using Python 3.x to launch the reporting wizard.
2. **Select Report Type**:
   - **Single Report**: Generate a report for a specific system metric by entering the corresponding Report ID (1-7) or choose 0 to clear the screen.
   - **All-in-One Report**: Generate a comprehensive report covering all metrics.
3. **View or Save Report**: The results will be saved in JSON format. Ensure the `methods.control_result_to_json` function is correctly implemented to handle this.

## Interactive Commands
- **Generate Single Report**: Enter a Report ID (1-7) to generate a specific metric report or 0 to clear the screen.
- **Generate All-in-One Report**: Choose "all_in_one" to generate a comprehensive report of all metrics.
- **Clear Screen**: Enter 0 during the single report generation process to clear the terminal screen.
- **Exit**: The script exits gracefully upon completion or interruption.

## Special Commands
- **Screen Clearing**: Handled by the `ScreenManager` class. It uses `cls` for Windows and `clear` for Unix-based systems to clear the terminal screen.
- **Error Handling**: Includes handling for invalid inputs, keyboard interrupts, and general exceptions to ensure a smooth user experience.

## Conclusion
The System Analyzer script offers a robust tool for monitoring and reporting on various system metrics. By providing detailed insights into CPU usage, process management, memory, disk, network, system information, and battery status, it helps users maintain a clear understanding of their system's performance. With features like customizable reporting, screen management, and JSON output, the script is a versatile solution for both casual users and system administrators. Its comprehensive error handling ensures reliability and ease of use in various scenarios.

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### **Disclaimer:**
Kindly note that this project is developed solely for educational purposes, not intended for industrial use, as its sole intention lies within the realm of education. We emphatically underscore that this endeavor is not sanctioned for industrial application. It is imperative to bear in mind that any utilization of this project for commercial endeavors falls outside the intended scope and responsibility of its creators. Thus, we explicitly disclaim any liability or accountability for such usage.
