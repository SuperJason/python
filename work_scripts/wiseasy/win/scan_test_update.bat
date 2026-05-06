REM ssh fuzhongxin@10.30.0.52 "cd /home/workspace_sda/fuzhongxin/p5/external/test_tools && ./compile.sh"
scp fuzhongxin@10.30.0.52:/home/workspace_sda/fuzhongxin/p5/out/target/product/bengal/system/bin/p5pro_scanner_test .
adb wait-for-device && adb root
adb push p5pro_scanner_test /data/
adb shell "chmod a+x /data/p5pro_scanner_test"
REM adb shell "/data/p5pro_scanner_test"
