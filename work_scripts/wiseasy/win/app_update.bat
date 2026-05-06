scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515tiny/system/bin/wis_scan_demo .

adb wait-for-device
adb root
adb remount

adb push wis_scan_demo /system/bin

REM adb reboot
