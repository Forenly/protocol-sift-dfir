#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol SIFT: Cyber-Physical DFIR Demo Runner
A premium CLI experience illustrating the MCP-driven SIFT AI Analyst workflow.
"""

import os
import sys
import time
from sift_analyst_agent import Colors, SiftAnalystAgent

BANNER = f"""
{Colors.BLUE}{Colors.BOLD}========================================================================
██████╗ ██████╗  ██████╗ ████████╗ ██████╗  ██████╗ ████╗     ██████╗██╗███████╗████████╗
██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔════╝ ██║██║     ██╔════╝██║██╔════╝╚══██╔══╝
██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║██║      ██████╔╝  ███████╗██║█████╗     ██║   
██╔═══╝ ██╔══██╗██║   ██║   ██║   ██║   ██║██║      ██╔══██╗  ╚════██║██║██╔══╝     ██║   
██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╗ ██║  ██║  ███████║██║██║        ██║   
╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝  ╚══════╝╚═╝╚═╝        ╚═╝   
========================================================================{Colors.END}
           {Colors.GREEN}{Colors.BOLD}🤖 CYBER-PHYSICAL DIGITAL FORENSICS & INCIDENT RESPONSE (DFIR) 🤖{Colors.END}
                {Colors.BOLD}SANS SIFT Workstation + Model Context Protocol (MCP){Colors.END}
"""

def print_menu():
    print(f"\n{Colors.BOLD}Select a Cyber-Physical Forensic Case to investigate:{Colors.END}")
    print(f"[{Colors.GREEN}1{Colors.END}] ROS 2 Autonomous Lawnmower Node Hijack (Bypass Laser /cmd_vel Override)")
    print(f"[{Colors.GREEN}2{Colors.END}] SLAM Spatial Map Modification (Quadruped Tumble & Navigation Defeat)")
    print(f"[{Colors.GREEN}3{Colors.END}] Embedded IoT Mirai Botnet Infection (Drone Autopilot Starvation)")
    print(f"[{Colors.GREEN}4{Colors.END}] Run All Investigations (Full Batch Triage)")
    print(f"[{Colors.RED}Q{Colors.END}] Exit Forensics Console")

def main():
    print(BANNER)
    agent = SiftAnalystAgent()
    
    while True:
        print_menu()
        try:
            choice = input(f"\n{Colors.BOLD}Enter choice [1-4, Q]: {Colors.END}").strip().upper()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting SIFT Console...")
            break
            
        if choice == "1":
            print(f"\n{Colors.BLUE}--- CASE 1 SELECTED ---{Colors.END}")
            agent.analyze_case("case_ros2_node_hijack")
        elif choice == "2":
            print(f"\n{Colors.BLUE}--- CASE 2 SELECTED ---{Colors.END}")
            agent.analyze_case("case_slam_map_tampering")
        elif choice == "3":
            print(f"\n{Colors.BLUE}--- CASE 3 SELECTED ---{Colors.END}")
            agent.analyze_case("case_dji_mirai_botnet")
        elif choice == "4":
            print(f"\n{Colors.BLUE}--- BATCH RUN COMMENCING ---{Colors.END}")
            agent.analyze_case("case_ros2_node_hijack")
            agent.analyze_case("case_slam_map_tampering")
            agent.analyze_case("case_dji_mirai_botnet")
        elif choice == "Q":
            print(f"\n{Colors.GREEN}Session closed. Stay safe out in physical space! 🐝🍯{Colors.END}")
            break
        else:
            print(f"{Colors.RED}Invalid input. Please enter 1, 2, 3, 4, or Q.{Colors.END}")

if __name__ == "__main__":
    main()
