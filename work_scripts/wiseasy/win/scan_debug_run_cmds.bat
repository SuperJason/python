scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515/vendor_boot.img .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/msm-kernel-bengal-consolidate/dist/boot.img .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/dist/msm_geni_serial.ko .

adb wait-for-device
adb root
adb shell vdc checkpoint commitChanges
adb remount
adb push msm_geni_serial.ko /vendor_dlkm/lib/modules

adb reboot bootloader
fastboot flash boot_a boot.img
fastboot flash vendor_boot_a vendor_boot.img
fastboot reboot
adb wait-for-device
adb root
REM timeout /T 5
REM adb shell "echo '1' > /sys/devices/platform/wiseasy,scan/port_state"
REM timeout /T 3
REM adb shell "echo '0' > /sys/devices/platform/wiseasy,scan/port_state"
