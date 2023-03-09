# create temporary directory
mkdir tmp-dump-cache

# download latest apk
url=$(curl -IL http://apkfind.com/store/download\?id\=nl.topicus.somtoday.leerling | grep --color=never "Location: http://dl" | sed s/"Location: "//)
curl -o tmp-dump-cache/tmp.apk "${url%$'\r'}\&dl=2"
# dump apk using jadx
jadx -d tmp-dump-cache/out tmp-dump-cache/tmp.apk

# delete old files
rm -rf app/src/main

# replace them with the new files
mv tmp-dump-cache/out/resources app/src/main
mv tmp-dump-cache/out/sources app/src/main/java

# clean up
rm -rf tmp-dump-cache