(define (domain ballbot)

 (:types
    room
    ball
    gripper
 )

 (:predicates
    (atrobby ?l - room)
    (atball ?b - ball ?l - room)
    (free ?g - gripper) 
    (carry ?g - gripper ?b - ball)
    )

 (:action move 
    :parameters     (?from - room ?to - room)
    :precondition   (atrobby ?from)
    :effect         (and (atrobby ?to)
                     (not (atrobby ?from)) ))

 (:action pick 
    :parameters (?b - ball ?l - room ?g - gripper)
    :precondition (and (atball ?b ?l) (atrobby ?l) (free ?g))
    :effect (and (carry ?g ?b)
                  (not (atball ?b ?l)) (not (free ?g)) ))

 (:action drop 
    :parameters (?b - ball ?l - room ?g - gripper)
    :precondition (and (atrobby ?l) (carry ?g ?b))
    :effect (and (atball ?b ?l)
                  (free ?g)
                  (not (carry ?g ?b)) ))
)