#------------------------------------------------------------------------------#
#             Site-specific Seismic Hazard Analysis & Research Kit             #
#                      A Site Response Analysis Tool                           #
#                                                                              #
#------------------------------------------------------------------------------#

QT       += core gui quick qml webenginewidgets uitools webengine webchannel

CONFIG += c++11

TARGET = s3hark
TEMPLATE = lib
CONFIG += staticlib

win32 {
    RC_ICONS = icons/NHERI-s3hark-Icon.ico
} else {
    mac {
    ICON = icons/NHERI-s3hark-Icon.icns
    }
}

include($$PWD/ConanHelper.pri)
include(./s3hark.pri)

OTHER_FILES += conanfile.py
