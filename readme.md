# Turn off speakers using a smart plug when Windows is not playing any sound

When your computer speakers use a lot of energy in idle (common when using Class A/B amplifiers) then it makes sense to turn them off automatically when they are not outputting any sound.

- For this I used a very cheap smart plug from Aliexpress and flashed it with this firmware: https://github.com/openshwprojects/OpenBK7231T_App
- Because I don't have any tasmota or MQTT server this script is using the HTTP configuration interface of the smart plug directly.
- The script is using the Windows win32 api to get the current volume level. When the volume is zero for two minutes the script turns off the smart plug and the speakers. As soon as there is any sound playing in Windows the smart plug is turned on again.
- Adjust the IP address in main.py and put the batch file into the autostart directory. The application will run in the background (visible as pythonw3.9.exe in the task manager). 