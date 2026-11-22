module Main (main) where

import GHC.IO.Encoding (setLocaleEncoding, utf8)
import System.Environment (getArgs)
import System.IO (hSetEncoding, stdout)

import Normalize (normalize)
import Render (render)
import Sentences (sortByWords, splitSentences, wordCount)
import Tokenizer (tokenize)

import Data.List (isPrefixOf, partition)

main :: IO ()
main = do
  setLocaleEncoding utf8
  hSetEncoding stdout utf8
  args <- getArgs
  let (flags, files) = partition ("--" `isPrefixOf`) args
      withCounts     = "--counts" `elem` flags
      inPath  = case files of
        (p : _) -> p
        []      -> "data/textbook.txt"
      outPath = case drop 1 files of
        (o : _) -> o
        []      -> "data/result.txt"
  raw <- readFile inPath
  let text      = normalize (filter (/= '\xFEFF') raw)
      sentences = filter ((> 0) . wordCount)
                . splitSentences
                . tokenize
                $ text
      sorted    = sortByWords sentences
      fmt (i, s)
        | withCounts = show i ++ ". [" ++ show (wordCount s) ++ " words] " ++ render s
        | otherwise  = render s
      body     = map fmt (zip [1 :: Int ..] sorted)
      outLines
        | withCounts = ("Total number of sentences: " ++ show (length sorted)) : "" : body
        | otherwise  = body
  writeFile outPath (unlines outLines)
  putStrLn ("Result written to " ++ outPath)