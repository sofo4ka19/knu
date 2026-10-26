module Main where

import Integrate

f :: F
f x = exp (negate (x * x))

main :: IO ()
main = print (integrateSeq f 0 3 1e-10)