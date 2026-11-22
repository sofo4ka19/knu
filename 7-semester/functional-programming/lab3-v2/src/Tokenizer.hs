module Tokenizer (tokenize) where

import Data.Char (isAlphaNum, isSpace)

import Types (Punctuation (..), Symbol, Token (..), Word (..))

isWordChar :: Symbol -> Bool
isWordChar c = isAlphaNum c || c == '_'

isInner :: Symbol -> Bool
isInner c = c `elem` ".-'’"

spanWord :: [Symbol] -> ([Symbol], [Symbol])
spanWord (c : i : d : cs)
  | isWordChar c && isInner i && isWordChar d =
      let (w, rest) = spanWord (d : cs)
      in  (c : i : w, rest)
spanWord (c : cs)
  | isWordChar c =
      let (w, rest) = spanWord cs
      in  (c : w, rest)
spanWord cs = ([], cs)

tokenize :: [Symbol] -> [Token]
tokenize = go False
  where
    go _ [] = []
    go sp xs@(c : cs)
      | isSpace c    = go True cs
      | isWordChar c = let (w, rest) = spanWord xs
                       in  TWord sp (Word w) : go False rest
      | otherwise    = TPunct sp (Punctuation c) : go False cs