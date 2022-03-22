(define (domain fart)

(:types 
    character
    location
)

(:predicates 
    (atLoc ?c - character ?l - location)
)
(:action move
    :parameters (?char - character ?from ?to - location)
    :precondition (atLoc ?char ?from)
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to))
)
)