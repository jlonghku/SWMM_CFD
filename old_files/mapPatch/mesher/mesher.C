#include "fvCFD.H"
#include "osPatch"
typedef PrimitivePatch<faceList, pointField> CPatch;
int main(int argc, char *argv[])
{
    // addoptions
    //argList::initValidTables::clear();
    argList::addOption("fromFiles", "filenames", "from patch files");
    argList::addOption("toFiles", "filenames", "to patch files");

    argList args(argc, argv);
    //get options
    fileNameList fromFiles = args.optionLookupOrDefault<fileNameList>("fromFiles", {args.path(), "patchPoints", "patchFaces"});
    fileNameList toFiles = args.optionLookupOrDefault<fileNameList>("toFiles", {args.path(), "patchPoints", "patchFaces"});
    fileName p = argv[1];
    fileName f = argv[2];
    fileName pf = argv[3];
    IFstream osPoints(args.path() / pf);
    List<word> names;
    List<pointField> pts;
    while (!osPoints.eof())
    {

        char ch;
        word namei;
        pointField ptsi;
        osPoints.get(ch);
        osPoints >> namei >> namei >> ptsi >> ch;
        names.append(namei);
        pts.append(ptsi);
    }

    osPatch pat(args.path(), p, f);
    for (int i = 0; i < pat.fcs.size(); i++)
    {
        CPatch patch(pat.fcs[i], pat.pts[i]);
        PrimitivePatchInterpolation interpatch(patch);
        interpatch.pointToFaceInterpolate(pts[i]);
    }

    Info << "mapPatch Completed!" << endl;
    return 0;
}