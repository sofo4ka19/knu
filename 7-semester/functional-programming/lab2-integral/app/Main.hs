module Main where

import Control.Concurrent (getNumCapabilities)
import Control.Exception (SomeException, evaluate, try)
import GHC.Clock (getMonotonicTime)
import Text.Printf (printf)
import Integrate

f :: F
f x = sum [ sin (fromIntegral j * x) / fromIntegral j | j <- [1 .. 200 :: Int] ]

lowerA, upperB, epsilon :: Double
lowerA  = 0
upperB  = 10
epsilon = 1e-10

timed :: String -> IO Double -> IO ()
timed label act = do
  t0  <- getMonotonicTime
  res <- try act :: IO (Either SomeException Double)
  t1  <- getMonotonicTime
  case res of
    Left e  -> printf "%-12s ERROR: %s\n" label (show e)
    Right r -> printf "%-12s J = %.12f   time = %.3f ms\n"
                      label r ((t1 - t0) * 1000)

main :: IO ()
main = do
  caps <- getNumCapabilities
  let k = 64
  printf "A=%g B=%g eps=%g threads=%d chunks=%d\n"
         lowerA upperB epsilon caps k
  timed "sequential"  (evaluate (integrateSeq f lowerA upperB epsilon))
  timed "parMap"      (evaluate (integratePar k f lowerA upperB epsilon))
  timed "forkIO+MVar" (integrateConc k f lowerA upperB epsilon)