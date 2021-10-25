(define (domain ad)
(:requirements :universal-preconditions :disjunctive-preconditions :quantified-preconditions)
(:types
    player npc - character
    area site - location
    consumable weapon trophy - item
    info
    goblin creep vampire - monster
)

(:predicates
    (hasTrack ?loc - location)
    (canTrack ?char - character)
    (haveItem ?char - character ?i - item)
    (atLoc ?char - character ?loc - location)
    (trackInfo ?inf - info ?loc - location ?lair - location)
    (isSus ?char - character)
    (onGround ?i - item ?loc - location)
    (isAvailable ?char - character)
    (isDead ?char - character)
    (isUnknown ?omni)
    (isBound ?char - character)
    (knowInfo ?char - character ?inf - info)
    (haveBodyPart ?char - character ?bp - trophy)
    (canCut ?item - item)
    (isMonster ?char - character ?typ - monster)
    (inArea ?site - site ?area - area)
    (follows ?follower ?leader - character)
)
(:functions
    (total-cost)
)
(:action move
    :parameters (?char - player ?from - location ?to - site ?area - area)
    :precondition (and (atLoc ?char ?from) (not (isUnknown ?to)) (isAvailable ?char) (inArea ?to ?area) (or (= ?from ?area) (inArea ?from ?area)) )
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to)
    (forall (?follower - character) (when (follows ?follower ?char) (and (not (atLoc ?follower ?from)) (atLoc ?follower ?to)) ))
    (increase (total-cost) 2)
    )
)
(:action travel
    :parameters (?char - player ?from - location ?to - area)
    :precondition (and (atLoc ?char ?from) (not (isUnknown ?to)) (isAvailable ?char))
    :effect (and (not (atLoc ?char ?from)) (atLoc ?char ?to)
    (forall (?follower - character) (when (follows ?follower ?char) (and (not (atLoc ?follower ?from)) (atLoc ?follower ?to)) ))
    (increase (total-cost) 2)
    )
)
(:action investigate
    :parameters (?char - character ?inf - info ?loc ?lair - location)
    :precondition (and (atLoc ?char ?loc) (canTrack ?char) (hasTrack ?loc) (trackInfo ?inf ?loc ?lair) (isAvailable ?char) (not (isUnknown ?inf)))
    :effect (and (not (isUnknown ?lair))
    (increase (total-cost) 2)
    )
)
(:action attack
    :parameters (?char1 - player ?char2 - character ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (isSus ?char2) (isAvailable ?char1) (not (= ?char1 ?char2)))
    :effect (and (isDead ?char2) (not (isSus ?char2))
    (forall (?i - item) (when (haveItem ?char2 ?i) (and (onGround ?i ?loc) (not (haveItem ?char2 ?i)))))
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
    :parameters (?char - character ?i - item ?loc - location)
    :precondition (and (onGround ?i ?loc) (atLoc ?char ?loc) (isAvailable ?char))
    :effect (and (haveItem ?char ?i) (not (onGround ?i ?loc))
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
(:action talk
    :parameters (?char1 - player ?char2 - character ?loc - location ?inf - info)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (knowInfo ?char2 ?inf) (not (= ?char1 ?char2)))
    :effect (and (not (isUnknown ?inf))
    (increase (total-cost) 1)
    )
)
(:action give
    :parameters (?char1 ?char2 - character ?i - item ?loc - location)
    :precondition (and (atLoc ?char1 ?loc) (atLoc ?char2 ?loc) (haveItem ?char1 ?i) (not (isDead ?char1)) (not (isSus ?char1)) (not (= ?char1 ?char2))) 
    :effect (and (haveItem ?char2 ?i) (not (haveItem ?char1 ?i))
    (increase (total-cost) 2)
    )
)
(:action dismember
    :parameters (?char1 ?char2 - character ?bp - trophy ?loc - location ?blad - item)
    :precondition (and (atLoc ?char1 ?loc) (haveItem ?char1 ?blad) (canCut ?blad) (atLoc ?char2 ?loc) (isAvailable ?char1) (not (= ?char1 ?char2)) (isDead ?char2) (haveBodyPart ?char2 ?bp))
    :effect (and (onGround ?bp ?loc) (not (haveBodyPart ?char2 ?bp))
    (increase (total-cost) 1)
    )
)
)