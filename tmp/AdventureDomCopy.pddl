(define (domain adc)
(:requirements :universal-preconditions :disjunctive-preconditions :quantified-preconditions :typing :equality :negative-preconditions :conditional-effects)
(:types
    concept monster location character - info
    player npc - character
    site area - location
    consumable weapon trophy item - thing
)

(:predicates
    (atLoc ?char - character ?loc - location)
    (onGround ?i - thing ?loc - location)
    (canTrack ?char - character)
    (havething ?char - character ?i - thing)
    (inArea ?site - location ?area - area)
    (trackInfo ?inf - info ?loc - location ?lair - location)
    (isSus ?char - character)
    (isAvailable ?char - character)
    (isDead ?char - character)
    (isBound ?char - character)
    (haveBodyPart ?char - character ?bp - trophy)
    (follows ?follower ?leader - character)
    (isMonster ?char - character ?typi - monster ?inf - info)
    (isMissing ?char - character)
    (isLair ?char - character ?loc - location)
    (isDestination ?char - character ?loc - location)
    (canCut ?thing - thing)
    (knowInfo ?char - character ?omni - info)
    (isUnknown ?omni - info)
)
(:functions
    (total-cost) - number
)
(:action move
    :parameters (?char - player ?from - location ?to - site ?area - area)
    :precondition (and (atLoc ?char ?from) (not (isUnknown ?to)) (isAvailable ?char) (inArea ?to ?area) (or (= ?from ?area) (inArea ?from ?area)) )
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to)
    (forall (?follower - character) (when (follows ?follower ?char) (and (atLoc ?follower ?to) (not (atLoc ?follower ?from))) ))
    )
)
(:action travel
    :parameters (?char - player ?from - location ?to - area)
    :precondition (and (atLoc ?char ?from) (not (isUnknown ?to)) (isAvailable ?char))
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to)
    (forall (?follower - character) (when (follows ?follower ?char) (and (atLoc ?follower ?to) (not (atLoc ?follower ?from))) ))
    )
)
(:action investigatetrack
    :parameters (?char - character ?inf - info ?loc ?lair - location)
    :precondition (and (atLoc ?char ?loc) (canTrack ?char) (trackInfo ?inf ?loc ?lair) (isAvailable ?char) (not (isUnknown ?inf)))
    :effect (and (not (isUnknown ?lair))
    )
)
(:action slay
    :parameters (?char1 - player ?char2 - character ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (isSus ?char2) (isAvailable ?char1) (not (= ?char1 ?char2)))
    :effect (and (isDead ?char2)
    (forall (?i - thing) (when (havething ?char2 ?i) (and (onGround ?i ?loc) (not (havething ?char2 ?i)))))
    )
)
(:action gowith
    :parameters (?follower ?leader - character ?loc - location)
    :precondition (and (atLoc ?leader ?loc) (atLoc ?follower ?loc) (isAvailable ?follower) (not (= ?follower ?leader))
                    (or (and (not (isSus ?follower)) (not (isBound ?follower))) (and (isSus ?follower) (isBound ?follower)))
    (forall (?sus - character) (or (or (not (atLoc ?sus ?loc))  (not (isSus ?sus))) (isDead ?sus) )) 
    )
    :effect (and (follows ?follower ?leader)
    )
)
(:action pickup
    :parameters (?char - character ?i - thing ?loc - location)
    :precondition (and (onGround ?i ?loc) (atLoc ?char ?loc) (isAvailable ?char))
    :effect (and (havething ?char ?i) (not (onGround ?i ?loc))
    )
)
(:action untie
    :parameters (?char1 - player ?char2 - character ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (isBound ?char2)  (isAvailable ?char1) 
    (forall (?sus - character) (or (or (not (atLoc ?sus ?loc))  (not (isSus ?sus))) (isDead ?sus) )) 
    )
    :effect (and (not (isBound ?char2)) (isAvailable ?char2)
    )
)
(:action askInfo
    :parameters (?char1 - player ?char2 - character ?loc - location ?inf - info)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (knowInfo ?char2 ?inf) (not (= ?char1 ?char2)) (not (isDead ?char1)) (not (isDead ?char2)))
    :effect (and (not (isUnknown ?inf))
    )
)
(:action accuse
    :parameters (?char1 - player ?char2 - npc ?loc - location ?inf - info ?typ - monster)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (isMonster ?char2 ?typ ?inf) (not (isUnknown ?inf)) )
    :effect (and (isSus ?char2)
    )
)

(:action give
    :parameters (?char1 ?char2 - character ?i - thing ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (havething ?char1 ?i) (not (isDead ?char1)) (not (isSus ?char1)) (not (= ?char1 ?char2))) 
    :effect (and (havething ?char2 ?i) (not (havething ?char1 ?i))
    )
)
(:action dismember
    :parameters (?char1 - player ?char2 - npc ?bp - trophy ?loc - location ?blad - thing)
    :precondition (and (atLoc ?char1 ?loc) (havething ?char1 ?blad) (canCut ?blad) (atLoc ?char2 ?loc) (isAvailable ?char1) (isDead ?char2) (haveBodyPart ?char2 ?bp))
    :effect (and (onGround ?bp ?loc) (not (haveBodyPart ?char2 ?bp))
    )
)
(:action endscort
    :parameters (?char1 ?char2 - character ?loc - location)
    :precondition (and (isDestination ?char2 ?loc) (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (follows ?char2 ?char1) (not (= ?char1 ?char2)))
    :effect (and (not (isMissing ?char2)) (not (follows ?char2 ?char1)) (not (isDestination ?char2 ?loc)) (not (isAvailable ?char2))
    )
)
(:action kidnap
    :parameters (?mon - character ?vict - npc ?from ?to - location ?typ - monster ?inf - info)
    :precondition (and (isMonster ?mon ?typ ?inf) (not (isMissing ?vict)) (not (isDead ?mon)) (atLoc ?vict ?from) (isLair ?mon ?to) (not (= ?mon ?vict)))
    :effect (and (atLoc ?vict ?to) (isMissing ?vict) (isDestination ?vict ?from) (isBound ?vict) (not (atLoc ?vict ?from)) (knowInfo ?vict ?inf)
    )
)

)