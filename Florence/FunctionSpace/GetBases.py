import numpy as np 
import os, sys, imp


from Florence.FunctionSpace import QuadLagrangeGaussLobatto as TwoD
from Florence.FunctionSpace import HexLagrangeGaussLobatto as ThreeD
# Modal Bases
# import Florence.InterpolationFunctions.TwoDimensional.Tri.hpModal as Tri 
# import Florence.InterpolationFunctions.ThreeDimensional.Tetrahedral.hpModal as Tet 
# Nodal Bases
from Florence.FunctionSpace import Tri
from Florence.FunctionSpace import Tet

def GetBases(C,Quadrature,info, useLagrange = False):

    w = Quadrature.weights
    z = Quadrature.points

    ns=[]; Basis=[]; gBasisx=[]; gBasisy=[]
    if info=='tri':
        p=C+1
        ns = (p+1)*(p+2)/2
        Basis = np.zeros((ns,w.shape[0]),dtype=np.float64)
        gBasisx = np.zeros((ns,w.shape[0]),dtype=np.float64)
        gBasisy = np.zeros((ns,w.shape[0]),dtype=np.float64)
    elif info=='quad':
        ns = (C+2)**2
        Basis = np.zeros((ns,z.shape[0]*z.shape[0]),dtype=np.float64)
        gBasisx = np.zeros((ns,z.shape[0]*z.shape[0]),dtype=np.float64)
        gBasisy = np.zeros((ns,z.shape[0]*z.shape[0]),dtype=np.float64)


    if info == 'quad':
        counter = 0
        for i in range(0,z.shape[0]):
            for j in range(0,z.shape[0]):
                ndummy = TwoD.LagrangeGaussLobatto(C,z[i],z[j])[0]
                Basis[:,counter] = ndummy[:,0]
                dummy = TwoD.GradLagrangeGaussLobatto(C,z[i],z[j])
                gBasisx[:,counter] = dummy[:,0]
                gBasisy[:,counter] = dummy[:,1]
                counter+=1
    elif info == 'tri':
        hpBases = Tri.hpNodal.hpBases
        for i in range(0,w.shape[0]):
            # Better convergence for curved meshes when Quadrature.optimal!=0
            ndummy, dummy = hpBases(C,z[i,0],z[i,1],Quadrature.optimal) 
            # ndummy, dummy = Tri.hpBases(C,z[i,0],z[i,1])
            Basis[:,i] = ndummy
            gBasisx[:,i] = dummy[:,0]
            gBasisy[:,i] = dummy[:,1]



    class Domain(object):
        Bases = Basis
        gBasesx = gBasisx
        gBasesy = gBasisy
        gBasesz = np.zeros(gBasisx.shape)


    return Domain



def GetBases3D(C,Quadrature,info):

    ndim = 3

    w = Quadrature.weights
    z = Quadrature.points

    ns=[]; Basis=[]; gBasisx=[]; gBasisy=[]; gBasisz=[]
    if info=='hex':
        ns = (C+2)**ndim
        Basis = np.zeros((ns,(z.shape[0])**ndim),dtype=np.float64)
        gBasisx = np.zeros((ns,(z.shape[0])**ndim),dtype=np.float64)
        gBasisy = np.zeros((ns,(z.shape[0])**ndim),dtype=np.float64)
        gBasisz = np.zeros((ns,(z.shape[0])**ndim),dtype=np.float64)
    elif info=='tet':
        p=C+1
        ns = (p+1)*(p+2)*(p+3)/6
        Basis = np.zeros((ns,w.shape[0]),dtype=np.float64)
        gBasisx = np.zeros((ns,w.shape[0]),dtype=np.float64)
        gBasisy = np.zeros((ns,w.shape[0]),dtype=np.float64)
        gBasisz = np.zeros((ns,w.shape[0]),dtype=np.float64)    
    

    if info=='hex':
        counter = 0
        for i in range(0,w.shape[0]):
            for j in range(0,w.shape[0]):
                for k in range(0,w.shape[0]):
                    ndummy = ThreeD.LagrangeGaussLobatto(C,z[i],z[j],z[k])[0]
                    dummy = ThreeD.GradLagrangeGaussLobatto(C,z[i],z[j],z[k])

                    Basis[:,counter] = ndummy[:,0]
                    gBasisx[:,counter] = dummy[:,0]
                    gBasisy[:,counter] = dummy[:,1]
                    gBasisz[:,counter] = dummy[:,2]
                    counter+=1
    elif info=='tet':
        hpBases = Tet.hpNodal.hpBases
        for i in range(0,w.shape[0]):
            # Better convergence for curved meshes when Quadrature.optimal!=0
            ndummy, dummy = hpBases(C,z[i,0],z[i,1],z[i,2],Quadrature.optimal)
            # ndummy, dummy = Tet.hpBases(C,z[i,0],z[i,1],z[i,2])
            Basis[:,i] = ndummy
            gBasisx[:,i] = dummy[:,0]
            gBasisy[:,i] = dummy[:,1]
            gBasisz[:,i] = dummy[:,2]


    class Domain(object):
        """docstring for Domain"""
        Bases = Basis
        gBasesx = gBasisx
        gBasesy = gBasisy
        gBasesz = gBasisz
            

    return Domain



def GetBasesBoundary(C,z,ndim):

    BasisBoundary = np.zeros(((C+2)**(ndim),(z.shape[0])**(ndim-1),2*ndim))
    gBasisBoundaryx = np.zeros(((C+2)**(ndim),(z.shape[0])**(ndim-1),2*ndim))
    gBasisBoundaryy = np.zeros(((C+2)**(ndim),(z.shape[0])**(ndim-1),2*ndim))
    gBasisBoundaryz = np.zeros(((C+2)**(ndim),(z.shape[0])**(ndim-1),2*ndim))

    # eps = OneD.LagrangeGaussLobatto(C,0)
    eps = np.array([-1.,1.,-1.,1.,-1.,1.])
    

    for k in range(0,eps.shape[0]):
        counter = 0
        for i in range(0,z.shape[0]):
            for j in range(0,z.shape[0]):
                if k==0 or k==1:
                    ndummy = ThreeD.LagrangeGaussLobatto(C,eps[k],z[i],z[j])[0]
                    BasisBoundary[:,counter,k] = ndummy[:,0]

                    dummy = ThreeD.GradLagrangeGaussLobatto(C,eps[k],z[i],z[j])
                    gBasisBoundaryx[:,counter,k] = dummy[:,0]
                    gBasisBoundaryy[:,counter,k] = dummy[:,1]
                    gBasisBoundaryz[:,counter,k] = dummy[:,2]

                elif k==2 or k==3:
                    ndummy = ThreeD.LagrangeGaussLobatto(C,z[i],eps[k],z[j])[0]
                    BasisBoundary[:,counter,k] = ndummy[:,0]

                    dummy = ThreeD.GradLagrangeGaussLobatto(C,z[i],eps[k],z[j])
                    gBasisBoundaryx[:,counter,k] = dummy[:,0]
                    gBasisBoundaryy[:,counter,k] = dummy[:,1]
                    gBasisBoundaryz[:,counter,k] = dummy[:,2]

                elif k==4 or k==5:
                    ndummy = ThreeD.LagrangeGaussLobatto(C,z[i],z[j],eps[k])[0]
                    BasisBoundary[:,counter,k] = ndummy[:,0]

                    dummy = ThreeD.GradLagrangeGaussLobatto(C,z[i],z[j],eps[k])
                    gBasisBoundaryx[:,counter,k] = dummy[:,0]
                    gBasisBoundaryy[:,counter,k] = dummy[:,1]
                    gBasisBoundaryz[:,counter,k] = dummy[:,2]

                
                counter+=1

    class Boundary(object):
        """docstring for BasisBoundary"""
        def __init__(self, arg):
            super(BasisBoundary, self).__init__()
            self.arg = arg
        Basis  = BasisBoundary
        gBasisx = gBasisBoundaryx
        gBasisy = gBasisBoundaryy
        gBasisz = gBasisBoundaryz


    return Boundary



def GetBasesAtNodes(C,Quadrature,info):

    ns=[]; Basis=[]; gBasisx=[]; gBasisy=[]; gBasisz=[]
    if mesh.element_type=='hex' or mesh.element_type == "quad":
        ns = (C+2)**ndim
        # GET THE BASES AT NODES INSTEAD OF GAUSS POINTS
        Basis = np.zeros((ns,w.shape[0]**ndim))
        gBasisx = np.zeros((ns,w.shape[0]**ndim))
        gBasisy = np.zeros((ns,w.shape[0]**ndim))
        gBasisz = np.zeros((ns,w.shape[0]**ndim))
    elif mesh.element_type=='tet':
        p=C+1
        ns = (p+1)*(p+2)*(p+3)/6
        # GET BASES AT NODES INSTEAD OF GAUSS POINTS
        # BE CAREFUL TAHT 4 STANDS FOR 4 VERTEX NODES (FOR HIGHER C CHECK THIS)
        Basis = np.zeros((ns,4))
        gBasisx = np.zeros((ns,4))
        gBasisy = np.zeros((ns,4))
        gBasisz = np.zeros((ns,4))
    elif mesh.element_type =='tri':
        p=C+1
        ns = (p+1)*(p+2)/2
        # GET BASES AT NODES INSTEAD OF GAUSS POINTS
        # BE CAREFUL TAHT 3 STANDS FOR 3 VERTEX NODES (FOR HIGHER C CHECK THIS)
        Basis = np.zeros((ns,3))
        gBasisx = np.zeros((ns,3))
        gBasisy = np.zeros((ns,3))


    eps=[]
    if mesh.element_type == 'hex':
        counter = 0
        eps = ThreeD.LagrangeGaussLobatto(C,0,0,0)[1]
        for i in range(0,eps.shape[0]):
            ndummy = ThreeD.LagrangeGaussLobatto(C,eps[i,0],eps[i,1],eps[i,2],arrange=1)[0]
            Basis[:,counter] = ndummy[:,0]
            dummy = ThreeD.GradLagrangeGaussLobatto(C,eps[i,0],eps[i,1],eps[i,2],arrange=1)
            gBasisx[:,counter] = dummy[:,0]
            gBasisy[:,counter] = dummy[:,1]
            gBasisz[:,counter] = dummy[:,2]
            counter+=1
    elif mesh.element_type == 'tet':
        counter = 0
        eps = np.array([
            [-1.,-1.,-1.],
            [1.,-1.,-1.],
            [-1.,1.,-1.],
            [-1.,-1.,1.]
            ])
        for i in range(0,eps.shape[0]):
            ndummy, dummy = Tet.hpBases(C,eps[i,0],eps[i,1],eps[i,2],1,1)
            ndummy = ndummy.reshape(ndummy.shape[0],1)
            Basis[:,counter] = ndummy[:,0]
            gBasisx[:,counter] = dummy[:,0]
            gBasisy[:,counter] = dummy[:,1]
            gBasisz[:,counter] = dummy[:,2]
            counter+=1
    elif mesh.element_type == 'tri':
        eps = np.array([
            [-1.,-1.],
            [1.,-1.],
            [-1.,1.]
            ])
        hpBases = Tri.hpNodal.hpBases
        for i in range(0,eps.shape[0]):
            ndummy, dummy = hpBases(C,eps[i,0],eps[i,1],1,1)
            ndummy = ndummy.reshape(ndummy.shape[0],1)
            Basis[:,i] = ndummy[:,0]
            gBasisx[:,i] = dummy[:,0]
            gBasisy[:,i] = dummy[:,1]



    class Domain(object):
        Bases = Basis
        gBasesx = gBasisx
        gBasesy = gBasisy
        gBasesz = np.zeros(gBasisx.shape)

            