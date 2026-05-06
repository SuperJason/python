scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/dist/max1726x_battery.ko .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/dist/sgm41528_charger.ko .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/dist/extcon-dock.ko .

adb wait-for-device
adb root
adb remount
adb push max1726x_battery.ko /vendor_dlkm/lib/modules
adb push sgm41528_charger.ko /vendor_dlkm/lib/modules
adb push extcon-dock.ko /vendor_dlkm/lib/modules
adb reboot
