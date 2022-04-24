(define (problem OVERHERE) (:domain cpd)
(:objects
    Cewmann_village manor_Cewmann_village house_4_Cewmann_village house_3_Cewmann_village house_2_Cewmann_village house_1_Cewmann_village farm_4_Cewmann_village farm_3_Cewmann_village farm_2_Cewmann_village farm_1_Cewmann_village shop_2_Cewmann_village shop_1_Cewmann_village inn_1_Cewmann_village Wellspring_village church_Wellspring_village house_3_Wellspring_village house_2_Wellspring_village house_1_Wellspring_village farm_5_Wellspring_village farm_4_Wellspring_village farm_3_Wellspring_village farm_2_Wellspring_village farm_1_Wellspring_village shop_2_Wellspring_village shop_1_Wellspring_village Sherfield_village manor_Sherfield_village house_4_Sherfield_village house_3_Sherfield_village house_2_Sherfield_village house_1_Sherfield_village farm_3_Sherfield_village farm_2_Sherfield_village farm_1_Sherfield_village Kilkenny_forrest - location
    Elegia Vincenta Alibert Hildegod Ermenbert Joan-Stephanie Waldeger Sighilde Olivera Haelcar Demetrius Ermentaria Berthold Honest Sabata Herois Honorius Gilbald Kale Walrich Wilbald Thecla Piat Urith Wojslav Engelmar Ansgot Gautlinde Wigand Calvo Aldhelm Maenwallon Hudrich Micah Clemence Eckrich Eloise Godo Beauvis Plena Victoria Eleanor Sumarlidi Madalulf Abba Caesar Herzog Antelm Theodore Maol Sicleramna Framengilde Drew Cynthius Bertbert Wojciech Sclavo Deurhoiarn Godwi Regalis - character
    Carla - agent
 )
(:init
    (atloc manor_cewmann_village cewmann_village)
    (atloc house_4_cewmann_village cewmann_village)
    (atloc house_3_cewmann_village cewmann_village)
    (atloc house_2_cewmann_village cewmann_village)
    (atloc house_1_cewmann_village cewmann_village)
    (atloc farm_4_cewmann_village cewmann_village)
    (atloc farm_3_cewmann_village cewmann_village)
    (atloc farm_2_cewmann_village cewmann_village)
    (atloc farm_1_cewmann_village cewmann_village)
    (atloc shop_2_cewmann_village cewmann_village)
    (atloc shop_1_cewmann_village cewmann_village)
    (atloc inn_1_cewmann_village cewmann_village)
    (atloc church_wellspring_village wellspring_village)
    (atloc house_3_wellspring_village wellspring_village)
    (atloc house_2_wellspring_village wellspring_village)
    (atloc house_1_wellspring_village wellspring_village)
    (atloc farm_5_wellspring_village wellspring_village)
    (atloc farm_4_wellspring_village wellspring_village)
    (atloc farm_3_wellspring_village wellspring_village)
    (atloc farm_2_wellspring_village wellspring_village)
    (atloc farm_1_wellspring_village wellspring_village)
    (atloc shop_2_wellspring_village wellspring_village)
    (atloc shop_1_wellspring_village wellspring_village)
    (atloc manor_sherfield_village sherfield_village)
    (atloc house_4_sherfield_village sherfield_village)
    (atloc house_3_sherfield_village sherfield_village)
    (atloc house_2_sherfield_village sherfield_village)
    (atloc house_1_sherfield_village sherfield_village)
    (atloc farm_3_sherfield_village sherfield_village)
    (atloc farm_2_sherfield_village sherfield_village)
    (atloc farm_1_sherfield_village sherfield_village)
    (whereabouts manor_cewmann_village elegia)
    (whereabouts house_3_cewmann_village vincenta)
    (whereabouts house_3_cewmann_village alibert)
    (whereabouts house_3_cewmann_village hildegod)
    (whereabouts house_2_cewmann_village ermenbert)
    (whereabouts house_2_cewmann_village joan-stephanie)
    (whereabouts house_2_cewmann_village waldeger)
    (whereabouts house_2_cewmann_village sighilde)
    (whereabouts house_1_cewmann_village olivera)
    (whereabouts house_1_cewmann_village haelcar)
    (whereabouts house_1_cewmann_village demetrius)
    (whereabouts house_1_cewmann_village ermentaria)
    (whereabouts farm_2_cewmann_village berthold)
    (whereabouts farm_2_cewmann_village honest)
    (whereabouts farm_1_cewmann_village sabata)
    (whereabouts farm_1_cewmann_village herois)
    (whereabouts shop_2_cewmann_village honorius)
    (whereabouts shop_2_cewmann_village gilbald)
    (whereabouts shop_1_cewmann_village kale)
    (whereabouts church_wellspring_village walrich)
    (whereabouts church_wellspring_village wilbald)
    (whereabouts church_wellspring_village thecla)
    (whereabouts house_3_wellspring_village piat)
    (whereabouts house_2_wellspring_village urith)
    (whereabouts house_1_wellspring_village wojslav)
    (whereabouts farm_5_wellspring_village engelmar)
    (whereabouts farm_5_wellspring_village ansgot)
    (whereabouts farm_5_wellspring_village gautlinde)
    (whereabouts farm_5_wellspring_village wigand)
    (whereabouts farm_4_wellspring_village calvo)
    (whereabouts farm_4_wellspring_village aldhelm)
    (whereabouts farm_4_wellspring_village maenwallon)
    (whereabouts farm_3_wellspring_village hudrich)
    (whereabouts farm_3_wellspring_village micah)
    (whereabouts farm_2_wellspring_village clemence)
    (whereabouts farm_2_wellspring_village eckrich)
    (whereabouts farm_1_wellspring_village eloise)
    (whereabouts farm_1_wellspring_village godo)
    (whereabouts farm_1_wellspring_village beauvis)
    (whereabouts shop_1_wellspring_village plena)
    (whereabouts shop_1_wellspring_village victoria)
    (whereabouts manor_sherfield_village eleanor)
    (whereabouts manor_sherfield_village sumarlidi)
    (whereabouts manor_sherfield_village madalulf)
    (whereabouts manor_sherfield_village abba)
    (whereabouts house_4_sherfield_village caesar)
    (whereabouts house_4_sherfield_village herzog)
    (whereabouts house_3_sherfield_village antelm)
    (whereabouts house_3_sherfield_village theodore)
    (whereabouts house_3_sherfield_village maol)
    (whereabouts house_3_sherfield_village sicleramna)
    (whereabouts house_2_sherfield_village framengilde)
    (whereabouts house_2_sherfield_village drew)
    (whereabouts house_2_sherfield_village cynthius)
    (whereabouts house_1_sherfield_village bertbert)
    (whereabouts house_1_sherfield_village wojciech)
    (whereabouts farm_3_sherfield_village sclavo)
    (whereabouts farm_3_sherfield_village deurhoiarn)
    (whereabouts farm_3_sherfield_village godwi)
    (whereabouts farm_2_sherfield_village regalis)
    (whereabouts farm_2_sherfield_village carla)
)
(:goal
    (and
        (isdead Godo)
    )
)
)