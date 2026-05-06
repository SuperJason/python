scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/modem/p5pro/amss/BOOT.XF.4.1/boot_images/QcomPkg/SocPkg/KamortaPkg/Bin/LAA/RELEASE/xbl.elf .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/modem/p5pro/amss/BOOT.XF.4.1/boot_images/QcomPkg/SocPkg/KamortaPkg/Bin/LAA/RELEASE/xbl_config.elf .
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/modem/p5pro/amss/BOOT.XF.4.1/boot_images/QcomPkg/SocPkg/KamortaPkg/Bin/LAA/RELEASE/imagefv.elf .

if /i "%1" neq "--skip-wait-device" (
    adb wait-for-device 
    adb reboot bootloader
)
fastboot flash xbl_a xbl.elf
fastboot flash xbl_b xbl.elf
fastboot flash xbl_config_a xbl_config.elf
fastboot flash xbl_config_b xbl_config.elf
fastboot flash imagefv_a imagefv.elf
fastboot flash imagefv_b imagefv.elf
fastboot reboot
