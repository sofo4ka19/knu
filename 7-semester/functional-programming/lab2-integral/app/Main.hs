module Main where

import Integrate

f :: F
f x = exp (negate (x * x))

main :: IO ()
main = do
  print (integrateSeq f 0 3 1e-10)
  print (integratePar 48 f 0 3 1e-10)