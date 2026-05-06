scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515/vendor_dlkm/lib/modules/sitronix_incell.ko .

adb wait-for-device
adb root
adb remount
adb push sitronix_incell.ko /vendor_dlkm/lib/modules

adb reboot
