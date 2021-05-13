#include "fvCFD.H"
#include "patchToPatchInterpolation.H"
//#include "IFstreamN.H"
#include "osPatches.H"
#include "mapPatches.H"

int main(int argc, char *argv[])
{
    // addoptions
    //argList::initValidTables::clear();
    argList::addOption("fromFiles", "filenames", "from patch files");
    argList::addOption("toFiles", "filenames", "to patch files");
    argList::addOption("from", "filename", "from file");
    argList::addOption("to", "filename", "to file");
    argList::addBoolOption("v", "vector patchfield");
    argList::addBoolOption("s", "scalar patchfield");
    argList::addBoolOption("f", "file only");
    argList args(argc, argv);
    //get options
    fileNameList fromFiles = args.optionLookupOrDefault<fileNameList>("fromFiles", {args.path(), "patchPoints", "patchFaces", "data.out"});
    fileNameList toFiles = args.optionLookupOrDefault<fileNameList>("toFiles", {args.path(), "patchPoints", "patchFaces", "data.in"});
    if( args.optionFound("f"))
    {
        fileName from = args.optionLookupOrDefault<fileName>("from", "data.out");
        fileName to = args.optionLookupOrDefault<fileName>("to", "data.in");
        fromFiles[3] = from;
        toFiles[3] = to;
    }

    if (args.optionFound("v"))
    {
        mapPatches<vector>(fromFiles, toFiles);
    }
    else
    {
        mapPatches<scalar>(fromFiles, toFiles);
    }

    Info << "mapPatch Completed!" << endl;
    return 0;
}