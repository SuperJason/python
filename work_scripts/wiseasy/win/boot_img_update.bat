REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/gki_kernel/dist/boot.img .
REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/dist/boot.img .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5p/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/dist/boot.img .
adb wait-for-device
adb reboot bootloader
fastboot flash boot_a boot.img
fastboot reboot
