@echo off
rem open shortcut
type %1|find "\"|find /v "/" > C:\temp\vartmp.txt
set /p vartmp=<C:\temp\vartmp.txt
DEL C:\temp\vartmp.txt
cd %vartmp%
