REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515/abl.elf .
REM scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/kernel_platform/out/msm-kernel-bengal-consolidate/dist/unsigned_abl_userdebug.elf abl.elf
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5pro/QISI13/out/target/product/bengal_515tiny/signed/abl.elf .

if /i "%1" neq "--skip-wait-device" (
    adb wait-for-device 
    adb reboot bootloader
)
fastboot flash abl_a  abl.elf
fastboot reboot
