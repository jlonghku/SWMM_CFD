/*---------------------------------------------------------------------------*  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "functionObjectTemplate.H"
#include "fvCFD.H"
#include "unitConversion.H"
#include "addToRunTimeSelectionTable.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

defineTypeNameAndDebug(getDeltaTFunctionObject, 0);

addRemovableToRunTimeSelectionTable
(
    functionObject,
    getDeltaTFunctionObject,
    dictionary
);


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    // dynamicCode:
    // SHA1 = 3653b5de919e30f64394a6eb9abbe8c5f0fe6442
    //
    // unique function name that can be checked if the correct library version
    // has been loaded
    void getDeltaT_3653b5de919e30f64394a6eb9abbe8c5f0fe6442(bool load)
    {
        if (load)
        {
            // code that can be explicitly executed after loading
        }
        else
        {
            // code that can be explicitly executed before unloading
        }
    }
}


// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * Private Member Functions  * * * * * * * * * * * //

const fvMesh& getDeltaTFunctionObject::mesh() const
{
    return refCast<const fvMesh>(obr_);
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

getDeltaTFunctionObject::getDeltaTFunctionObject
(
    const word& name,
    const Time& runTime,
    const dictionary& dict
)
:
    functionObjects::regionFunctionObject(name, runTime, dict)
{
    read(dict);
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

getDeltaTFunctionObject::~getDeltaTFunctionObject()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

bool getDeltaTFunctionObject::read(const dictionary& dict)
{
    if (false)
    {
        Info<<"read getDeltaT sha1: 3653b5de919e30f64394a6eb9abbe8c5f0fe6442\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool getDeltaTFunctionObject::execute()
{
    if (false)
    {
        Info<<"execute getDeltaT sha1: 3653b5de919e30f64394a6eb9abbe8c5f0fe6442\n";
    }

//{{{ begin code
    #line 89 "/home/jlong/workspace/SWMM_CFD/Case/OpenFOAM/pipe1/system/controlDict/functions/timeStep"
const Time& runTime = mesh().time();
            scalar deltaTt=runTime.deltaT().value();
            OFstream out("./deltaT");
            out<<deltaTt<<"TIME:"<<runTime.value();
//}}} end code

    return true;
}


bool getDeltaTFunctionObject::write()
{
    if (false)
    {
        Info<<"write getDeltaT sha1: 3653b5de919e30f64394a6eb9abbe8c5f0fe6442\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool getDeltaTFunctionObject::end()
{
    if (false)
    {
        Info<<"end getDeltaT sha1: 3653b5de919e30f64394a6eb9abbe8c5f0fe6442\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

