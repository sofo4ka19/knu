module Integrate ( F, simpson, integrateSeq, simpsonPar, integratePar ) where

import Control.Parallel.Strategies (parMap, rdeepseq)

type F = Double -> Double

simpson :: F -> Double -> Double -> Int -> Double
simpson f a b n = h / 3 * (f a + f b + 4 * odds + 2 * evens)
  where
    h     = (b - a) / fromIntegral n
    x i   = a + fromIntegral i * h
    odds  = foldl' (\s i -> s + f (x i)) 0 [1, 3 .. n - 1]
    evens = foldl' (\s i -> s + f (x i)) 0 [2, 4 .. n - 2]

integrateSeq :: F -> Double -> Double -> Double -> Double
integrateSeq f a b eps = go 2 (simpson f a b 2)
  where
    go n prev =
      let n'  = 2 * n
          cur = simpson f a b n'
      in if abs (cur - prev) / 15 < eps then cur else go n' cur

simpsonPar :: F -> Double -> Double -> Int -> Int -> Double
simpsonPar f a b k m = sum (parMap rdeepseq piece [0 .. k - 1])
  where
    w       = (b - a) / fromIntegral k
    piece i = let l = a + fromIntegral i * w
              in simpson f l (l + w) m

integratePar :: Int -> F -> Double -> Double -> Double -> Double
integratePar k f a b eps = go 2 (simpsonPar f a b k 2)
  where
    go m prev =
      let m'  = 2 * m
          cur = simpsonPar f a b k m'
      in if abs (cur - prev) / 15 < eps then cur else go m' cur