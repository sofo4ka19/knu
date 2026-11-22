module Main (main) where

import GHC.IO.Encoding (setLocaleEncoding, utf8)
import System.Environment (getArgs)
import System.IO (hSetEncoding, stdout)

import Normalize (normalize)
import Render (render)
import Sentences (sortByWords, splitSentences, wordCount)
import Tokenizer (tokenize)

main :: IO ()
main = do
  setLocaleEncoding utf8
  hSetEncoding stdout utf8
  args <- getArgs
  let inPath  = case args of
        (p : _) -> p
        []      -> "data/textbook.txt"
      outPath = case drop 1 args of
        (o : _) -> o
        []      -> "data/result.txt"
  raw <- readFile inPath
  let text      = normalize (filter (/= '\xFEFF') raw)
      sentences = filter ((> 0) . wordCount)
                . splitSentences
                . tokenize
                $ text
      sorted    = sortByWords sentences
      outLines  = ("Total number of sentences: " ++ show (length sorted))
                : ""
                : [ show i ++ ". [" ++ show (wordCount s) ++ " words] " ++ render s
                  | (i, s) <- zip [1 :: Int ..] sorted ]
  writeFile outPath (unlines outLines)
  putStrLn ("Result written to " ++ outPath)