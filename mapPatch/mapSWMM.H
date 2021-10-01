
template <class Type>
void mapPatches(fileNameList fromFiles, fileNameList toFiles)
{
    fileName toDir = toFiles[0];
    fileName toPoints = toFiles[1];
    fileName toFaces = toFiles[2];
    fileName toFile = toFiles[3];
    fileName swmmFile = fromFiles[0];
    fileName refFile = fromFiles[1];
    osPatches<Type> toPatches(toDir, toPoints, toFaces);

    OFstream osWrite(toDir / toFile);
    IFstream osSWMM(swmmFile);
    List<word> fromname;
    List<Type> fromvalue;
    while (!osSWMM.eof() && osSWMM.peek() != EOF)
    {
        word patchName;
        Type value;
        char end;
        osSWMM >> patchName >> value;
        osSWMM.get(end);
        Info << osSWMM.peek() << endl;
        fromname.append(patchName);
        fromvalue.append(value);
    }
    if (refFile != "no")
    {
        toPatches.getField(toDir, refFile);

        forAll(toPatches.name, vi)
        {
            forAll(fromname, ni)
            {
                if (toPatches.name[vi] == fromname[ni])
                {
                    forAll(toPatches.magSfs[vi], facei)
                    {
                        scalar per = toPatches.magSfs[vi][facei] / sum(toPatches.magSfs[vi]);
                        toPatches.values[vi][facei] = per * fromvalue[ni];
                        Info <<sum(toPatches.values[vi])<< endl;
                    }
                }
            }
        }
    }
    else
    {
        forAll(toPatches.name, vi)
        {
            forAll(fromname, ni)
            {
                if (toPatches.name[vi] == fromname[ni])
                {
                    label size = toPatches.fcs[vi].size();
                    Type value = fromvalue[ni] / size;
                    Info << value << endl;
                    Field<Type> valueito(size, value);
                    Field<Type> snGradito(size, Zero);
                    toPatches.values.append(valueito);
                    toPatches.snGrads.append(snGradito);
                }
            }
        }
    }
    //output the data.in file
    forAll(toPatches.values, vi)
    {
        forAll(toPatches.values[vi], facei)
        {
            osWrite << toPatches.values[vi][facei] << token::SPACE << toPatches.snGrads[vi][facei] << token::SPACE << 1 << nl;
        }
    }
}