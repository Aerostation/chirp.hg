import sys

import os

from chirp import CHIRP_VERSION

def win32_build():
    from distutils.core import setup
    import py2exe

    try:
        # if this doesn't work, try import modulefinder
        import py2exe.mf as modulefinder
        import win32com
        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", p)
        for extra in ["win32com.shell"]: #,"win32com.mapi"
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)
    except ImportError:
        # no build path setup, no worries.
        pass


    opts = {
        "py2exe" : {
            "includes" : "pango,atk,gobject,cairo,pangocairo,win32gui,win32com,win32com.shell,email.iterators,email.generator",

            "compressed" : 1,
            "optimize" : 2,
            "bundle_files" : 3,
            #        "packages" : ""
            }
        }

    setup(
        windows=[{'script'        : "chirpw",
                  'icon_resources': [(0x0004, 'share/chirp.ico')],
		 }],
        options=opts)

def macos_build():
    from setuptools import setup
    import shutil

    APP = ['chirp-%s.py' % CHIRP_VERSION]
    shutil.copy("chirpw", APP[0])
    DATA_FILES = [('../Frameworks',
                   ['/opt/local/lib/libpangox-1.0.dylib']),
		  ('../Resources/', ['/opt/local/lib/pango']),
                  ]
    OPTIONS = {'argv_emulation': True, "includes" : "gtk,atk,pangocairo,cairo"}

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
        )

    EXEC = 'bash ./build/macos/make_pango.sh /opt/local dist/chirp-%s.app' % CHIRP_VERSION
    #print "exec string: %s" % EXEC
    os.system(EXEC) 

def default_build():
    from distutils.core import setup
    from glob import glob

    desktop_files = glob("share/*.desktop")
    #form_files = glob("forms/*.x?l")
    image_files = glob("images/*")
    #_locale_files = glob("locale/*/LC_MESSAGES/D-RATS.mo")
    _locale_files = []

    locale_files = []
    for f in _locale_files:
        locale_files.append(("/usr/share/chirp/%s" % os.path.dirname(f), [f]))

    print "LOC: %s" % str(locale_files)

    setup(
        name="chirp",
        packages=["chirp", "chirpui"],
        version=CHIRP_VERSION,
        scripts=["chirpw"],
        data_files=[('/usr/share/applications', desktop_files),
                    ('/usr/share/chirp/images', image_files),
                    ('/usr/share/doc/chirp', ['COPYING']),
		    ('/usr/share/pixmaps', ['share/chirp.png']),
                    ('/usr/man/man1', ["share/chirpw.1"]),
                    ] + locale_files)

def rpttool_build():
    from distutils.core import setup
    
    setup(name="rpttool",
          packages=["chirp"],
          version="0.2",
          scripts=["rpttool"],
          description="A frequency tool for ICOM D-STAR Repeaters",
          data_files=[('/usr/sbin', ["tools/icomsio.sh"])],
          )

def nuke_manifest(*files):
    for i in ["MANIFEST", "MANIFEST.in"]:
        if os.path.exists(i):
            os.remove(i)

    if not files:
        return

    f = file("MANIFEST.in", "w")
    for fn in files:
        print >>f, fn
    f.close()
                    
if sys.platform == "darwin":
    macos_build()
elif sys.platform == "win32":
    win32_build()
else:
    if os.path.exists("rpttool"):
        nuke_manifest("include tools/icomsio.sh", "include README.rpttool")
        rpttool_build()
    if os.path.exists("chirpui"):
        nuke_manifest("include *.xsd",
                      "include share/*.desktop",
                      "include share/*.1",
                      "include COPYING")
        default_build()

