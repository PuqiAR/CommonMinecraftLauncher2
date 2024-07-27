@echo off
echo building Restarter.cpp
g++ -std=c++20 -static -o CMCL/Restarter.exe Dev-Tools/Restarter.cpp
echo built successfully