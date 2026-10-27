module Integrate
  ( F, simpson, integrateSeq
  , simpsonPar, integratePar
  , simpsonConc, integrateConc
  ) where

import Control.Concurrent (forkIO, newEmptyMVar, putMVar, takeMVar)
import Control.Exception (evaluate)
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

simpsonConc :: F -> Double -> Double -> Int -> Int -> IO Double
simpsonConc f a b k m = do
  vars  <- mapM spawn [0 .. k - 1]   -- 1) launch k threads, each computing a partial integral
  parts <- mapM takeMVar vars        -- 2) waiting and collecting the results from each thread
  return (sum parts)                 -- 3) sum partial results to get the final result
  where
    w = (b - a) / fromIntegral k
    spawn i = do
      box <- newEmptyMVar
      _   <- forkIO $ do
               let l = a + fromIntegral i * w
               r <- evaluate (simpson f l (l + w) m)
               putMVar box r
      return box


integrateConc :: Int -> F -> Double -> Double -> Double -> IO Double
integrateConc k f a b eps = do
  first <- simpsonConc f a b k 2
  go 2 first
  where
    go m prev = do
      let m' = 2 * m
      cur <- simpsonConc f a b k m'
      if abs (cur - prev) / 15 < eps
        then return cur
        else go m' cur