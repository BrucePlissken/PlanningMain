(define (problem OVERHERE) (:domain cpd)
(:objects
    Cewmann_village manor_Cewmann_village house_4_Cewmann_village house_3_Cewmann_village house_2_Cewmann_village house_1_Cewmann_village farm_4_Cewmann_village farm_3_Cewmann_village farm_2_Cewmann_village farm_1_Cewmann_village shop_2_Cewmann_village shop_1_Cewmann_village inn_1_Cewmann_village Wellspring_village church_Wellspring_village house_3_Wellspring_village house_2_Wellspring_village house_1_Wellspring_village farm_5_Wellspring_village farm_4_Wellspring_village farm_3_Wellspring_village farm_2_Wellspring_village farm_1_Wellspring_village shop_2_Wellspring_village shop_1_Wellspring_village Sherfield_village manor_Sherfield_village house_4_Sherfield_village house_3_Sherfield_village house_2_Sherfield_village house_1_Sherfield_village farm_3_Sherfield_village farm_2_Sherfield_village farm_1_Sherfield_village Kilkenny_forrest - location
    Elegia Vincenta Alibert Hildegod Ermenbert Joan-Stephanie Waldeger Sighilde Olivera Haelcar Demetrius Ermentaria Berthold Honest Sabata Herois Honorius Gilbald Kale Walrich Wilbald Thecla Piat Urith Wojslav Engelmar Ansgot Gautlinde Wigand Calvo Aldhelm Maenwallon Hudrich Micah Clemence Eckrich Eloise Godo Beauvis Plena Victoria Eleanor Sumarlidi Madalulf Abba Caesar Herzog Antelm Theodore Maol Sicleramna Framengilde Drew Cynthius Bertbert Wojciech Sclavo Deurhoiarn Godwi Regalis - character
    Carla - agent
 )
(:init
    (atloc manor_Cewmann_village Cewmann_village)
    (atloc house_4_Cewmann_village Cewmann_village)
    (atloc house_3_Cewmann_village Cewmann_village)
    (atloc house_2_Cewmann_village Cewmann_village)
    (atloc house_1_Cewmann_village Cewmann_village)
    (atloc farm_4_Cewmann_village Cewmann_village)
    (atloc farm_3_Cewmann_village Cewmann_village)
    (atloc farm_2_Cewmann_village Cewmann_village)
    (atloc farm_1_Cewmann_village Cewmann_village)
    (atloc shop_2_Cewmann_village Cewmann_village)
    (atloc shop_1_Cewmann_village Cewmann_village)
    (atloc inn_1_Cewmann_village Cewmann_village)
    (atloc church_Wellspring_village Wellspring_village)
    (atloc house_3_Wellspring_village Wellspring_village)
    (atloc house_2_Wellspring_village Wellspring_village)
    (atloc house_1_Wellspring_village Wellspring_village)
    (atloc farm_5_Wellspring_village Wellspring_village)
    (atloc farm_4_Wellspring_village Wellspring_village)
    (atloc farm_3_Wellspring_village Wellspring_village)
    (atloc farm_2_Wellspring_village Wellspring_village)
    (atloc farm_1_Wellspring_village Wellspring_village)
    (atloc shop_2_Wellspring_village Wellspring_village)
    (atloc shop_1_Wellspring_village Wellspring_village)
    (atloc manor_Sherfield_village Sherfield_village)
    (atloc house_4_Sherfield_village Sherfield_village)
    (atloc house_3_Sherfield_village Sherfield_village)
    (atloc house_2_Sherfield_village Sherfield_village)
    (atloc house_1_Sherfield_village Sherfield_village)
    (atloc farm_3_Sherfield_village Sherfield_village)
    (atloc farm_2_Sherfield_village Sherfield_village)
    (atloc farm_1_Sherfield_village Sherfield_village)
    (whereabouts manor_Cewmann_village Elegia)
    (whereabouts house_3_Cewmann_village Vincenta)
    (whereabouts house_3_Cewmann_village Alibert)
    (whereabouts house_3_Cewmann_village Hildegod)
    (whereabouts house_2_Cewmann_village Ermenbert)
    (whereabouts house_2_Cewmann_village Joan-Stephanie)
    (whereabouts house_2_Cewmann_village Waldeger)
    (whereabouts house_2_Cewmann_village Sighilde)
    (whereabouts house_1_Cewmann_village Olivera)
    (whereabouts house_1_Cewmann_village Haelcar)
    (whereabouts house_1_Cewmann_village Demetrius)
    (whereabouts house_1_Cewmann_village Ermentaria)
    (whereabouts farm_2_Cewmann_village Berthold)
    (whereabouts farm_2_Cewmann_village Honest)
    (whereabouts farm_1_Cewmann_village Sabata)
    (whereabouts farm_1_Cewmann_village Herois)
    (whereabouts shop_2_Cewmann_village Honorius)
    (whereabouts shop_2_Cewmann_village Gilbald)
    (whereabouts shop_1_Cewmann_village Kale)
    (whereabouts church_Wellspring_village Walrich)
    (whereabouts church_Wellspring_village Wilbald)
    (whereabouts church_Wellspring_village Thecla)
    (whereabouts house_3_Wellspring_village Piat)
    (whereabouts house_2_Wellspring_village Urith)
    (whereabouts house_1_Wellspring_village Wojslav)
    (whereabouts farm_5_Wellspring_village Engelmar)
    (whereabouts farm_5_Wellspring_village Ansgot)
    (whereabouts farm_5_Wellspring_village Gautlinde)
    (whereabouts farm_5_Wellspring_village Wigand)
    (whereabouts farm_4_Wellspring_village Calvo)
    (whereabouts farm_4_Wellspring_village Aldhelm)
    (whereabouts farm_4_Wellspring_village Maenwallon)
    (whereabouts farm_3_Wellspring_village Hudrich)
    (whereabouts farm_3_Wellspring_village Micah)
    (whereabouts farm_2_Wellspring_village Clemence)
    (whereabouts farm_2_Wellspring_village Eckrich)
    (whereabouts farm_1_Wellspring_village Eloise)
    (whereabouts farm_1_Wellspring_village Godo)
    (whereabouts farm_1_Wellspring_village Beauvis)
    (whereabouts shop_1_Wellspring_village Plena)
    (whereabouts shop_1_Wellspring_village Victoria)
    (whereabouts manor_Sherfield_village Eleanor)
    (whereabouts manor_Sherfield_village Sumarlidi)
    (whereabouts manor_Sherfield_village Madalulf)
    (whereabouts manor_Sherfield_village Abba)
    (whereabouts house_4_Sherfield_village Caesar)
    (whereabouts house_4_Sherfield_village Herzog)
    (whereabouts house_3_Sherfield_village Antelm)
    (whereabouts house_3_Sherfield_village Theodore)
    (whereabouts house_3_Sherfield_village Maol)
    (whereabouts house_3_Sherfield_village Sicleramna)
    (whereabouts house_2_Sherfield_village Framengilde)
    (whereabouts house_2_Sherfield_village Drew)
    (whereabouts house_2_Sherfield_village Cynthius)
    (whereabouts house_1_Sherfield_village Bertbert)
    (whereabouts house_1_Sherfield_village Wojciech)
    (whereabouts farm_3_Sherfield_village Sclavo)
    (whereabouts farm_3_Sherfield_village Deurhoiarn)
    (whereabouts farm_3_Sherfield_village Godwi)
    (whereabouts farm_2_Sherfield_village Regalis)
    (whereabouts farm_2_Sherfield_village Carla)
)
(:goal
    (and
        (isdead Godo)
    )
)
)