
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#

import sys
import copy
import math

from FabricEngine.SceneGraph.RT.Math import *
from FabricEngine.SceneGraph.Nodes.Rendering import *
from FabricEngine.SceneGraph.Nodes.Lights import *
from FabricEngine.SceneGraph.Nodes.Images import *
from FabricEngine.SceneGraph.Nodes.Manipulation import *
from FabricEngine.SceneGraph.Nodes.Kinematics import *
from FabricEngine.SceneGraph.Nodes.Importers import *
from FabricEngine.SceneGraph.ServerSide.ServerSideApplicationImpl import *
from BezierDeformComponentImpl import BezierDeformComponent
from BezierGizmoComponentImpl import BezierGizmoComponent
    
class MyDeformerApp(ServerSideApplication):
  
  def __init__(self):
    
    super(MyDeformerApp, self).__init__(
      enableRaycasting=True,
      gridSize=100.0,
      setupUndoRedo=False
    )
    
    # query the constructed components
    scene = self.getScene()
    
    # import the text obj file
    importer = OBJImporter(scene, filePath='text.obj')
    nodesList = importer.importAsset()

    # loop over all constructed nodes
    for name, node in nodesList.iteritems():
      if isinstance(node, PolygonMesh):

        # construct the bezier deformer
        deformerComp = BezierDeformComponent()
        gizmoComp = BezierGizmoComponent(deformerComp = deformerComp)
        node.addComponent(deformerComp)
        node.addComponent(gizmoComp)
   
        # setup the gizmo
        self.__manipulator = GizmoManipulator(scene)
        gizmo = GizmoInstance(scene,
          source=node, 
          sourceDGNodeName='GeometryDGNode', 
          sourceMemberName=gizmoComp.getGizmoMember()
        )
        self.__manipulator.addGizmoNode(gizmo)

    # for every client connecting, 
    # push the gizmo manipulator to the client's camera manipulator
    def onClientConnecting(webSocketHandler):
      webSocketHandler.getCameraManipulator().setChildManipulatorNode(self.__manipulator)

    self.setWebSocketConnectionCallback(onClientConnecting)
    
MyDeformerApp().start()
