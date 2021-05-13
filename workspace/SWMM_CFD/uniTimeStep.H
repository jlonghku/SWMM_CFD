vector b(1, 1, 1);

const Time &runTime = mesh().time();
//OFstream osW("Time_" + Foam::name(runTime.value()) + ".out");
//osW << "jlong" << runTime.value() << nl;
Info << "jlong" << runTime.value() << nl;
//const volVectorField &p = mesh().lookupObject<volVectorField>("p");
const volVectorField &U = mesh().lookupObject<volVectorField>("U");
//volVectorField pp=p.clone();

 fvVectorMatrix UUEqn
        (
            fvm::ddt(U)
          
          
        );
/*
if (Pstream::master())
{
    sleep(3);
}
*/