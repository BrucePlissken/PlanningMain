(define (problem ridin) (:domain lrrh)
(:objects
    littleRedRidingHood grandma bigBadWolf lumberJack - character
    home woods grandmasHouse - location
)
(:init
    (atLoc littleRedRidingHood home)
    (atLoc grandma grandmasHouse)
    (atLoc bigBadWolf woods)
    (atLoc lumberJack woods)
    (isConnected home woods)
    (isConnected woods grandmasHouse)
    (haveAxe lumberJack)
    (canEat bigBadWolf)
    (cantMove grandma)
    (unaware bigBadWolf grandmasHouse)
    (unaware bigBadWolf home)
    (areEnemies lumberJack bigBadWolf)
)
(:goal
    (and (isSaved grandma)
        (isSaved littleRedRidingHood))
  )
)