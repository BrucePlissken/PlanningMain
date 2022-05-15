(define (problem OVERHERE) (:domain cpd)
(:objects
    Ermentaria - agent
    Vincenta Regalis - character
    house_1_Cewmann_village house_3_Cewmann_village farm_2_Sherfield_village - location
    stick_49 dagger_43 - weapon
    crusifix_17 - item
)
(:init
    (whereabouts house_1_Cewmann_village Ermentaria)
    (inventory stick_49 Vincenta)
    (whereabouts house_3_Cewmann_village Vincenta)
    (inventory dagger_43 Regalis)
    (inventory crusifix_17 Regalis)
    (whereabouts farm_2_Sherfield_village Regalis)
)
(:goal
    (and
        (inventory crusifix_22 Maol)
    )
)
)