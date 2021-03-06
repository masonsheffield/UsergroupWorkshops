
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#

from FabricEngine.SceneGraph.SceneImpl import Scene
from FabricEngine.SceneGraph.Nodes.SceneGraphNodeImpl import SceneGraphNode

class MyNode(SceneGraphNode):

  def __init__(self, scene, **options):

    super(MyNode, self).__init__(scene, **options)

    # create a core node
    scalarDGNode = self.constructDGNode('Scalars')
    scalarDGNode.addMember('a', 'Scalar', 1.0)
    scalarDGNode.addMember('b', 'Scalar', 2.0)
    scalarDGNode.addMember('result', 'Scalar')

    # The operator that will perform our computation
    self.bindDGOperator(scalarDGNode.bindings,
      name = 'addOp', 
      fileName = '1_basicMath.kl',
      layout = [
        'self.a',
        'self.b',
        'self.result'
      ]
    )

  def compute(self):
    self.getDGNode('Scalars').evaluate()

scene = Scene(None)
node = MyNode(scene)
node.compute()

scene.close()