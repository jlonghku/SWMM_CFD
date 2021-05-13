
#include "fvCFD.H"
class WASP
{
    // needed:
    // mesh
    // para
    // number of algae NB
public:
    // WASP and EFDC model
    // 1.Variable Description
    // #	State variable	Acronyms	Units 	Group
    // 1	Algae	B	mg/l C	Algae
    // 2	Particulate organic carbon	POC	mg/l 	Organic carbon
    // 3	Dissolved organic carbon	DOC	mg/l
    // 4	Particulate organic phosphorus	POP	mg/l	Phosphorus
    // 5	Dissolved organic phosphorus	DOP	mg/l
    // 6	Total phosphate	PO4	mg/l
    // 7	Particulate organic nitrogen	PON	mg/l	Nitrogen
    // 8	Dissolved organic nitrogen	DON	mg/l
    // 9	Ammonia nitrogen	NH4	mg/l
    // 10	Nitrate and nitrite nitrogen	NOX	mg/l
    // 11	Particulate biogenic silica	SU	mg/l 	Silica
    // 12	Dissolved available silica	SA	mg/l
    // 13	Chemical oxygen demand	COD	mg/l	Others
    // 14	Dissolved oxygen	DO	mg/l
    // 15	Macroalgae/Periphyton	Bm	mg/l C
    // *16	Total active metal	TAM	mole/m3
    // *17	Fecal coliform bacteria	FCB	MPN/100ml

    //#############################################################
    // Tools defined
    template <class Type>
    volScalarField dz(volScalarField field)
    {
        return grad(field).component(vector::Z);
    }
    volScalarField::Internal V()
    {
        return mesh.V();
    }

    volScalarField D()
    {
        const volVectorField &P = mesh.lookupObject<volVectorField>("p");
        dimensionedScalar Pws([0 2 - 2 0 0 0 0], 101);
        return (P - Pws) / (9.81);
    }

    //############################################################

    // 2.Kinetic Equations for Algae
    List<volScalarField> B_(NB);  // B is the algal biomass of algal group x (g C/m3),
    List<volScalarField> BG_(NB); // BG is the production, basal metabolism and predation rate of algal x (g C/m3/day),
    List<volScalarField> BS_(NB); // BS is the settling rate of algal x   (g C/m3/day),
    List<volScalarField> BL_(NB); // BS is the external loads rate of algal x   (g C/m3/day),
    fvScalarMatrix Bdt(label x)
    {
        Bdt_[x] = BG(x) + BS(x) + BL(x);
        return Bdt_[x];
    }
    // 2.1 Algae production, basal metabolism and predation
    List<volScalarField> P_(NB);  // P is the production rate of algal group  (1/day),
    List<volScalarField> BM_(NB); // BM is the basal metabolism rate of algal group  (1/day),
    List<volScalarField> PR_(NB); // PR bis the predation rate of algal group  (1/day),
    // Equation 1
    volScalarField BG(label x)
    {
        BG_[x] = (P(x) - BM(x) - PR(x)) * B(x);
        return BG_[x];
    }
    // 2.1.1 Algal Growth
    List<volScalarField> PM_(NB);  // PM is the maximum growth rate under optimal conditions for algal group  (1=day),
    List<volScalarField> FIN_(NB); // FIN is the effect of suboptimal nutrient concentration (0 ≤ f1 ≤ 1),
    List<volScalarField> FIL_(NB); // FIL is the effect of suboptimal light intensity (0 ≤ f2 ≤ 1),
    List<volScalarField> FIT_(NB); // FIT is the effect of suboptimal temperature (0 ≤ f3 ≤ 1), and
    List<volScalarField> FIS_(NB); // FIS is the effect of salinity on cyanobacteria growth (0 ≤ f4 ≤ 1)
    // Equation 2
    volScalarField P(label x)
    {
        P_[x] = PM(x) * FIN(x) * FIL(x) * FIT(x) * FIS(x);
        return P_[x];
    }
    // 2.1.1.1 Effect of Nutrients on Algal Growth
    volScalarField NH4_();  // NH4 is the ammonium nitrogen concentration (g N/m3),
    volScalarField NO3_();  // NO3 is the nitrate nitrogen concentration (g N/m3),
    scalar KHN_;            // KHN is the half-saturation constant for nitrogen uptake for algal group  (g N/m3),
    volScalarField PO4d_(); // PO4d is the dissolved phosphate phosphorus concentration (g P/m3),
    scalar KHP_;            // KHP is the half-saturation constant for phosphorus uptake for algal group  (g P/m3),
    volScalarField SAd_();  // SAd is the concentration of dissolved available silica (g Si/m3),
    scalar KHS_;            // KHS is the half-saturation constant for silica uptake for algal group (g Si/m3).

    // Equation 3
    volScalarField FIN(label x)
    {
        FIN_[x] = min((NH4() + NO3()) / (KHN_[x] + NH4() + NO3()), PO4d() / (KHP_[x] + PO4d()), SAd() / (KHS_[x] + SAd()));
        return FIN_[x];
    }

    // 2.1.1.2 Effect of Light on Algal Growth
    // a.The Light Field
    scalar Keb_;            // Keb is the background light extinction (1/m),
    scalar KeISS_;          // KeISS is the light extinction coefficient for inorganic suspended solid (1/m perg/m3),
    volScalarField ISS_;    // ISS is the inorganic suspended solid concentration (g/m3) provided from the hydrodynamic model,
    scalar KeVSS_;          // KeVSS is the light extinction coefficient for volatile suspended solid (1/m perg/m3),
    volScalarField VSS_;    // VSS is the volatile suspended solid concentration (g/m3) provided from the water quality model,
    scalar KeChl_;          // KeChl is the light extinction coefficient for algae chlorophyll (1/m per mg Chl/m3),
    List<scalar> CChl_(NB); // CChlx is the carbon-to-chlorophyll ratio in algal group x (g C per mg Chl),
    scalar KeRPS_;          // KeRPS is the light extinction coefficient for rooted plant shoots (1/m per gm C/m2), and
    volScalarField RPS_;    // RPS is the concentration of plant shoots (g C per m2).
    volScalarField Kessac;  // the light extinction coefficient in the water column above the canopy
    volScalarField Kessic;  // the light extinction coefficient in the water column

    // Equation 4
    volScalarField kessac()
    {
        // B is the concentration of algae group x (g C per ml),
        Kessac_ = Keb_ + KeISS_ * ISS() + KeVSS_ * VSS() + KeChl_ * sum(B_ / CChl_);
        return Kessac_;
    }
    // Equation 5
    volScalarField kessic()
    {
        Kessic_ = Keb_ + KeISS_ * ISS() + KeVSS_ * VSS() + KeChl_ * sum(B_ / CChl_) + KeRPS_ * RPS();
        return Kessic_;
    }
    volScalarField I_; // Light intensity
    // Equation 6
    volScalarField I()
    {
        I_ = (H() ≤ H − HRPS) * Iws * exp(−Kessac() * Z);
        0 ≤ Z∗ ≤ H − HRPS;
        return I_;
    }

    // b.Steele’s Equation for Light Limitation
    List<scalar> Isx_; // Isx is the optimal light intensity for algal group x (langleys=day)
    // Equation 6
    volScalarField FIL(label x)
    {
        FIL_[x] = I() / Isx_ * exp(1− I() / Isx_);
        return FIL_[x];
    }

    // 2.1.1.3 Effect of Temperature on Algal Growth
    scalar T_;              // T is the temperature (◦C),
    List<scalar> TM1_(NB);  // TM1x is the low optimal temperature for algal growth for algal group x (◦C),
    List<scalar> TM2_(NB);  // TM2x is the high optimal temperature for algal growth for algal group x (◦C),
    List<scalar> KTG1_(NB); // KTG1x is the effect of temperature below TM1x on growth for algal group x (1/◦C2),
    List<scalar> KTG2_(NB); // KTG2x is the effect of temperature above TM2x on growth for algal group x (1/◦C2)

    List<volScalarField> FIT(label x)
    {
        if (T_ <= TM1_[x])
        {
            FIT_[x] = exp(−KTG1[x] * (T_ −TM1_[x]) ^ 2);
        }
        elif (T_ > TM1_[x] && T_ < TM2_[x])
        {
            FIT_[x] = 1;
        }
        elif (T_ > TM2_[x])
        {
            FIT_[x] = exp(−KTG2[x] * (T_ −TM2_[x]) ^ 2);
        }
        return FIT_[x];
    }

    // 2.1.1.4 Effect of Salinity on Growth of Freshwater Cyanobacteria

    List<scalar> STOXS_(NB); // STOXS is the salinity at which Microcystis x growth is halved (ppt), and
    volScalarField S_;       // S is the salinity in water column (ppt) provided from the hydrodynamic model.
    List<volScalarField> FIS(label x)
    {
        FIS_[x] = (STOXS_[x] ^ 2) / (STOXS_[x] ^ 2 + S_ ^ 2);

        return FIS_[x];
    }
    // 2.1.2 Algal Basal Metabolism
    // 2.1.2.1 Effect of Temperature on Algal Basal Metabolism
    List<scalar> BMR_(NB); // BMRx is the basal metabolism rate at TRxfor algal group x (1=day),
    List<scalar> KTB_(NB); // KTB is the effect of temperature on metabolism for algal group x (1/◦C), and
    List<scalar> TR_(NB);  // TR is the reference temperature for basal metabolism for algal group x (◦C)
    List<volScalarField> BM(label x)
    {
        BM_[x] = BMR_[x] * exp(KTB_[x] * (T_ −TR_[x]));
        return BM_[x];
    }
    // 2.1.3 Algal Predation
    // 2.1.3.1 Effect of Algal Biomass and Temperature on Algal Predation
    List<scalar> PRR_(NB); // PRR is the reference predation rate at BxP and TRx for algal group x (1=day),
    List<scalar> BP_(NB);  // BP is the reference algae concentration for predation (g C=m3),
    scalar aP;             // aP is the exponential dependence factor, and
    List<scalar> KTP_(NB); // KTP is the effect of temperature on predation for algal group x (1/◦C)
    //List<scalar> TP_;  // TR is the reference temperature for basal metabolism for algal group x (◦C)
    List<volScalarField> PR_(NB, zero);
    List<volScalarField> PR(label x)
    {
        if (PR_[x] == zero)
        {
            PR_[x] = PRR_[x] * (B(x) / BP_[x]) ^ aP * exp(KTP_[x] * (T_ - TR_[x]));
        }
        return PR_[x];
    }

    // 2.2 Algal Settling
    List<scalar> WS_(NB); // WS is the positive settling velocity of algal group  (m/day),
    volScalarField BS(label x)
    {
        BS_[x] = dz(WS_[x] * B(x));
        return BS_[x];
    }
    // 2.3 External loads
    List<volScalarField> WB_(NB); // WB is the external loads of algal group x (g C/day), and
    volScalarField BL(label x)
    {
        BL_[x] = WB(x) / V();
        return BL_[x];
    }

// 3.Kinetic Equations for Organic Carbon

// 3.1 Particulate Organic Carbon

// 3.2 Dissolved Organic Carbon

/home/jlong/couof /home/jlong/codetest /home/jlong/backup/inp_new /opt/openfoam8/src/finiteVolume/fields/fvPatchFields/derived/externalCoupledMixedNew /home/jlong/backup/Case1/OpenFOAM/openfoamcase
};