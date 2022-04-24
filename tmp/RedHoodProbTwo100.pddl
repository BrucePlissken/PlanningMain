(define (problem ridin) (:domain lrrh)
(:objects
    littleRedRidingHood grandma bigBadWolf lumberJack - character
    home woods grandmasHouse - location
)
(:init
    (atloc littleredridinghood home)
    (atloc grandma grandmashouse)
    (atloc bigbadwolf woods)
    (isconnected home woods)
    (isconnected woods grandmashouse)
    (isconnected grandmashouse woods)
    (haveaxe lumberjack)
    (caneat bigbadwolf)
    (cantmove grandma)
    (unaware bigbadwolf grandmashouse)
    (unaware bigbadwolf home)
    (areenemies lumberjack bigbadwolf)
    (atloc lumberjack home)
    (isdead littleredridinghood)
)
(:goal
    (and (isdead littleredridinghood))
  )
)