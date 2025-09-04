typedef PrimitivePatch<faceList, pointField> CPatch;
// data from data.out file
template <class Type>
void mapPatches(fileNameList fromFiles, fileNameList toFiles)
{

    //create toPatches file
    fileName toDir = toFiles[0];
    fileName toPoints = toFiles[1];
    fileName toFaces = toFiles[2];
    fileName toFile = toFiles[3];
    osPatches<Type> toPatches(toDir, toPoints, toFaces);
    OFstream osWrite(toDir / toFile);

    //use from files

    fileName fromDir = fromFiles[0];
    fileName fromPoints = fromFiles[1];
    fileName fromFaces = fromFiles[2];
    fileName fromFile = fromFiles[3];
    Info << "Reading data from: " << fromFile << nl;
    osPatches<Type> fromPatches(fromDir, fromPoints, fromFaces);
    fromPatches.getField(fromDir, fromFile);

    //get patches
    forAll(toPatches.names, vi)
    {
        label fromid = fromPatches.findID(toPatches.names[vi]);
        Info << "Mapping Patch: " << toPatches.names[vi] << nl;
        if (fromid >= 0)
        {
            CPatch fromPatch(fromPatches.fcs[fromid], fromPatches.pts[fromid]);
            CPatch toPatch(toPatches.fcs[vi], toPatches.pts[vi]);
            PatchToPatchInterpolation<CPatch, CPatch>
                interpolator(fromPatch, toPatch);

            Field<Type> valueito = interpolator.faceInterpolate<Type>(fromPatches.values[fromid]);
            Field<Type> snGradito = interpolator.faceInterpolate<Type>(fromPatches.snGrads[fromid]);

            toPatches.values.append(valueito);
            toPatches.snGrads.append(snGradito);
        }
    }

    //output the data.in file
    Info << "Writing data to: " << toFile << nl;
    forAll(toPatches.values, vi)
    {
        forAll(toPatches.values[vi], facei)
        {
            osWrite << toPatches.values[vi][facei] << token::SPACE << toPatches.snGrads[vi][facei] << token::SPACE << 1 << nl;
        }
    }
}
