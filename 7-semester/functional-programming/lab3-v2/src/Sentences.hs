module Sentences (splitSentences) where

import Types (Punctuation (..), Sentence (..), Token (..), Word (..))
import Data.Char (isUpper)

isTerminator :: Token -> Bool
isTerminator (TPunct (Punctuation p)) = p `elem` ".!?…"
isTerminator _                        = False

isEnding :: Token -> Bool
isEnding t@(TPunct (Punctuation p)) = isTerminator t || p `elem` ")]}»”"
isEnding _                          = False

isOpener :: Token -> Bool
isOpener (TPunct (Punctuation p)) = p `elem` "([{«“\""
isOpener _                        = False

startsNewSentence :: [Token] -> Bool
startsNewSentence ts = case dropWhile isOpener ts of
  []                         -> True
  (TWord (Word (c : _)) : _) -> isUpper c
  _                          -> False

splitSentences :: [Token] -> [Sentence]
splitSentences = go []
  where
    go acc [] = [Sentence (reverse acc) | not (null acc)]
    go acc (t : ts)
      | isTerminator t =
          let (ends, rest) = span isEnding ts
              acc'         = reverse (t : ends) ++ acc
          in  if startsNewSentence rest
                then Sentence (reverse acc') : go [] rest
                else go acc' rest
      | otherwise = go (t : acc) ts