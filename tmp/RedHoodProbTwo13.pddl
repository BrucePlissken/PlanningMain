(define (problem ridin) (:domain lrrh)
(:objects
    littleRedRidingHood grandma bigBadWolf lumberJack - character
    home woods grandmasHouse - location
)
(:init
    (atloc grandma grandmashouse)
    (atloc bigbadwolf woods)
    (isconnected home woods)
    (isconnected woods grandmashouse)
    (haveaxe lumberjack)
    (caneat bigbadwolf)
    (cantmove grandma)
    (unaware bigbadwolf grandmashouse)
    (unaware bigbadwolf home)
    (areenemies lumberjack bigbadwolf)
    (atloc littleredridinghood woods)
    (atloc lumberjack grandmashouse)
    (isdead littleredridinghood)
    (cantmove bigbadwolf)
    (isswallowed littleredridinghood bigbadwolf)
)
(:goal
    (and (atloc littleredridinghood grandmashouse))
  )
)