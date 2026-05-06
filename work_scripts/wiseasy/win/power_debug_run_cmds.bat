scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515/vendor_boot.img .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/msm-kernel-bengal-consolidate/dist/boot.img .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/msm-kernel-bengal-consolidate/msm-kernel/drivers/power/supply/sgm41528_charger.ko .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/msm-kernel-bengal-consolidate/msm-kernel/drivers/power/supply/max1726x_battery.ko .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/msm-kernel-bengal-consolidate/msm-kernel/drivers/usb/dwc3/dwc3-msm.ko .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515/vendor_dlkm/lib/modules/sitronix_incell.ko .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/msm-kernel-bengal-consolidate/msm-kernel/drivers/hwtracing/coresight/coresight-csr.ko .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/msm-kernel-bengal-consolidate/msm-kernel/drivers/hwtracing/coresight/coresight-hwevent.ko .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/device/qcom/bengal-kernel/dtbs/dtbo.img .

REM @GOTO :STEP1
adb wait-for-device
adb root
adb shell vdc checkpoint commitChanges
adb remount
adb push sgm41528_charger.ko /vendor_dlkm/lib/modules
adb push max1726x_battery.ko /vendor_dlkm/lib/modules
adb push sitronix_incell.ko /vendor_dlkm/lib/modules
adb push coresight-csr.ko /vendor_dlkm/lib/modules
adb push coresight-hwevent.ko /vendor_dlkm/lib/modules
adb push dwc3-msm.ko /vendor_dlkm/lib/modules

adb reboot bootloader
:STEP1
fastboot flash boot_a boot.img
fastboot flash vendor_boot_a vendor_boot.img
fastboot flash dtbo_a dtbo.img
fastboot reboot
adb wait-for-device
adb root
adb shell "mount -t debugfs none /sys/kernel/debug"
REM adb shell "echo 3 > /proc/sys/kernel/printk"
REM adb shell "echo 'POWER OFF' > /dev/wis_sp"
REM adb shell "echo 'shutdown' > /sys/devices/platform/soc/soc:wis_sp/pin_state"
