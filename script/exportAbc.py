import sys
import os
import maya.cmds as cmds
import pymel.core as pm
def _assemblePath(path):
    assemblePaths = ''
    for string in path:
        assemblePaths+=string
        assemblePaths+='#'
    return assemblePaths

def getframeRange():
    minT = cmds.playbackOptions(query=True, minTime=True)
    maxT = cmds.playbackOptions(query=True, maxTime=True)
    return [int(minT), int(maxT)]
    
def getObject(filters):
    obj = []
    all = cmds.ls(type = 'transform',long = True)
    for i in  all:
        if filters in i:
            if cmds.listRelatives(i,shapes=True) !=None:
                obj.append(i)
    return obj
    
def exportAbc(path, singleFrame=False, frameRange=None, objects=[], step_num=0.2,
              options=['-stripNamespaces', '-uvWrite', '-wholeFrameGeo','-worldSpace','-writeVisibility','-writeUVSets',
                       '-dataFormat ogawa']):
    '''Exports abc cache file.'''
    # AbcExport -j "-frameRange 1 34 -dataFormat ogawa -root |camera:tst_001_01 -root |dog:dog -file C:/Users/nian/Documents/maya/projects/default/cache/alembic/test.abc";

    cmds.loadPlugin("AbcExport")

    # Get arguments
    if singleFrame:
        frameRange = [self.currentFrame(), self.currentFrame()]
    elif frameRange == None:
        frameRange = getframeRange()
    # print frameRange
    args = '-frameRange %s %s ' % (frameRange[0], frameRange[1])

    if type(options) in (list, tuple):
        options = ' '.join(options)

    if options:
        args += options + ' '

    step_str = "-step " + str(step_num)
    args = step_str + " " + args
    for obj in objects:
        args += '-root %s ' % obj

    args += '-file %s' % path

    # Get cmd
    cmd = 'AbcExport -j "%s";' % args
    print cmd
    pm.mel.eval(cmd)
    
def RunExport(path,filters='',publishPath =''):
    paths = path.split('#')
    paths.pop(-1)
    for i in paths:
        cmds.file(i, o=1,f=1)
        objs = getObject(filters)
		output = (os.path.join(publishPath,(os.path.basename(i)).split('.')[0]+'.abc')).replace('\\','/')
        exportAbc(output,objects =objs)

