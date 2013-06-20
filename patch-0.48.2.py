#! /usr/bin/python -u
import os, subprocess, sys

# Thanks to http://cheer-ful.seesaa.net/article/150789261.html
xmodmap_content = """keycode 66 = Meta_L
keycode 69=Meta_R
keycode 67 = Meta_L
keycode 63 = Control_L
keycode 71 = Control_R
clear mod2
clear control
add mod2 = Meta_L
add control = Control_L Control_R
"""
xmodmap_file = os.environ["HOME"]+"/.xmodmap"
# Thanks to http://blog.livedoor.jp/unahide/archives/52785330.html
inkscape_file = "/Applications/Inkscape.app/Contents/Resources/bin/inkscape"

def move_to_bak(f):
    bak = f+".bak"
    if not os.path.isfile(f) or os.path.isfile(bak):
        return bak
    os.rename(f,bak)
    return bak

def main(argv):
    if len(argv) > 1:
        lang = argv[1]
    else: lang = "ja_JP.UTF8"

    move_to_bak(xmodmap_file)
    fw = open(xmodmap_file,"w")
    fw.write(xmodmap_content)
    fw.close()
    print "Created '%s'." % (xmodmap_file)
    print "It enables Inkscape to Alt key."
    print ""

    tmp = "/tmp/inkscape"
    bak = move_to_bak(inkscape_file)
    fw = open(tmp,"w")
    fr = open(bak,"r")
    following = 0
    for line in fr:
        if line.startswith("export LANG="):
            fw.write("#"+line)
            following = 1
        elif following > 0:
            following -= 1
            fw.write("#"+line)
            fw.write("export LANG=%s\n" % (lang))
        else:
            fw.write(line)
    fr.close()
    fw.close()
    subprocess.call(["mv",tmp,inkscape_file])
    subprocess.call(["chmod","+x",inkscape_file])
    print "Modified '%s'." % (inkscape_file)
    print "It changes Inkscape default language to Japanese."
    print ""

if __name__ == "__main__":
    # inkscape.py lang
    main(sys.argv)

