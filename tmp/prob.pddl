(define (problem gripper)
 (:domain ballbot)
 (:objects rooma roomb - room
            ball1 ball2 ball3 ball4 - ball
            left right - gripper
            )
 (:init 
        (free left)
        (free right)
        (atrobby rooma)
        (atball ball1 rooma)
        (atball ball2 rooma)
        (atball ball3 rooma)
        (atball ball4 rooma)
        )

 (:goal 
       (and
              (atball ball1 roomb)
              (atball ball2 roomb)
              (atball ball3 roomb)
              (atball ball4 roomb)
       )
 )
)