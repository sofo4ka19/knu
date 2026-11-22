module Sentences ( splitSentences
  , wordCount
  , sortByWords
  ) where

import Types (Punctuation (..), Sentence (..), Token (..), Word (..))
import Data.Char (isDigit, isUpper)
import Data.List (sortOn)

isTerminator :: Token -> Bool
isTerminator (TPunct _ (Punctuation p)) = p `elem` ".!?…"
isTerminator _                        = False

isEnding :: Token -> Bool
isEnding t@(TPunct _ (Punctuation p))   = isTerminator t || p `elem` ")]}»”"
isEnding _                          = False

isOpener :: Token -> Bool
isOpener (TPunct _ (Punctuation p))     = p `elem` "([{«“\""
isOpener _                        = False

startsNewSentence :: [Token] -> Bool
startsNewSentence ts = case dropWhile isOpener ts of
  []                           -> True
  (TWord _ (Word (c : _)) : _) | isUpper c -> True
  (TWord _ (Word w) : TPunct _ (Punctuation p) : TWord _ (Word (c : _)) : _)
    | all isDigit w && p `elem` ".)" && isUpper c -> True
  _                            -> False

isLoneNumber :: [Token] -> Bool
isLoneNumber [TWord _ (Word w)] = all isDigit w
isLoneNumber _                  = False

-- | Чи був пробіл перед лексемою у вихідному тексті.
spaceBefore :: Token -> Bool
spaceBefore (TWord sp _)  = sp
spaceBefore (TPunct sp _) = sp

splitSentences :: [Token] -> [Sentence]
splitSentences = go []
  where
    go acc [] = [Sentence (reverse acc) | not (null acc)]
    go acc (t : ts)
      | isTerminator t && not (isLoneNumber acc) =
          let (ends, rest) = span isEnding ts
              acc'         = reverse (t : ends) ++ acc
              -- після знака має йти пробіл (або кінець тексту),
              -- а перед ним пробілу бути не повинно: x!(i,k), #-}!Int, forall a .
              spaceAfter   = case rest of
                               []      -> True
                               (x : _) -> spaceBefore x
              realEnd      = not (spaceBefore t) && spaceAfter && startsNewSentence rest
          in  if realEnd
                then Sentence (reverse acc') : go [] rest
                else go acc' rest
      | otherwise = go (t : acc) ts

wordCount :: Sentence -> Int
wordCount (Sentence ts) = length [w | TWord _ w <- ts]

sortByWords :: [Sentence] -> [Sentence]
sortByWords = sortOn wordCount