class osPatch
{
public:
    label size = 0;
    List<word> names;
    List<pointField> pts;
    List<faceList> fcs;

    osPatch()
    {
    }
    osPatch(fileName dir, fileName points, fileName faces)
    {
        IFstream osPoints(dir / points);
        IFstream osFaces(dir / faces);
        //osPatches fromPatch;
        word patchKey;
        char end;
        while (!osPoints.eof())
        {
            word namei;
            pointField ptsi;
            osPoints.get(end);
            osPoints >> patchKey >> namei >> ptsi >> end;
            names.append(namei);
            pts.append(ptsi);
        }

        while (!osFaces.eof())
        {
            word namei;
            faceList fcsi;
            osFaces.get(end);
            osFaces >> patchKey >> namei >> fcsi >> end;
            //names.append(namei);
            fcs.append(fcsi);
            size += 1;
        }
    }

    label findID(word patchName)
    {
        forAll(names, namei)
        {
            if (names[namei] == patchName)
            {
                return namei;
            }
        }
        return -1;
    }
   
};

