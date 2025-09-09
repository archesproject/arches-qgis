equals(QT_MAJOR_VERSION, 5)
!versionAtLeast(QT_VERSION, 5.15.0):error("Use at least Qt version 5.15.0")

# add all .ui files (arches-qgis dialogs) from this dir
FORMS += $$files(*.ui)
