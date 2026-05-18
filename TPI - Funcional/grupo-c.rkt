#lang racket

; TPI - Funcional
; Integrantes:
; - Rafael Gorrochategui
; - Juan Pablo Iurato
; - Franco Caraffa
; - Zahir Argarañaz

(define despachos-lunes '(
  ((aa180be 15000) (4500 3000) (9000))
  ((ab550zd 12000) (3000 5000 1000) (500 2000))
  ((aa790ga 19000) (3500) (2800) (1100 400))))

(define lista-camiones
  (lambda (despachos)
    (map (lambda (despacho) (car (car despacho))) despachos)))

(define sumar-contenedores
  (lambda (contenedores)
    (if (null? contenedores)
        0
        (+ (apply + (car contenedores)) 
           (sumar-contenedores (cdr contenedores))))))

(define carga-kg
  (lambda (despachos patente)
    (cond
      [(null? despachos) "Patente inexistente"]
      [(equal? (car (car (car despachos))) patente) 
       (sumar-contenedores (cdr (car despachos)))]
      [else (carga-kg (cdr despachos) patente)])))

; pruebas
(lista-camiones despachos-lunes)
(carga-kg despachos-lunes 'aa180be)