
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#

from FabricEngine.SceneGraph.SceneImpl import Scene
from FabricEngine.SceneGraph.Nodes.SceneGraphNodeImpl import SceneGraphNode

class MyValuesNode(SceneGraphNode):

  def __init__(self, scene, count=11):

    super(MyValuesNode, self).__init__(scene)

    # create a core node
    scalarDGNode = self.constructDGNode('Scalars')
    scalarDGNode.addMember('a', 'Scalar', 1.0)
    scalarDGNode.addMember('b', 'Scalar', 2.0)

    # resize the node for parallel computation
    scalarDGNode.resize(count)

class MyResultsNode(SceneGraphNode):

  def __init__(self, scene):

    super(MyResultsNode, self).__init__(scene)

    # create a core node
    calcDGNode = self.constructDGNode('Calculator')
    calcDGNode.addMember('product', 'Scalar')
    calcDGNode.addMember('sum', 'Scalar')

    # define reference interfaces
    self.addInPort('Values', MyValuesNode, self.__onConnectValues)

    # private members
    self.__operatorsConstructed = False

  def __onConnectValues(self, data):

    node = data['node']
    if not node is None:

      calcDGNode = self.getDGNode('Calculator')
      valueDGNode = node.getDGNode('Scalars')

      # connect the nodes
      calcDGNode.setDependency('values', valueDGNode)

      # check if we have constructed the operators yet
      if not self.__operatorsConstructed:
    
        # The operator that will resize this node
        self.bindDGOperator(calcDGNode.bindings,
          name = 'resizeOp', 
          fileName = '2_basicMath.kl',
          layout = [
            'self',
            'values'
          ]
        )

        # The operators that will perform our computation
        self.bindDGOperator(calcDGNode.bindings,
          name = 'mulOp', 
          fileName = '2_basicMath.kl',
          layout = [
            'self.index',
            'values.a<>',
            'values.b<>',
            'self.product'
          ]
        )
        self.bindDGOperator(calcDGNode.bindings,
          name = 'addOp', 
          fileName = '2_basicMath.kl',
          layout = [
            'self.index',
            'values.a<>',
            'values.b<>',
            'self.sum'
          ]
        )

        self.__operatorsConstructed = True

  def compute(self):
    self.getDGNode('Calculator').evaluate()

# setup a scene and two nodes
scene = Scene(None)
values = MyValuesNode(scene, count = 10)
results = MyResultsNode(scene)

# connect them through the reference interface
results.getInPort('Values').setConnectedNode(values)

# check errors
scene.checkErrors()

# fire computation
results.compute()

# destroy all objects
scene.close()