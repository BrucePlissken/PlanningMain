(define (domain ad)
(:requirements :universal-preconditions :disjunctive-preconditions :quantified-preconditions :typing :equality :negative-preconditions   :fluents :conditional-effects)
(:types
    player npc - character
    area site - location
    consumable weapon trophy item - thing
    info
    monster
)

(:predicates
    (atLoc ?char - character ?loc - location)
    (onGround ?i - thing ?loc - location)
    (canTrack ?char - character)
    (havething ?char - character ?i - thing)
    (inArea ?site - site ?area - area)
    (trackInfo ?inf - info ?loc - location ?lair - location)
    (isSus ?char - character)
    (isAvailable ?char - character)
    (isDead ?char - character)
    (isBound ?char - character)
    (haveBodyPart ?char - character ?bp - trophy)
    (follows ?follower ?leader - character)
    (isMonster ?char - character ?typ - monster ?inf - info)
    (isMissing ?char - character)
    (isLair ?char - character ?loc - location)
    (isDestination ?char - character ?loc - location)
    (canCut ?thing - thing)
    (knowInfo ?char - character ?omni)
    (isUnknown ?omni)
)
(:functions
    (total-cost)
)
(:action move
    :parameters (?char - player ?from - location ?to - site ?area - area)
    :precondition (and (atLoc ?char ?from) (not (isUnknown ?to)) (isAvailable ?char) (inArea ?to ?area) (or (= ?from ?area) (inArea ?from ?area)) )
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to)
    (forall (?follower - character) (when (follows ?follower ?char) (and (atLoc ?follower ?to) (not (atLoc ?follower ?from))) ))
    (increase (total-cost) 2)
    )
)
(:action travel
    :parameters (?char - player ?from - location ?to - area)
    :precondition (and (atLoc ?char ?from) (not (isUnknown ?to)) (isAvailable ?char))
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to)
    (forall (?follower - character) (when (follows ?follower ?char) (and (atLoc ?follower ?to) (not (atLoc ?follower ?from))) ))
    (increase (total-cost) 2)
    )
)
(:action investigatetrack
    :parameters (?char - character ?inf - info ?loc ?lair - location)
    :precondition (and (atLoc ?char ?loc) (canTrack ?char) (trackInfo ?inf ?loc ?lair) (isAvailable ?char) (not (isUnknown ?inf)))
    :effect (and (not (isUnknown ?lair))
    (increase (total-cost) 2)
    )
)
(:action attack
    :parameters (?char1 - player ?char2 - character ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (or (isSus ?char2) (and (isMonster ?char2 ?typ ?inf) (not (isUnknown ?inf)))) (isAvailable ?char1) (not (= ?char1 ?char2)))
    :effect (and (isDead ?char2) (not (isSus ?char2))
    (forall (?i - thing) (when (havething ?char2 ?i) (and (onGround ?i ?loc) (not (havething ?char2 ?i)))))
    (increase (total-cost) 2)
    )
)
(:action gowith
    :parameters (?follower ?leader - character ?loc - location)
    :precondition (and (atLoc ?leader ?loc) (atLoc ?follower ?loc) (isAvailable ?follower) (not (= ?follower ?leader))
                    (or (and (not (isSus ?follower)) (not (isBound ?follower))) (and (isSus ?follower) (isBound ?follower)))
    (forall (?sus - character) (or (or (not (atLoc ?sus ?loc))  (not (isSus ?sus))) (isDead ?sus) )) 
    )
    :effect (and (follows ?follower ?leader)
    (increase (total-cost) 4)
    )
)
(:action pickup
    :parameters (?char - character ?i - thing ?loc - location)
    :precondition (and (onGround ?i ?loc) (atLoc ?char ?loc) (isAvailable ?char))
    :effect (and (havething ?char ?i) (not (onGround ?i ?loc))
    (increase (total-cost) 1)
    )
)
(:action untie
    :parameters (?char1 - player ?char2 - character ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (isBound ?char2)  (isAvailable ?char1) 
    (forall (?sus - character) (or (or (not (atLoc ?sus ?loc))  (not (isSus ?sus))) (isDead ?sus) )) 
    )
    :effect (and (not (isBound ?char2)) (isAvailable ?char2)
    (increase (total-cost) 1)
    )
)
(:action askInfo
    :parameters (?char1 - player ?char2 - character ?loc - location ?inf - info)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (knowInfo ?char2 ?inf) (not (= ?char1 ?char2)) (not (isDead ?char1)) (not (isDead ?char2)))
    :effect (and (not (isUnknown ?inf))
    (increase (total-cost) 1)
    )
)
(:action askloc
    :parameters (?char1 - player ?char2 - character ?loc - location ?inf - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (knowInfo ?char2 ?inf) (not (= ?char1 ?char2)) (not (isDead ?char1)) (not (isDead ?char2)))
    :effect (and (not (isUnknown ?inf))
    )
)
(:action give
    :parameters (?char1 ?char2 - character ?i - thing ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (havething ?char1 ?i) (not (isDead ?char1)) (not (isSus ?char1)) (not (= ?char1 ?char2))) 
    :effect (and (havething ?char2 ?i) (not (havething ?char1 ?i))
    (increase (total-cost) 2)
    )
)
(:action dismember
    :parameters (?char1 ?char2 - character ?bp - trophy ?loc - location ?blad - thing)
    :precondition (and (atLoc ?char1 ?loc) (havething ?char1 ?blad) (canCut ?blad) (atLoc ?char2 ?loc) (isAvailable ?char1) (not (= ?char1 ?char2)) (isDead ?char2) (haveBodyPart ?char2 ?bp))
    :effect (and (onGround ?bp ?loc) (not (haveBodyPart ?char2 ?bp))
    (increase (total-cost) 1)
    )
)
(:action endscort
    :parameters (?char1 ?char2 - character ?loc - location)
    :precondition (and (isDestination ?char2 ?loc) (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (follows ?char2 ?char1) (not (= ?char1 ?char2)))
    :effect (and (not (isMissing ?char2)) (not (follows ?char2 ?char1)) (not (isDestination ?char2 ?loc))
    )
)
(:action kidnap
    :parameters (?mon - character ?vict - npc ?from ?to - location ?typ - monster ?inf - info)
    :precondition (and (isMonster ?mon ?typ ?inf) (not (isMissing ?vict)) (not (isDead ?mon)) (atLoc ?vict ?from) (isLair ?mon ?to))
    :effect (and (atLoc ?vict ?to) (isMissing ?vict) (isDestination ?vict ?from) (isBound ?vict) (not (atLoc ?vict ?from)) (knowInfo ?vict ?inf)
    (increase (total-cost) 15)
    )
)

)