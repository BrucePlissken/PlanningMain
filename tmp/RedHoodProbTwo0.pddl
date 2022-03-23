(define (problem ridin) (:domain lrrh)
(:objects
    littleRedRidingHood grandma bigBadWolf lumberJack - character
    home woods grandmasHouse - location
)
(:init
    (atloc littleredridinghood home)
    (atloc grandma grandmashouse)
    (atloc bigbadwolf woods)
    (atloc lumberjack woods)
    (isconnected home woods)
    (isconnected woods grandmashouse)
    (haveaxe lumberjack)
    (caneat bigbadwolf)
    (cantmove grandma)
    (unaware bigbadwolf grandmashouse)
    (unaware bigbadwolf home)
    (areenemies lumberjack bigbadwolf)
)
(:goal
    (and (not (atloc bigbadwolf home))
)
  )
)