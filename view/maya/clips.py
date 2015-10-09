# Clips window

import maya.cmds as cmds

i18n = {
    "clips" : {
        "title"         : "Clips Menu",
        "editChar"      : "Click to change the characters details",
        "addClip"       : "Click to add clip to the scene",
        "editClip"      : "Edit",
        "editClipDesc"  : "Click to change the clips details"
    }
}

class Clips(object):
    def __init__(s, i18n, char, requestCharEdit, requestClipEdit, sendClip):
        s.i18n = i18n
        s.char = char
        s.requestClipEdit = requestClipEdit # We're asking to edit the clip
        s.sendClip = sendClip # User wants to place the clip
        name = "clipname"

        s.winName = "%sWin" % name
        if cmds.window(s.winName, ex=True):
            cmds.deleteUI(s.winName)
        s.window = cmds.window(s.winName, rtf=True, t=s.i18n["title"])
        cmds.columnLayout(adj=True)
        cmds.rowLayout(nc=2, adj=1)
        cmds.text(
            l="<h1>%s</h1>" % name,
            hl=True,
            h=50
            )
        cmds.iconTextButton(
            ann=i18n["editChar"],
            style="iconOnly",
            font="boldLabelFont",
            image="ghostOff.png",
            h=50,
            w=50,
            bgc=[0.1,0.1,0.1],
            c=requestCharEdit
        )
        cmds.setParent("..") # Close row
        cmds.separator()
        cmds.floatSlider(
            min=50,
            max=200,
            v=100,
            dc=s.sizeClips,
            h=20
            )
        cmds.scrollLayout(cr=True, bgc=[0.2,0.2,0.2], h=400)
        s.wrapper = cmds.gridLayout(cwh=[100, 130], cr=True)
        cmds.showWindow(s.window)
        s.refresh()
    def sizeClips(s, val):
        cmds.gridLayout(s.wrapper, e=True, cwh=[val,val+30])
        if s.clips:
            for c in s.clips:
                c.resize(val)
    def refresh(s):
        try:
            cmds.deleteUI(cmds.layout(s.wrapper, q=True, ca=True))
        except RuntimeError:
            pass
        s.clips = []
        for c in range(20): # TODO, get these from the character
            s.clips.append(Clip(
                s.i18n,
                s.wrapper,
                c,
                s.sendClip,
                s.requestClipEdit,
                "ghostOff.png",
                "time.svg"
                ))
            s.clips[-1].resize(100)

class Clip(object):
    """
    Single clip
    """
    def __init__(s, i18n, parent, clip, sendClip, requestClipEdit, imgSmall, imgLarge):
        cmds.columnLayout(adj=True, bgc=[0.1,0.1,0.1], p=parent)
        s.imgSmall = imgSmall
        s.imgLarge = imgLarge
        s.img = cmds.iconTextButton(
            l="",
            ann=i18n["addClip"],
            style="iconOnly",#"iconAndTextVertical",
            image=s.imgSmall,
            c=lambda: sendClip(clip)
            )
        s.btn = cmds.button(
            l=i18n["editClip"],
            ann=i18n["editClipDesc"],
            h=30,
            c=lambda x: requestClipEdit(clip)
            )
    def resize(s, size):
        img = s.imgSmall if size < 150 else s.imgLarge
        cmds.iconTextButton(s.img, e=True, w=size, h=size, i=img)

#
# def test(*args):
#     print "edit", args
#
# Clips(i18n["clips"], None, test, test, test)
