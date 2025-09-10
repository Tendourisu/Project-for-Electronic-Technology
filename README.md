# Project for Electronic Technology

An intelligent electronic car control system based on STM32 microcontrollers and OpenMV vision modules, implementing various autonomous navigation and visual recognition capabilities.

## Project Overview

This project consists of three main tasks, each demonstrating different electronic car control technologies:

- **Task1**: Line Following - Sensor-based line tracking car
- **Task2**: Labyrinth - Autonomous navigation in maze environments
- **Task3**: Comprehensive Task - Complex tasks combining visual recognition

## Hardware Platform

### Main Controllers
- **STM32F103**: For basic control and sensor data processing
- **STM32H743**: For high-performance computing and complex algorithms
- **OpenMV**: Vision processing module based on MicroPython

### Electronic Car Platform
- LongQiu Universal Electronic Car Control Board
- Three-wheel trapezoidal chassis
- Omnidirectional movement system

### Sensor Configuration
- Photoelectric sensor array (line tracking)
- Ultrasonic distance sensors
- Encoders (motion feedback)
- Camera module (visual recognition)

## Project Structure

```
Project for Electronic Technology/
├── README.md                          # Project documentation
├── Task1 Line_Following/              # Task 1: Line Following
│   └── STM32F103/                     # STM32F103 control code
│       ├── CMSIS/                     # CMSIS library files
│       ├── MDK/                       # Keil MDK project files
│       ├── OBJ/                       # Compilation output files
│       └── USER/                      # User code
├── Task2 Labyrinth/                   # Task 2: Labyrinth Navigation
│   ├── STM32F103/                     # STM32F103 control code, structure like Task1's
│   └── STM32H743/                     # STM32H743 + OpenMV code
├── Task3 Comprehensive_Task/          # Task 3: Comprehensive Task
│   ├── STM32F103/                     # STM32F103 control code, structure like Task1's
│   └── STM32H743/                     # STM32H743 advanced control code
```

## Features

### Task1 - Line Following
- **Function**: High-precision line tracking based on photoelectric sensor array
- **Technology**: 
  - Four-channel photoelectric sensor array
  - PID control algorithm
  - Three-wheel omnidirectional motion control
  - Obstacle detection and avoidance
- **Features**: 
  - Real-time sensor data fusion
  - Adaptive speed control
  - Exception path handling (intersections, sharp turns)

### Task2 - Labyrinth Navigation
- **Function**: Autonomous navigation and path planning in maze environments
- **Technology**: 
  - Dual ultrasonic sensor distance detection
  - Left-hand/right-hand wall following algorithm
  - State machine control logic
- **Features**: 
  - Dynamic path adjustment
  - Wall distance adaptive control
  - Dead-end detection and backtracking mechanism

### Task3 - Comprehensive Task
- **Function**: Complex task execution combining visual recognition
- **Technology**: 
  - OpenMV vision processing
  - Multi-target recognition (lines, balls, arrows)
  - Multi-mode switching control
- **Features**: 
  - Line tracking mode: Vision-based line following
  - Ball kicking mode: Target recognition and precise positioning
  - Obstacle avoidance mode: Dynamic obstacle handling

## Technical Highlights

### Control Algorithms
- **State Machine**: Modular behavior control logic
- **Sensor Fusion**: Real-time multi-sensor data processing

### Vision Processing
- **Color Recognition**: HSV color space threshold processing
- **Shape Detection**: Blob detection and template matching
- **Real-time Processing**: High frame rate vision data processing

### Motion Control
- **Three-wheel Omnidirectional**: Flexible motion control
- **Encoder Feedback**: Precise motion measurement
- **Adaptive Control**: Dynamic adjustment based on task requirements

## Development Environment

### STM32 Development
- **IDE**: Keil MDK-ARM
- **Framework**: STM32 HAL Library
- **Programming Language**: C

### OpenMV Development
- **IDE**: OpenMV IDE
- **Framework**: MicroPython
- **Dependencies**: 
  - OpenMV built-in image processing library
  - Custom PID control module
  - Custom motor control module

## Build and Deployment

### STM32 Projects
1. Open the corresponding `.uvprojx` project file with Keil MDK
2. Configure target chip model (STM32F103 or STM32H743)
3. Build project to generate firmware
4. Download to target board via J-Link or ST-Link

### OpenMV Projects
1. Open Python files with OpenMV IDE
2. Connect OpenMV camera module
3. Run directly or save to device

## Usage Instructions

### Hardware Connections
1. Ensure all sensors are correctly connected to corresponding GPIO pins
2. Check motor driver board communication with main controller
3. Verify stable power supply

### Software Configuration
1. Adjust sensor thresholds according to actual hardware
2. Calibrate motor parameters and PID coefficients
3. Set serial communication parameters

### Running Tests
1. Observe OLED display status after power-on
2. Switch between different working modes via buttons
3. Monitor serial output for debugging information

## Contact Information

For questions or suggestions, please contact via:
- Project Repository: [GitHub Repository](https://github.com/Tendourisu/Project-for-Electronic-Technology)
- Issue Reporting: GitHub Issues

---
