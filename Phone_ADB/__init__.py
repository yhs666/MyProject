from adb_android import adb_android


#adb_android.push('/tmp/file.txt', '/data/media/0')
#adb_android.pull('/data/media/0/file.txt', '/tmp/')
adb_android.shell('ls')
adb_android.devices()
adb_android.bugreport("report.log")
#adb_android.install('/usr/local/app.apk')
#adb_android.uninstall('com.example.android.valid')
adb_android.getserialno()
