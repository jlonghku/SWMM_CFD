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

defineTypeNameAndDebug(writeTimeFunctionObject, 0);

addRemovableToRunTimeSelectionTable
(
    functionObject,
    writeTimeFunctionObject,
    dictionary
);


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    // dynamicCode:
    // SHA1 = 6cc1e310a7d375e209887921effe5057155691e5
    //
    // unique function name that can be checked if the correct library version
    // has been loaded
    void writeTime_6cc1e310a7d375e209887921effe5057155691e5(bool load)
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

const fvMesh& writeTimeFunctionObject::mesh() const
{
    return refCast<const fvMesh>(obr_);
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

writeTimeFunctionObject::writeTimeFunctionObject
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

writeTimeFunctionObject::~writeTimeFunctionObject()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

bool writeTimeFunctionObject::read(const dictionary& dict)
{
    if (false)
    {
        Info<<"read writeTime sha1: 6cc1e310a7d375e209887921effe5057155691e5\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool writeTimeFunctionObject::execute()
{
    if (false)
    {
        Info<<"execute writeTime sha1: 6cc1e310a7d375e209887921effe5057155691e5\n";
    }

//{{{ begin code
    #line 83 "/home/jlong/workspace/SWMM_CFD/Case/OpenFOAM/pipe1/system/controlDict/functions/time"
const Time& runTime = mesh().time();        
            OFstream out("/home/jlong/workspace/SWMM_CFD/Case/OpenFOAM/pipe1/time.log");
            out<<runTime.value()<<" "<<runTime.deltaTValue();
//}}} end code

    return true;
}


bool writeTimeFunctionObject::write()
{
    if (false)
    {
        Info<<"write writeTime sha1: 6cc1e310a7d375e209887921effe5057155691e5\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool writeTimeFunctionObject::end()
{
    if (false)
    {
        Info<<"end writeTime sha1: 6cc1e310a7d375e209887921effe5057155691e5\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

