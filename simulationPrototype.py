#required import for python
import Sofa

USE_GUI = True


def main():
	import SofaRuntime
	import Sofa.Gui
	SofaRuntime.importPlugin("SofaOpenglVisual")
	SofaRuntime.importPlugin("SofaImplicitOdeSolver")
	
	root = Sofa.Core.Node("root")
	createScene(root)
	Sofa.Simulation.init(root)
	
	if not USE_GUI:
		for iteration in range(10):
			Sofa.Simulation.animate(root, root.dt.value)
	else:
		Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
		Sofa.Gui.GUIManager.createGUI(root, __file__)
		Sofa.Gui.GUIManager.SetDimension(1080, 1080)
		Sofa.Gui.GUIManager.MainLoop(root)
		Sofa.Gui.GUIManager.closeGUI()
        
def createScene(root):
	root.gravity = [0,-9.81, 0]
	root.dt = 0.02
        
	root.addObject('DefaultVisualManagerLoop')
	root.addObject('DefaultAnimationLoop')

	root.addObject('VisualStyle', displayFlags="showCollisionModels showForceFields")
	root.addObject('RequiredPlugin', pluginName="SofaImplicitOdeSolver SofaLoader SofaOpenglVisual SofaBoundaryCondition SofaGeneralLoader SofaGeneralSimpleFem")
	root.addObject('DefaultPipeline', name="CollisionPipeline")
	root.addObject('BruteForceBroadPhase', name="BroadPhase")
	root.addObject('BVHNarrowPhase', name="NarrowPhase")
	root.addObject('DefaultContactManager', name="CollisionResponse", response="default")
	root.addObject('DiscreteIntersection')
	
	#arrow for orientation information
	#confignode = root.addChild("Config")
	#confignode.addObject('OglSceneFrame', style="Arrows", alignment="TopRight")
    	
	phantom = root.addChild('Phantom')
	phantom.addObject('EulerImplicitSolver', name="cg_odesolver", rayleighStiffness=0.1, rayleighMass=0.1)
	phantom.addObject('CGLinearSolver', name="linear_solver", iterations=25, tolerance=1e-09, threshold=1e-09)
    	
	phantom.addObject('MeshGmshLoader', name="meshLoader", filename="./phantom.msh")
	phantom.addObject('TetrahedronSetTopologyContainer', name="topo", src="@meshLoader")
	phantom.addObject('MechanicalObject', name="dofs", src="@meshLoader")
	#phantom.addObject('TetrahedronSetTopologyModifier' name="Modifier")
	phantom.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="GeomAlgo")
	phantom.addObject('DiagonalMass', name="Mass", totalMass="0.22")
    	#human breast has poisson ratio of 0.5 according to  https://www.eng.tau.ac.il/~msbm/resources/55.PDF
    	#young's modulos = 200 kPa by assumption
	phantom.addObject('TetrahedralCorotationalFEMForceField', template="Vec3d", name="FEM", method="large", poissonRatio=0.49, youngModulus=200000, computeGlobalMatrix=False)
	
	phantom.addObject('BoxROI', template="Vec3d", box="-0.01 -0.01 -0.01 0.1 0.001 0.1", name="FixedROI", drawBoxes="1", drawSize="1")
	phantom.addObject('FixedConstraint', name="fixROIindices", indices="@FixedROI.indices", showObject="True", drawSize="1")
    	
	return root
        
if __name__ == '__main__':
    main()
