#include "fvCFD.H"
#include "patchToPatchInterpolation.H"
#include "runinfo.H"

#include <unistd.h>
#include <fcntl.h>
#include <semaphore.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <iostream>
#include "runinfo.H"
#define MAXSOL 10 //maximum number of solvers

fvMesh readMesh(int argc, char *argv[])
{
    #include "setRootCaseLists.H"
    #include "createTime.H"
 
    #include "createMesh.H"
    
}
int main(int argc, char *argv[])
{
    runinfo info(argc, argv);

    label a = 0;

    info.getinfo("case");
  
    // PtrList<fvMesh> meshes = cv(argc, argv);
    //info.getinfo("case1");
    //fvMesh mesh1 = cv(info.argcc, info.argvv);
    PrimitivePatch<SubList<face>, const pointField&> 
    patchToPatchInterpolation  interpolator2d3d(
        meshes.boundaryMesh()[a],
        meshes.boundaryMesh()[a] // to patch
    );

    // vectorField UUU = interpolator2d3d.faceInterpolate<vector>(U.boundaryField()[a]);
    //UU.boundaryField()[a] = UUU;

    // Info << "U3dPatch = " << U.boundaryField()[a] << endl;
    
    return 0;
}