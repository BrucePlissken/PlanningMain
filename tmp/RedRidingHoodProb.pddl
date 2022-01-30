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
    (knowInfo littleRedRidingHood home)
    (knowInfo littleRedRidingHood woods)
    (knowInfo littleRedRidingHood grandmasHouse)
    (knowInfo bigBadWold woods)
    (knowInfo lumberJack woods)
    (knowInfo lumberJack grandmasHouse)
    (areEnemies lumberJack bigBadWolf)
)
(:goal
    (isswallowed grandma bigbadwolf)
  )
)