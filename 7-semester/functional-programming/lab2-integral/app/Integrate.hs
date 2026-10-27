module Integrate
  ( F, simpson, runge
  , integrateSeq, integratePar, integrateConc
  ) where

import Control.Concurrent (forkFinally, newEmptyMVar, putMVar, takeMVar)
import Control.Exception (evaluate, throwIO)
import Control.Parallel.Strategies (parMap, rdeepseq)
import Data.Functor.Identity (Identity (..))

type F = Double -> Double

simpson :: F -> Double -> Double -> Int -> Double
simpson f a b n = h / 3 * (f a + f b + 4 * odds + 2 * evens)
  where
    h     = (b - a) / fromIntegral n
    x i   = a + fromIntegral i * h
    odds  = foldl' (\s i -> s + f (x i)) 0 [1, 3 .. n - 1]
    evens = foldl' (\s i -> s + f (x i)) 0 [2, 4 .. n - 2]

runge :: Monad m => (Int -> m Double) -> Double -> m Double
runge rule eps = rule 2 >>= go 2
  where
    go m prev = do
      let m' = 2 * m
      cur <- rule m'
      if bad cur || abs (cur - prev) / 15 < eps
        then return cur
        else go m' cur
    bad x = isNaN x || isInfinite x

pureRunge :: (Int -> Double) -> Double -> Double
pureRunge rule eps = runIdentity (runge (Identity . rule) eps)

integrateSeq :: F -> Double -> Double -> Double -> Double
integrateSeq f a b = pureRunge (simpson f a b)

integratePar :: Int -> F -> Double -> Double -> Double -> Double
integratePar k f a b = pureRunge (simpsonPar f a b k)

simpsonPar :: F -> Double -> Double -> Int -> Int -> Double
simpsonPar f a b k m = sum (parMap rdeepseq piece [0 .. k - 1])
  where
    w       = (b - a) / fromIntegral k
    piece i = let l = a + fromIntegral i * w
              in simpson f l (l + w) m

integrateConc :: Int -> F -> Double -> Double -> Double -> IO Double
integrateConc k f a b eps = do
  r <- runge (simpsonConc f a b k) eps
  if isNaN r || isInfinite r
    then ioError (userError "integral is NaN or Infinity: f is undefined on [A,B]")
    else return r

simpsonConc :: F -> Double -> Double -> Int -> Int -> IO Double
simpsonConc f a b k m = do
  vars  <- mapM spawn [0 .. k - 1]   -- 1) launch k threads, each computing a partial integral
  parts <- mapM (\v -> takeMVar v >>= either throwIO return) vars        -- 2) waiting and collecting the results from each thread
  return (sum parts)                 -- 3) sum partial results to get the final result
  where
    w = (b - a) / fromIntegral k
    spawn i = do
      box <- newEmptyMVar
      let l = a + fromIntegral i * w
      _ <- forkFinally (evaluate (simpson f l (l + w) m)) (putMVar box)
      return box