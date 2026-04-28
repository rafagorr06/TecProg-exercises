#lang racket

;'(a b c . x)
(cdr(cdr(cdr'(a b c . x))))

;'(a b c x)
(car(cdr(cdr(cdr'(a b c x)))))

;'((a . x) b)
