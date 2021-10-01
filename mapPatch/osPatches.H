template <class Type>
class osPatches
{
public:
    label size = 0;
    List<word> names;
    List<pointField> pts;
    List<faceList> fcs;
    List<Field<scalar>> magSfs;
    List<Field<Type>> values;
    List<Field<Type>> snGrads;
    osPatches()
    {
    }
    osPatches(fileName dir, fileName points, fileName faces)
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

    void getField(word fromDir, word filename)
    {
        IFstream osField(fromDir / filename);

        magSfs.resize(size);
        values.resize(size);
        snGrads.resize(size);
        scalar fieldSize=0;
        word wtmp;

        while (!osField.eof() && osField.peek() != EOF&&fieldSize<size)
        {
            word patchName, patchType;
            osField >> patchName;
            osField >> patchType;

            label namei = findID(patchName);

            label n = fcs[namei].size();
            Field<scalar> magSf(n);
            Field<Type> value(n);
            Field<Type> snGrad(n);
            
            forAll(value, i)
            {
                osField >> value[i] >> snGrad[i] >> magSf[i];
            }
            
            magSfs[namei] = magSf;
            values[namei] = value;
            snGrads[namei] = snGrad;
            fieldSize+=1;
        }
    };
};