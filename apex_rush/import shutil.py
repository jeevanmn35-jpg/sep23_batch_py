import shutil
import os

# Storage Analysis

drive = "C:\\"

total, used, free = shutil.disk_usage(drive)

print("===== COMPUTER STORAGE ANALYSIS =====")

print("Total Storage:", round(total / (1024**3), 2), "GB")

print("Used Storage:", round(used / (1024**3), 2), "GB")

print("Free Storage:", round(free / (1024**3), 2), "GB")

print("Storage Usage:",
      round((used / total) * 100, 2), "%")