scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515tiny/recovery.img .
adb wait-for-device
adb reboot bootloader
fastboot flash recovery_a recovery.img
fastboot reboot
