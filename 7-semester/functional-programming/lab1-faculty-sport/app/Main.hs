module Main where

import DB
import UI
import System.IO (hSetBuffering, stdout, BufferMode(NoBuffering))

main :: IO ()
main = do
  hSetBuffering stdout NoBuffering
  conn <- connectDB
  putStrLn "Підключено до бази!"
  runMenu conn